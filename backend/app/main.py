from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.chat import router as chat_router
from config import settings
from db.postgres import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Create database tables on startup
        await create_tables()
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise
    yield
    # Shutdown

app = FastAPI(
    title="Physical AI Textbook RAG Backend",
    description="RAG backend for Physical AI textbook using FastAPI, Qdrant, Cohere, and Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Physical AI Textbook RAG Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )