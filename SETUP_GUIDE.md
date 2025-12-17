# Physical AI & Humanoid Robotics Textbook - Full Setup Guide

This project consists of a Docusaurus-based frontend book interface and a RAG (Retrieval Augmented Generation) backend chatbot system for the Physical AI textbook.

## Project Structure

```
physical-ai-textbook/
├── ai-textbook-web/          # Docusaurus frontend
│   ├── src/
│   │   ├── components/      # React components (including BookChatbot)
│   │   ├── services/        # Frontend services
│   │   └── pages/
│   ├── docs/                # Book content
│   ├── static/
│   └── docusaurus.config.ts # Frontend configuration
└── backend/                 # FastAPI backend
    ├── api/
    │   ├── routers/         # API routes (chat, ingest)
    │   └── services/        # Backend services (gemini, qdrant, db)
    ├── services/            # Core services
    ├── models/              # Data models
    ├── config.py            # Backend configuration
    └── start_server.py      # Server startup script
```

## Prerequisites

- Python 3.8+ with pip
- Node.js 18+ with npm
- Git

## Setup Instructions

### 1. Backend Setup (RAG Chatbot)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables by editing `.env`:
   ```bash
   # Add your API keys and configuration
   GEMINI_API_KEY=your_actual_api_key_here
   QDRANT_URL=your_qdrant_url_or_localhost
   QDRANT_API_KEY=your_qdrant_api_key
   DATABASE_URL=sqlite+aiosqlite:///./physical_ai_textbook.db
   ```

5. Start the backend server:
   ```bash
   python start_server.py
   ```
   The backend will be available at `http://127.0.0.1:8001`

### 2. Frontend Setup (Docusaurus Book)

1. Navigate to the frontend directory:
   ```bash
   cd ai-textbook-web
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure frontend environment by creating `.env`:
   ```bash
   # Frontend Configuration
   REACT_APP_BACKEND_URL=http://127.0.0.1:8001
   ```

4. Start the frontend server:
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000` (or first available port like 3001, 3002, etc.)

## Running the Full Project

### Option 1: Manual Start (Separate Terminals)

1. **Start Backend First**:
   ```bash
   cd backend
   python start_server.py
   ```

2. **In a new terminal, start Frontend**:
   ```bash
   cd ai-textbook-web
   npm start
   ```

### Option 2: Using Process Manager (Recommended)

Create a startup script to manage both servers:

**Windows (start_both.bat)**:
```batch
@echo off
start "Backend" cmd /k "cd backend && python start_server.py"
timeout /t 5 /nobreak >nul
start "Frontend" cmd /k "cd ai-textbook-web && npm start"
```

**Linux/macOS (start_both.sh)**:
```bash
#!/bin/bash
# Start backend in background
cd backend
python start_server.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 5

# Start frontend
cd ../ai-textbook-web
npm start

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
```

## API Endpoints

### Backend API (http://127.0.0.1:8001)
- `GET /` - Health check
- `GET /docs` - API Documentation (Swagger UI)
- `POST /api/v1/chat` - General chat with RAG
- `POST /api/v1/chat/selected-text` - Chat with selected text context
- `POST /api/v1/chat/completions` - ChatKit-compatible endpoint

### Frontend (http://localhost:3000 or similar)
- Book content is served from `/docs/`
- Chatbot is integrated as a floating component on all pages
- API calls are proxied through the frontend

## Configuration Notes

### Frontend Configuration
- The BookChatbot component uses `REACT_APP_BACKEND_URL` from `.env`
- The chatbot automatically detects selected text on the page
- Sessions are stored in localStorage for persistence

### Backend Configuration
- Uses SQLite database by default (`test.db`)
- Supports Qdrant vector database for RAG
- Integrates with Google Gemini for AI responses
- Supports both selected text and full document context modes

## Troubleshooting

### Common Issues

1. **Port Conflicts**: If ports 8001 or 3000 are in use:
   - Backend: Edit `start_server.py` to change port (default 8001)
   - Frontend: Use `npm start -- --port [available_port]`

2. **API Keys Missing**: Ensure all required API keys are in backend `.env`:
   - `GEMINI_API_KEY` - Required for AI responses
   - `QDRANT_URL` and `QDRANT_API_KEY` - Required for RAG functionality

3. **Database Issues**: The system uses SQLite by default. For production:
   - Update `DATABASE_URL` in `.env` to use PostgreSQL or other database
   - Run `python -c "from db.database import create_tables; import asyncio; asyncio.run(create_tables())"` to initialize tables

4. **CORS Issues**: Backend already configured for common frontend origins. If needed, add origins in `main.py` CORS middleware.

### Testing Integration

1. Verify backend is running: `curl http://127.0.0.1:8001/`
2. Verify API access: `curl http://127.0.0.1:8001/docs`
3. Check frontend console for API connection errors
4. Test chat functionality through the floating chatbot button

## Services Architecture

### Backend Services
- **gemini_service**: Handles AI model interactions and embeddings
- **qdrant_service**: Manages vector database operations for RAG
- **db_service**: Handles session and message persistence

### Frontend Components
- **BookChatbot**: Main chat interface component
- **chatbot-api.js**: Service layer for API communication
- **Root.jsx**: Global component integration

## Development Notes

- The frontend is built with Docusaurus v3 and React
- Backend uses FastAPI with async/await patterns
- RAG functionality retrieves context from ingested documents
- The system supports both general queries and selected-text-specific questions