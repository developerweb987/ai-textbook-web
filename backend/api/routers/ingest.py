from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os
import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from config import settings
import hashlib
import logging

router = APIRouter()

class IngestRequest(BaseModel):
    docs_path: str = "../ai-textbook-web/docs"

class IngestResponse(BaseModel):
    message: str
    documents_processed: int
    chunks_created: int

def clean_markdown_text(text: str) -> str:
    """
    Clean markdown text by removing code blocks, headers, and other markdown syntax
    """
    # Remove markdown code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`.*?`', '', text)
    # Remove markdown headers but keep the text
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove markdown links and images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
    text = re.sub(r'_{1,2}(.*?)_{1,2}', r'\1', text)
    # Remove extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(request: IngestRequest):
    """
    Ingest all .md and .mdx files from the specified directory,
    chunk content, generate embeddings, and store in Qdrant
    """
    try:
        logging.info(f"Starting ingestion from: {request.docs_path}")

        # Initialize services
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GEMINI_API_KEY
        )

        # Initialize Qdrant client with settings
        if settings.QDRANT_URL:
            qdrant_client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
        elif settings.QDRANT_HOST:
            qdrant_client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                api_key=settings.QDRANT_API_KEY
            )
        else:
            raise HTTPException(status_code=500, detail="Qdrant configuration is missing")

        # Create collection if it doesn't exist
        try:
            collections = qdrant_client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if settings.COLLECTION_NAME not in collection_names:
                qdrant_client.create_collection(
                    collection_name=settings.COLLECTION_NAME,
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
                )
                logging.info(f"Created collection: {settings.COLLECTION_NAME}")
        except Exception as e:
            logging.error(f"Error creating collection: {str(e)}")
            raise

        # Find all .md and .mdx files
        docs_path = Path(request.docs_path)
        if not docs_path.exists():
            raise HTTPException(status_code=404, detail=f"Directory {request.docs_path} not found")

        markdown_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.mdx"))

        if not markdown_files:
            raise HTTPException(status_code=404, detail="No markdown files found in the specified directory")

        logging.info(f"Found {len(markdown_files)} markdown files")

        total_chunks = 0
        total_docs = 0

        # Text splitter for chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,  # ~700 tokens as requested
            chunk_overlap=50,
            length_function=len,
        )

        points = []

        for file_path in markdown_files:
            try:
                logging.info(f"Processing file: {file_path}")

                # Load the markdown file
                loader = UnstructuredMarkdownLoader(str(file_path))
                documents = loader.load()

                # Combine all content
                full_content = " ".join([doc.page_content for doc in documents])

                # Clean the markdown content
                cleaned_content = clean_markdown_text(full_content)

                # Split content into chunks
                chunks = text_splitter.split_text(cleaned_content)

                logging.info(f"Split {file_path.name} into {len(chunks)} chunks")

                # Process each chunk
                for i, chunk in enumerate(chunks):
                    # Generate embedding
                    embedding = embeddings.embed_query(chunk)

                    # Create unique ID for the chunk
                    chunk_id = hashlib.md5(f"{file_path.name}_{i}_{chunk[:100]}".encode()).hexdigest()

                    # Create point for Qdrant
                    point = PointStruct(
                        id=chunk_id,
                        vector=embedding,
                        payload={
                            "text": chunk,
                            "source_file": str(file_path.relative_to(docs_path))
                        }
                    )
                    points.append(point)

                total_chunks += len(chunks)
                total_docs += 1

            except Exception as e:
                logging.error(f"Error processing file {file_path}: {str(e)}")
                continue  # Continue with other files

        # Upload all points to Qdrant
        if points:
            qdrant_client.upsert(
                collection_name=settings.COLLECTION_NAME,
                points=points
            )
            logging.info(f"Stored {len(points)} chunks in Qdrant")

        message = f"Successfully ingested {total_docs} documents and created {total_chunks} chunks"
        logging.info(message)

        return IngestResponse(
            message=message,
            documents_processed=total_docs,
            chunks_created=total_chunks
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logging.error(f"Error during ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during ingestion: {str(e)}")