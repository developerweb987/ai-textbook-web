# Physical AI Textbook - Full Stack Setup Guide

This guide provides complete instructions for setting up the Physical AI Textbook frontend (Docusaurus) and backend (FastAPI RAG chatbot) on Windows.

## Prerequisites

- **Node.js** (v20 or higher) - Download from [nodejs.org](https://nodejs.org/)
- **Python** (v3.10 or higher) - Download from [python.org](https://python.org/)
- **Git** - Download from [git-scm.com](https://git-scm.com/)
- **Windows Terminal** or **Command Prompt** with PowerShell

## Backend Setup (FastAPI RAG Chatbot)

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```env
# Google API Key for Gemini
GEMINI_API_KEY=your_api_key_here

# Database configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost/physical_ai_textbook

# Qdrant configuration
QDRANT_URL=http://localhost:6333

# Documents path for RAG
DOCS_PATH=../ai-textbook-web/docs
```

### 3. Install and Start Qdrant (Vector Database)

Option 1: Using Docker
```bash
docker run -d --name qdrant-container -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

Option 2: Using pip
```bash
pip install qdrant-client
# Then run: python -m qdrant_client.local --path ./qdrant_data
```

### 4. Install and Start PostgreSQL

Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)

### 5. Start the Backend Server

```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`

## Frontend Setup (Docusaurus)

### 1. Install Node.js Dependencies

```bash
cd ai-textbook-web
npm install
```

### 2. Set Up Environment Variables

The `.env` file is already created with:
```
REACT_APP_BACKEND_URL=http://localhost:8000
```

### 3. Start the Frontend

```bash
cd ai-textbook-web
npm start
```

The frontend will start on `http://localhost:3000`

## Complete Setup Commands for Windows

### Option 1: Using Command Prompt

```cmd
# Clone the repository (if not already done)
git clone https://github.com/your-username/physical-ai-textbook.git
cd physical-ai-textbook

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Start backend in a new terminal
start cmd /k "cd /d %cd% && python main.py"

# Install frontend dependencies
cd ../ai-textbook-web
npm install

# Start frontend
npm start
```

### Option 2: Using PowerShell

```powershell
# Navigate to project directory
Set-Location -Path "D:\physical-ai-textbook"

# Install backend dependencies
Set-Location -Path ".\backend"
pip install -r requirements.txt

# Start backend in a new PowerShell window
Start-Process powershell -ArgumentList "-Command", "Set-Location -Path '$(Get-Location)'; python main.py"

# Install frontend dependencies
Set-Location -Path "..\ai-textbook-web"
npm install

# Start frontend
npm start
```

## Troubleshooting

### Common Issues:

1. **Blank Page on Frontend**:
   - Check that the backend is running on `http://localhost:8000`
   - Verify CORS settings in `backend/main.py`
   - Check browser console for errors

2. **Backend Connection Issues**:
   - Ensure `REACT_APP_BACKEND_URL` is set correctly in `.env`
   - Verify that both services are running on their respective ports
   - Check firewall settings if running on Windows

3. **Python Dependencies**:
   - Use virtual environment: `python -m venv venv && venv\Scripts\activate`
   - Upgrade pip: `python -m pip install --upgrade pip`

4. **Node.js Issues**:
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### Windows-Specific Issues:

1. **Execution Policy** (PowerShell):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Long Path Issues**:
   - Enable long path support in Windows settings
   - Or use Git Bash for development

## Verification

1. Backend should be accessible at: `http://localhost:8000`
2. Frontend should be accessible at: `http://localhost:3000`
3. Chatbot should appear as a floating button on the frontend
4. Selected text functionality should work when highlighting text and asking questions

## Running in Production

For production deployment:

1. Update CORS settings in `backend/main.py` to specific origins
2. Use environment variables for sensitive data
3. Set up proper reverse proxy (nginx, Apache)
4. Use process managers like PM2 for Node.js and Gunicorn for Python

## Additional Notes

- The chatbot is integrated into all pages via the `Root.jsx` component
- Selected text functionality works by highlighting text and then opening the chatbot
- RAG (Retrieval Augmented Generation) uses Qdrant vector database and Gemini AI
- All chat sessions are stored in PostgreSQL for persistence