import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    NEON_DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_POOL_TIMEOUT: int = 30

    # Qdrant settings
    QDRANT_URL: str
    QDRANT_API_KEY: str
    COLLECTION_NAME: str = "documents"

    # API Keys
    GEMINI_API_KEY: str
    COHERE_API_KEY: str
    GEMINI_MODEL: str = 'gemini-1.5-flash'

    # Frontend docs path
    DOCS_PATH: str = "../ai-textbook-web/docs"

    # Chunking settings
    CHUNK_SIZE_TOKENS: int = 700

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

settings = Settings()