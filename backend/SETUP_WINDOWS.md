# Physical AI Textbook RAG Backend - Windows Setup Guide

This guide provides step-by-step instructions to fix common backend setup and runtime issues for the FastAPI RAG Chatbot project on Windows.

## Common Issues Fixed

1. `ModuleNotFoundError: No module named 'langchain'`
2. `ModuleNotFoundError: No module named 'app'`
3. `Fatal Python error: init_sys_streams`

## Prerequisites

- Python 3.9-3.12 (Python 3.13 may cause compatibility issues)
- Windows PowerShell or Command Prompt
- Git for Windows (if cloning from repository)

## Step-by-Step Setup

### Method 1: Using PowerShell Script (Recommended)

1. Open PowerShell as Administrator in the `backend` directory
2. Run the setup script:
   ```powershell
   .\setup_windows.ps1
   ```

### Method 2: Manual Setup

1. **Navigate to the backend directory:**
   ```powershell
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Upgrade pip:**
   ```powershell
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```powershell
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

### Method 3: Using Command Prompt

1. **Navigate to the backend directory:**
   ```cmd
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```

3. **Upgrade pip:**
   ```cmd
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```cmd
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

## Alternative Start Methods

### Using the Python Start Script

After setup, you can also use the provided start script:

```powershell
python start_server.py
```

### Using the Batch Script

```cmd
.\setup_windows.bat
```

## Configuration

1. **Create/update the `.env` file** with your configuration:
   ```
   QDRANT_URL=http://localhost:6333
   GEMINI_API_KEY=your_api_key_here
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/physical_ai_textbook
   DOCS_PATH=./docs
   LOG_LEVEL=INFO
   ```

2. **Ensure your documents are in the `docs/` directory** for ingestion.

## API Endpoints

Once the server is running, you can access:

- **Root**: `http://127.0.0.1:8000`
- **API Documentation**: `http://127.0.0.1:8000/docs`
- **Ingest Endpoint**: `POST http://127.0.0.1:8000/api/v1/ingest`
- **Chat Endpoint**: `POST http://127.0.0.1:8000/api/v1/chat`
- **Selected Text Chat**: `POST http://127.0.0.1:8000/api/v1/chat/selected-text`

## Troubleshooting

### If you encounter `ModuleNotFoundError`:
- Ensure virtual environment is activated
- Verify all `__init__.py` files exist in directories (they are created automatically by setup scripts)
- Check that PYTHONPATH includes the backend directory

### If you encounter Python 3.13 compatibility issues:
- Downgrade to Python 3.9-3.12
- Some packages may not be fully compatible with Python 3.13 yet

### If uvicorn fails to start:
- Make sure you're running from the backend directory
- Ensure the virtual environment is activated
- Check that all dependencies are installed

## Dependencies Included

The `requirements.txt` file includes:
- fastapi
- uvicorn[standard]
- qdrant-client
- google-generativeai
- sqlalchemy
- python-dotenv
- pydantic
- langchain
- langchain-community
- langchain-google-genai
- psycopg2-binary
- httpx
- cohere
- sentence-transformers
- unstructured

## Notes

- The setup automatically creates missing `__init__.py` files for proper Python module recognition
- The server runs on `localhost:8000` (accessible as `127.0.0.1:8000`)
- All scripts are designed specifically for Windows compatibility
- For production deployment, adjust security settings (CORS, authentication, etc.)