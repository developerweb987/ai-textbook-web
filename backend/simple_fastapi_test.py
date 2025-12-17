from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application startup complete")
    yield
    # Shutdown
    print("Application shutdown complete")

app = FastAPI(
    title="Test Backend",
    description="Simple test backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World - Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "simple_fastapi_test:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )