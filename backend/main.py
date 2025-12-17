from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from api.routers.chat import router as chat_router
from api.routers.ingest import router as ingest_router
from config import settings
from db.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Create database tables on startup - this is the only blocking call allowed
        await create_tables()
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise
    yield
    # Shutdown

app = FastAPI(
    title="Physical AI Textbook RAG Backend",
    description="RAG backend for Physical AI textbook using FastAPI, Qdrant, and Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware - this should be added before including routers
# Parse CORS origins from config, split by comma, and filter out empty strings
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(ingest_router, prefix="/api/v1", tags=["ingest"])

@app.get("/")
async def root():
    return {"message": "Physical AI Textbook RAG Backend"}

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