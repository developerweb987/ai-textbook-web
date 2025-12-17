@echo off
REM Batch script to set up the Physical AI Textbook RAG Backend on Windows
REM Usage: Run this script from the backend directory in Command Prompt as Administrator if needed

echo Setting up Physical AI Textbook RAG Backend on Windows...

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.9-3.12 from https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
    echo Python found: %python_version%
)

REM Check Python version compatibility
for /f "tokens=1,2 delims=." %%a in ("%python_version%") do (
    set major=%%a
    set minor=%%b
)
if "%major%" neq "3" (
    echo Warning: Python 3 is required.
    pause
    exit /b 1
)
if %minor% lss 9 (
    echo Warning: Python 3.9 or higher is recommended. Current version: %python_version%
    echo Python 3.13 may cause compatibility issues with some packages.
)
if %minor% gtr 12 (
    echo Warning: Python 3.12 or lower is recommended. Current version: %python_version%
    echo Python 3.13 may cause compatibility issues with some packages.
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip
    pause
    exit /b 1
)

REM Install packages from requirements.txt
echo Installing packages from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install packages from requirements.txt
    echo Trying to install with --no-cache-dir flag...
    pip install --no-cache-dir -r requirements.txt
    if errorlevel 1 (
        echo Still failed to install packages. Trying individual installations...
        REM Install core packages first
        pip install fastapi uvicorn[standard] qdrant-client google-generativeai sqlalchemy python-dotenv pydantic langchain langchain-community langchain-google-genai
    )
)

REM Verify installations
echo Verifying package installations...
python -c "import fastapi; print('✓ fastapi imported successfully')" 2>nul
if errorlevel 1 (echo ✗ Failed to import fastapi)
python -c "import uvicorn; print('✓ uvicorn imported successfully')" 2>nul
if errorlevel 1 (echo ✗ Failed to import uvicorn)
python -c "import langchain; print('✓ langchain imported successfully')" 2>nul
if errorlevel 1 (echo ✗ Failed to import langchain)
python -c "import qdrant_client; print('✓ qdrant-client imported successfully')" 2>nul
if errorlevel 1 (echo ✗ Failed to import qdrant-client)
python -c "import sqlalchemy; print('✓ sqlalchemy imported successfully')" 2>nul
if errorlevel 1 (echo ✗ Failed to import sqlalchemy)
python -c "import pydantic; print('✓ pydantic imported successfully')" 2>nul
if errorlevel 1 (echo ✗ Failed to import pydantic)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    echo # Physical AI Textbook RAG Backend Configuration > .env
    echo QDRANT_URL=http://localhost:6333 >> .env
    echo GEMINI_API_KEY=your_api_key_here >> .env
    echo DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/physical_ai_textbook >> .env
    echo DOCS_PATH=./docs >> .env
    echo LOG_LEVEL=INFO >> .env
    echo Created .env file. Please update it with your actual API keys and database configuration.
)

REM Create docs directory if it doesn't exist
if not exist "docs" (
    echo Creating docs directory...
    mkdir docs
    echo Created docs directory. Place your documents here for ingestion.
)

echo.
echo Setup completed successfully!
echo.
echo To run the backend:
echo 1. Make sure your virtual environment is activated:
echo    call venv\Scripts\activate.bat
echo 2. Run the application:
echo    python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
echo.
echo The API will be available at: http://127.0.0.1:8000
echo API documentation will be available at: http://127.0.0.1:8000/docs
echo.
echo To test the endpoints:
echo 1. Ingest documents: POST http://127.0.0.1:8000/api/v1/ingest
echo 2. Chat endpoint: POST http://127.0.0.1:8000/api/v1/chat
echo 3. Selected text chat: POST http://127.0.0.1:8000/api/v1/chat/selected-text
echo.
pause