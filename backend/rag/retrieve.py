from typing import List, Dict
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize embeddings model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=settings.GEMINI_API_KEY
)

# Initialize Qdrant client
if settings.QDRANT_URL:
    qdrant_client = AsyncQdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=True
    )
else:
    qdrant_client = AsyncQdrantClient(
        url=settings.QDRANT_HOST,
        api_key=settings.QDRANT_API_KEY,
        port=settings.QDRANT_PORT,
        prefer_grpc=True
    )

async def retrieve_documents(query: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieve relevant documents from Qdrant based on the query
    """
    try:
        # Generate embedding for the query
        query_embedding = await embeddings.aembed_query(query)

        # Search in Qdrant
        search_results = await qdrant_client.search(
            collection_name=settings.COLLECTION_NAME,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Format results
        retrieved_docs = []
        for hit in search_results:
            doc = {
                "id": hit.id,
                "text": hit.payload.get("text", ""),
                "source_file": hit.payload.get("source_file", ""),
                "chunk_index": hit.payload.get("chunk_index", 0),
                "score": hit.score
            }
            retrieved_docs.append(doc)

        logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query[:50]}...")
        return retrieved_docs

    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        raise

async def retrieve_document_by_id(doc_id: str) -> Dict:
    """
    Retrieve a specific document by its ID
    """
    try:
        # Retrieve point by ID
        points = await qdrant_client.retrieve(
            collection_name=settings.COLLECTION_NAME,
            ids=[doc_id],
            with_payload=True
        )

        if not points:
            return {}

        point = points[0]
        doc = {
            "id": point.id,
            "text": point.payload.get("text", ""),
            "source_file": point.payload.get("source_file", ""),
            "chunk_index": point.payload.get("chunk_index", 0)
        }

        return doc

    except Exception as e:
        logger.error(f"Error retrieving document by ID: {str(e)}")
        raise

async def get_all_documents(limit: int = 100) -> List[Dict]:
    """
    Retrieve all documents (up to limit) from Qdrant
    """
    try:
        # Scroll through collection to get all points
        points, _ = await qdrant_client.scroll(
            collection_name=settings.COLLECTION_NAME,
            limit=limit,
            with_payload=True
        )

        documents = []
        for point in points:
            doc = {
                "id": point.id,
                "text": point.payload.get("text", ""),
                "source_file": point.payload.get("source_file", ""),
                "chunk_index": point.payload.get("chunk_index", 0)
            }
            documents.append(doc)

        logger.info(f"Retrieved {len(documents)} documents from collection")
        return documents

    except Exception as e:
        logger.error(f"Error retrieving all documents: {str(e)}")
        raise