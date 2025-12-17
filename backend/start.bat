@echo off
REM Startup script for Physical AI Textbook RAG Backend

echo Starting Physical AI Textbook RAG Backend...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Starting the application...
echo Visit http://localhost:8000/docs for API documentation
echo.

REM Start the FastAPI application
uvicorn main:app --reload --host 0.0.0.0 --port 8000