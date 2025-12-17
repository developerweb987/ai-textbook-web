from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.chat import router as chat_router
from config import settings
from db.postgres import create_tables

# Lifespan context for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        print("Starting backend... Creating database tables if not exist.")
        await create_tables()
        print("Database tables ready.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise
    yield
    # Shutdown
    print("Shutting down backend...")

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Textbook RAG Backend",
    description="RAG backend for Physical AI textbook using FastAPI, Qdrant, Cohere, and Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
# Replace "https://your-frontend.vercel.app" with your actual deployed frontend URL
origins = [
    "https://ai-textbook-web.vercel.app",
    "http://localhost:3000",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat API router
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Physical AI Textbook RAG Backend is running."}

# Run locally (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
