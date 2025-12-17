#!/usr/bin/env python3
"""
Startup script for Physical AI Textbook RAG Backend
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

def start_server():
    """Start the FastAPI server"""
    print("Starting the application...")
    print("Visit http://localhost:8000/docs for API documentation")

    try:
        # Run uvicorn to start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start the server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        sys.exit(0)

def main():
    """Main function to run the startup process"""
    print("Starting Physical AI Textbook RAG Backend...")
    print()

    # Change to the script's directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    # Install requirements
    install_requirements()

    # Start the server
    start_server()

if __name__ == "__main__":
    main()