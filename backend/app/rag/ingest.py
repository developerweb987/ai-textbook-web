import os
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_cohere import CohereEmbeddings
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from config import settings
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize embeddings model
embeddings = CohereEmbeddings(
    model="embed-multilingual-v2.0",
    cohere_api_key=settings.COHERE_API_KEY
)

# Initialize Qdrant client
qdrant_client = AsyncQdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    prefer_grpc=True
)

async def setup_collection(force_recreate: bool = False):
    """
    Setup Qdrant collection for storing document embeddings
    """
    try:
        if force_recreate:
            try:
                await qdrant_client.delete_collection(settings.COLLECTION_NAME)
                logger.info(f"Deleted existing collection: {settings.COLLECTION_NAME}")
            except Exception as e:
                logger.info(f"Collection {settings.COLLECTION_NAME} doesn't exist, creating new one: {e}")

        # Check if collection exists
        collections = await qdrant_client.get_collections()
        collection_exists = any(col.name == settings.COLLECTION_NAME for col in collections.collections)

        if not collection_exists:
            # Create collection with 1024-dimensional vectors (standard for Cohere embeddings)
            await qdrant_client.create_collection(
                collection_name=settings.COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=1024,  # Standard dimension for Cohere embeddings
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection: {settings.COLLECTION_NAME}")
        else:
            logger.info(f"Collection {settings.COLLECTION_NAME} already exists")
    except Exception as e:
        logger.error(f"Error setting up collection: {str(e)}")
        raise

def clean_markdown_text(text: str) -> str:
    """
    Clean markdown text by removing unnecessary elements
    """
    import re
    # Remove markdown code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`[^`]*`', '', text)
    # Remove markdown links but keep the text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove image references
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
    # Remove markdown headers but keep the text
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
    text = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', text)
    # Remove extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

async def load_documents(docs_path: str) -> List[Dict]:
    """
    Load and process markdown documents from the specified path
    """
    docs_path = Path(docs_path)
    if not docs_path.exists():
        raise FileNotFoundError(f"Directory {docs_path} does not exist")

    # Find all markdown files
    md_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.mdx"))
    logger.info(f"Found {len(md_files)} markdown files in {docs_path}")

    documents = []
    for file_path in md_files:
        try:
            # Load the markdown file
            loader = UnstructuredMarkdownLoader(str(file_path))
            docs = loader.load()

            # Process each document chunk
            for i, doc in enumerate(docs):
                # Clean the content
                cleaned_content = clean_markdown_text(doc.page_content)

                # Skip empty content
                if not cleaned_content.strip():
                    continue

                # Create document object
                document_obj = {
                    "id": f"{file_path.name}_{i}_{hashlib.md5(cleaned_content[:100].encode()).hexdigest()[:8]}",
                    "filename": str(file_path),
                    "content": cleaned_content,
                    "metadata": {
                        "source_file": str(file_path),
                        "chunk_index": i
                    }
                }
                documents.append(document_obj)

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            continue

    logger.info(f"Loaded {len(documents)} document chunks from {len(md_files)} files")
    return documents

async def chunk_and_embed_documents(documents: List[Dict]) -> List[Dict]:
    """
    Chunk documents and generate embeddings using Cohere
    """
    logger.info(f"Processing {len(documents)} documents for embedding")

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE_TOKENS,
        chunk_overlap=50,
        length_function=len,
    )

    all_chunks_with_embeddings = []

    for doc in documents:
        # Split document into chunks
        content = doc["content"]
        chunks = text_splitter.split_text(content)

        logger.info(f"Split document {doc['filename']} into {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            # Generate embedding for the chunk using Cohere
            try:
                embedding = await embeddings.aembed_query(chunk)

                chunk_obj = {
                    "id": f"{doc['id']}_chunk_{i}",
                    "document_id": doc["id"],
                    "filename": doc["filename"],
                    "content": chunk,
                    "vector": embedding,
                    "metadata": {
                        "source_file": doc["metadata"]["source_file"],
                        "chunk_index": i,
                        "original_doc_id": doc["id"]
                    }
                }
                all_chunks_with_embeddings.append(chunk_obj)
            except Exception as e:
                logger.error(f"Error generating embedding for chunk: {str(e)}")
                continue

    logger.info(f"Generated embeddings for {len(all_chunks_with_embeddings)} chunks")
    return all_chunks_with_embeddings

async def store_embeddings_in_qdrant(chunks_with_embeddings: List[Dict]):
    """
    Store document embeddings in Qdrant
    """
    if not chunks_with_embeddings:
        logger.warning("No chunks to store in Qdrant")
        return

    logger.info(f"Storing {len(chunks_with_embeddings)} embeddings in Qdrant")

    points = []
    for chunk in chunks_with_embeddings:
        point = models.PointStruct(
            id=chunk["id"],
            vector=chunk["vector"],
            payload={
                "text": chunk["content"],
                "source_file": chunk["metadata"]["source_file"],
                "chunk_index": chunk["metadata"]["chunk_index"],
                "original_doc_id": chunk["metadata"]["original_doc_id"]
            }
        )
        points.append(point)

    # Upload points to Qdrant
    await qdrant_client.upsert(
        collection_name=settings.COLLECTION_NAME,
        points=points
    )

    logger.info(f"Successfully stored {len(points)} embeddings in Qdrant")

async def ingest_documents(docs_path: str, force_recreate: bool = False) -> Dict:
    """
    Main function to ingest documents into the RAG system
    """
    logger.info(f"Starting ingestion from: {docs_path}")

    # Setup Qdrant collection
    await setup_collection(force_recreate)

    # Load documents
    documents = await load_documents(docs_path)
    if not documents:
        raise ValueError("No documents found to ingest")

    # Chunk and embed documents using Cohere
    chunks_with_embeddings = await chunk_and_embed_documents(documents)

    # Store embeddings in Qdrant
    await store_embeddings_in_qdrant(chunks_with_embeddings)

    # Return ingestion summary
    unique_docs = set(doc["filename"] for doc in documents)
    result = {
        "message": f"Successfully ingested {len(unique_docs)} documents and created {len(chunks_with_embeddings)} chunks",
        "documents_processed": len(unique_docs),
        "chunks_created": len(chunks_with_embeddings)
    }

    logger.info(result["message"])
    return result

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ingest.py <docs_path> [--force-recreate]")
        sys.exit(1)

    docs_path = sys.argv[1]
    force_recreate = "--force-recreate" in sys.argv

    async def main():
        result = await ingest_documents(docs_path, force_recreate)
        print(result)

    asyncio.run(main())