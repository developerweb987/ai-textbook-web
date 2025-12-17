# PowerShell script to set up the Physical AI Textbook RAG Backend on Windows
# Usage: Run this script from the backend directory in PowerShell as Administrator if needed

Write-Host "Setting up Physical AI Textbook RAG Backend on Windows..." -ForegroundColor Green

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python not found. Please install Python 3.9-3.12 from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
} else {
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
}

# Check Python version compatibility
$version = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
[int]$major = [int]$version.Split('.')[0]
[int]$minor = [int]$version.Split('.')[1]

if ($major -ne 3 -or $minor -lt 9 -or $minor -gt 12) {
    Write-Host "Warning: Python 3.9-3.12 is recommended. Current version: $version" -ForegroundColor Yellow
    Write-Host "Python 3.13 may cause compatibility issues with some packages." -ForegroundColor Yellow
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$env:PYTHONPATH = "$PWD"
& "$PWD\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to upgrade pip" -ForegroundColor Red
    exit 1
}

# Install packages from requirements.txt
Write-Host "Installing packages from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install packages from requirements.txt" -ForegroundColor Red
    Write-Host "Trying to install with --no-cache-dir flag..." -ForegroundColor Yellow
    pip install --no-cache-dir -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Still failed to install packages. Trying individual installations..." -ForegroundColor Yellow

        # Install core packages first
        $corePackages = @("fastapi", "uvicorn[standard]", "qdrant-client", "google-generativeai", "sqlalchemy", "python-dotenv", "pydantic", "langchain", "langchain-community", "langchain-google-genai")
        foreach ($package in $corePackages) {
            Write-Host "Installing $package..." -ForegroundColor Yellow
            pip install $package
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Failed to install $package" -ForegroundColor Red
            }
        }
    }
}

# Verify installations
Write-Host "Verifying package installations..." -ForegroundColor Yellow

$packagesToCheck = @("fastapi", "uvicorn", "langchain", "qdrant-client", "sqlalchemy", "pydantic")

foreach ($package in $packagesToCheck) {
    $result = python -c "import $package; print('✓ $package imported successfully')"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $package imported successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to import $package" -ForegroundColor Red
    }
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    @"
# Physical AI Textbook RAG Backend Configuration
QDRANT_URL=http://localhost:6333
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/physical_ai_textbook
DOCS_PATH=./docs
LOG_LEVEL=INFO
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "Created .env file. Please update it with your actual API keys and database configuration." -ForegroundColor Yellow
}

# Create docs directory if it doesn't exist
if (-not (Test-Path "docs")) {
    Write-Host "Creating docs directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "docs" -Force | Out-Null
    Write-Host "Created docs directory. Place your documents here for ingestion." -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the backend:" -ForegroundColor Yellow
Write-Host "1. Make sure your virtual environment is activated:" -ForegroundColor White
Write-Host "   & 'backend\venv\Scripts\Activate.ps1'" -ForegroundColor Cyan
Write-Host "2. Run the application:" -ForegroundColor White
Write-Host "   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload" -ForegroundColor Cyan
Write-Host ""
Write-Host "The API will be available at: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "API documentation will be available at: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "To test the endpoints:" -ForegroundColor Yellow
Write-Host "1. Ingest documents: POST http://127.0.0.1:8000/api/v1/ingest" -ForegroundColor White
Write-Host "2. Chat endpoint: POST http://127.0.0.1:8000/api/v1/chat" -ForegroundColor White
Write-Host "3. Selected text chat: POST http://127.0.0.1:8000/api/v1/chat/selected-text" -ForegroundColor White
Write-Host ""