#!/usr/bin/env python3
"""
Debug script to test the exact same code path as the API
"""
import sys
import os
import asyncio

# Add backend to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the exact same services as used in the API
from services.db_service import DatabaseService

async def test_create_session():
    print("Testing DatabaseService.create_session...")

    try:
        # Test creating a session with title (the way it's called in add_message)
        session_id = "test-session-123"
        session = await DatabaseService.create_session(session_id, title="Test Chat")
        print(f"SUCCESS: Created session: {session.session_id}, title: {session.title}")
        return True
    except Exception as e:
        print(f"ERROR creating session: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_add_message():
    print("\\nTesting DatabaseService.add_message...")

    try:
        # Test adding a message which should trigger session creation if not exists
        session_id = "test-session-456"
        await DatabaseService.add_message(session_id, "user", "Hello, this is a test message")
        print(f"SUCCESS: Added message to session: {session_id}")
        return True
    except Exception as e:
        print(f"ERROR adding message: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("Running database service tests...\\n")

    success1 = await test_create_session()
    success2 = await test_add_message()

    if success1 and success2:
        print("\\nAll tests passed!")
    else:
        print("\\nSome tests failed!")

if __name__ == "__main__":
    asyncio.run(main())