# Physical AI Textbook RAG Backend

This is a production-ready RAG (Retrieval Augmented Generation) backend built with FastAPI for the Physical AI textbook project.

## Architecture

The backend consists of the following components:

1. **FastAPI Application**: Main web server with API endpoints
2. **Qdrant Vector Store**: Stores document embeddings for similarity search
3. **PostgreSQL Database**: Stores chat sessions and messages
4. **Google Gemini**: Generates answers using the embedding and generation models
5. **Markdown Processor**: Reads and chunks markdown files

## Requirements

- Python 3.8+
- API keys for:
  - Google Gemini
  - Qdrant Cloud or self-hosted Qdrant
  - PostgreSQL database (Neon or other)

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Database settings
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database_name  # Alternative to NEON_DATABASE_URL
NEON_DATABASE_URL=your_neon_database_url_here  # For Neon Serverless Postgres

DB_POOL_SIZE=5
DB_POOL_TIMEOUT=30

# Qdrant settings
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_cloud_url  # For Qdrant Cloud (e.g., https://your-cluster.us-east4-0.gcp.cloud.qdrant.io)
QDRANT_HOST=your_qdrant_host     # For self-hosted Qdrant (when not using QDRANT_URL)
QDRANT_PORT=6333                 # For self-hosted Qdrant (when not using QDRANT_URL)
COLLECTION_NAME=documents

# Google Generative AI settings
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash

# Frontend docs path
DOCS_PATH=../ai-textbook-web/docs

# Chunking settings
CHUNK_SIZE_TOKENS=700
```

## API Endpoints

### Ingestion Endpoints

#### POST `/api/v1/ingest`
Ingest documents from the docs directory and store embeddings in Qdrant.

Request body:
```json
{
  "force_recreate": false,
  "docs_path": "../ai-textbook-web/docs"
}
```

Response:
```json
{
  "message": "Successfully ingested 10 document chunks",
  "documents_processed": 2,
  "chunks_created": 10
}
```

### Chat Endpoints

#### POST `/api/v1/chat`
Chat endpoint that uses RAG to answer questions based on ingested documents.

Request body:
```json
{
  "message": "What is physical AI?",
  "session_id": "session-123"
}
```

Response:
```json
{
  "role": "assistant",
  "content": "Physical AI is..."
}
```

#### POST `/api/v1/chat/selected-text`
Chat endpoint that answers questions based only on the selected/highlighted text.

Request body:
```json
{
  "message": "Explain this concept?",
  "selected_text": "Physical AI is a field that combines robotics...",
  "session_id": "session-123"
}
```

Response:
```json
{
  "role": "assistant",
  "content": "Based on the selected text..."
}
```

## Running the Application

### Development (Windows)

For Windows users, we recommend using the setup script:

1. Open PowerShell in the `backend` directory
2. Run the Windows setup script:
```powershell
.\setup_windows.ps1
```

Or run manually:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The application will be available at `http://127.0.0.1:8000`

### Development (Linux/Mac)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file

3. Run the application:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

### Production

#### Using Python script:
```bash
cd backend
python start_prod.py
```

#### Using Docker:
```bash
cd backend
docker build -t textbook-rag-backend .
docker run -p 8000:8000 textbook-rag-backend
```

#### Using Docker Compose:
```bash
cd backend
docker-compose up -d
```

## Example Usage

### Ingest Documents
```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{"docs_path": "../ai-textbook-web/docs"}'
```

### Chat with RAG
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the main concept of physical AI?", "session_id": "my-session"}'
```

### Chat with Selected Text
```bash
curl -X POST http://localhost:8000/api/v1/chat/selected-text \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain this", "selected_text": "Physical AI combines robotics with AI...", "session_id": "my-session"}'
```

## Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration and environment variables
├── api/
│   └── chat.py                # Chat endpoints
├── rag/
│   ├── ingest.py              # Document ingestion and embedding
│   ├── retrieve.py            # Document retrieval from vector store
│   └── generate.py            # Response generation with Gemini
├── db/
│   ├── postgres.py            # Postgres database operations
│   └── models.py              # Database models
├── start.py                   # Development startup script
├── start_prod.py              # Production startup script
├── start_server.py            # Windows-compatible startup script
├── setup_windows.ps1          # Windows PowerShell setup script
├── setup_windows.bat          # Windows batch setup script
├── SETUP_WINDOWS.md           # Windows setup guide
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables template
```

## Windows-Specific Files

- `setup_windows.ps1`: PowerShell script to automatically set up the environment on Windows
- `setup_windows.bat`: Batch script alternative for Windows setup
- `start_server.py`: Windows-compatible startup script with proper path handling
- `SETUP_WINDOWS.md`: Detailed Windows setup guide with troubleshooting