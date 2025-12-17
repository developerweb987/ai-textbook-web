from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from api.routers.chat import router as chat_router
from api.routers.ingest import router as ingest_router
from config import settings
from db.database import create_tables
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Create database tables on startup - this is the only blocking call allowed
        logger.info("Initializing database tables...")
        await create_tables()
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    yield
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title="Physical AI Textbook RAG Backend",
    description="RAG backend for Physical AI textbook using FastAPI, Qdrant, and Gemini",
    version="1.0.0",
    lifespan=lifespan,
    # Add additional configuration for serverless environments
    debug=False  # Will be set via environment in production
)

# Add CORS middleware - this should be added before including routers
# Parse CORS origins from config, split by comma, and filter out empty strings
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
logger.info(f"Configuring CORS for origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
    # Additional options for production
    allow_origin_regex=None,  # We're using specific origins instead
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(ingest_router, prefix="/api/v1", tags=["ingest"])

@app.get("/")
async def root():
    return {"message": "Physical AI Textbook RAG Backend", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Vercel and other deployment platforms"""
    return {"status": "healthy", "message": "Backend is running"}

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)  # No content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )