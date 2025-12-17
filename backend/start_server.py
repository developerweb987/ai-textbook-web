import os
import sys
import subprocess
import threading
import time
import logging
from pathlib import Path

# Add the backend directory to Python path to fix module import issues
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'qdrant-client',
        'google-generativeai',
        'sqlalchemy',
        'python-dotenv',
        'pydantic',
        'langchain',
        'langchain-community',
        'langchain-google-genai'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        logger.warning(f"Missing packages: {missing_packages}")
        logger.info("Installing missing packages...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logger.info(f"Successfully installed {package}")
            except subprocess.CalledProcessError:
                logger.error(f"Failed to install {package}")
                return False
    else:
        logger.info("All required packages are already installed")

    return True

def ensure_directories():
    """Ensure required directories exist"""
    required_dirs = ['logs', 'docs', 'config']
    for directory in required_dirs:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

def ensure_init_files():
    """Ensure __init__.py files exist in all required directories"""
    init_dirs = [
        'api',
        'api/models',
        'api/rag',
        'api/routers',
        'api/services',
        'app',
        'app/api',
        'app/db',
        'app/rag',
        'config',
        'db',
        'rag',
        'services',
        'utils'
    ]

    for directory in init_dirs:
        init_path = Path('backend') / directory / '__init__.py'
        if not init_path.exists():
            init_path.parent.mkdir(parents=True, exist_ok=True)
            init_path.touch()
            logger.info(f"Created __init__.py file: {init_path}")

def ensure_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path('.env')
    if not env_path.exists():
        env_content = """# Physical AI Textbook RAG Backend Configuration
QDRANT_URL=http://localhost:6333
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/physical_ai_textbook
DOCS_PATH=./docs
LOG_LEVEL=INFO
"""
        env_path.write_text(env_content)
        logger.info("Created .env file with default configuration")

def run_backend():
    """Run the backend server"""
    try:
        import uvicorn
        from main import app

        logger.info("Starting FastAPI server...")
        logger.info("Server will be available at http://127.0.0.1:8001")
        logger.info("API documentation will be available at http://127.0.0.1:8001/docs")

        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8001,  # Changed to port 8001 to avoid conflicts
            reload=True,
            log_level="info"
        )
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.info("Please run setup script first to install dependencies")
    except Exception as e:
        logger.error(f"Error running backend: {e}")

def main():
    """Main function to start the backend"""
    logger.info("Starting Physical AI Textbook RAG Backend setup...")

    # Ensure all required files and directories exist
    ensure_directories()
    ensure_init_files()
    ensure_env_file()

    # Check and install dependencies
    if not check_and_install_dependencies():
        logger.error("Failed to install required dependencies")
        return

    # Run the backend
    run_backend()

if __name__ == "__main__":
    main()