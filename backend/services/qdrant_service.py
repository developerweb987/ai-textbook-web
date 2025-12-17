import asyncio
from typing import List, Dict, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from config import settings
from utils.logger import app_logger

class QdrantService:
    def __init__(self):
        # Use QDRANT_URL if it's set, otherwise use host/port
        if settings.QDRANT_URL:
            self.client = AsyncQdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
        else:
            self.client = AsyncQdrantClient(
                host=settings.QDRANT_HOST,
                api_key=settings.QDRANT_API_KEY,
                port=settings.QDRANT_PORT,
                grpc_port=6334,
                prefer_grpc=True
            )
        self.collection_name = settings.COLLECTION_NAME

    async def setup_collection(self):
        """
        Create or recreate the collection with appropriate vector configuration
        """
        try:
            app_logger.info(f"Setting up collection '{self.collection_name}'")

            # Check if collection exists
            collections = await self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if collection_exists:
                # Delete existing collection if it exists
                await self.client.delete_collection(self.collection_name)
                app_logger.info(f"Deleted existing collection '{self.collection_name}'")

            # Create new collection with 768-dimensional vectors (Gemini embedding dimensions)
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,  # Standard dimension for text embeddings
                    distance=models.Distance.COSINE
                )
            )

            app_logger.info(f"Collection '{self.collection_name}' created successfully")
        except Exception as e:
            app_logger.error(f"Error setting up collection: {str(e)}")
            raise

    async def store_embeddings(self, documents: List[Dict]):
        """
        Store document embeddings in Qdrant
        """
        try:
            app_logger.info(f"Storing {len(documents)} documents in Qdrant")

            # Prepare points for insertion
            points = []
            for idx, doc in enumerate(documents):
                point = models.PointStruct(
                    id=idx,
                    vector=doc['vector'],
                    payload={
                        'text': doc['content'],  # Required field: the actual text content
                        'source_file': doc['filename'],  # Required field: source file name
                        'section_heading': doc['metadata'].get('section_heading', ''),  # Required field: section heading
                        'id': doc['id'],
                        'document_id': doc['document_id'],
                        'tokens': doc['tokens'],
                        'metadata': doc['metadata']
                    }
                )
                points.append(point)

            # Upload points to Qdrant
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            app_logger.info(f"Successfully stored {len(points)} documents in Qdrant")
        except Exception as e:
            app_logger.error(f"Error storing embeddings in Qdrant: {str(e)}")
            raise

    async def search_similar(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """
        Search for similar documents based on query vector
        """
        try:
            app_logger.debug(f"Searching for similar documents, limit: {limit}")

            search_results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )

            results = []
            for hit in search_results:
                results.append({
                    'id': hit.id,
                    'score': hit.score,
                    'payload': hit.payload
                })

            app_logger.debug(f"Found {len(results)} similar documents")
            return results
        except Exception as e:
            app_logger.error(f"Error searching in Qdrant: {str(e)}")
            return []

    async def get_all_document_ids(self) -> List[str]:
        """
        Get all stored document IDs
        """
        try:
            app_logger.debug("Getting all document IDs from Qdrant")

            records = await self.client.scroll(
                collection_name=self.collection_name,
                limit=10000,  # Adjust as needed
                with_payload=True,
                with_vectors=False
            )

            ids = [record.payload.get('id') for record in records[0] if record.payload.get('id')]
            unique_ids = list(set(ids))  # Return unique IDs

            app_logger.info(f"Retrieved {len(unique_ids)} unique document IDs")
            return unique_ids
        except Exception as e:
            app_logger.error(f"Error getting document IDs from Qdrant: {str(e)}")
            return []

    async def close(self):
        """
        Close the Qdrant client connection
        """
        try:
            await self.client.close()
            app_logger.info("Qdrant client connection closed")
        except Exception as e:
            app_logger.error(f"Error closing Qdrant client: {str(e)}")

# Initialize the service
qdrant_service = QdrantService()