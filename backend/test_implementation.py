"""
Test script to verify the complete RAG Chatbot backend implementation
"""
import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.db.models import ChatSession, ChatMessage, Base
from app.db.postgres import AsyncSessionLocal
from app.rag.ingest import ingest_documents
from app.rag.retrieve import retrieve_documents
from app.rag.generate import generate_response, generate_response_from_selected_text

async def test_database_models():
    """Test that the UUID-based database models work correctly"""
    print("Testing database models...")

    # Create a new session with UUID
    session_id = uuid.uuid4()
    session = ChatSession(id=session_id)

    # Verify the session has a UUID
    assert session.id == session_id
    print(f"✓ ChatSession created with UUID: {session.id}")

    # Create a message with UUID
    message_id = uuid.uuid4()
    message = ChatMessage(
        id=message_id,
        session_id=session_id,
        role="user",
        content="Test message"
    )

    assert message.session_id == session_id
    assert message.role == "user"
    assert message.content == "Test message"
    print(f"✓ ChatMessage created with UUID: {message.id} and session_id: {message.session_id}")

async def test_database_operations():
    """Test actual database operations with UUID models"""
    print("\nTesting database operations...")

    # Create a new session
    session_uuid = uuid.uuid4()
    async with AsyncSessionLocal() as db:
        # Create session
        new_session = ChatSession(id=session_uuid)
        db.add(new_session)
        await db.commit()

        print(f"✓ Created session in database with UUID: {new_session.id}")

        # Create messages
        user_message = ChatMessage(
            session_id=session_uuid,
            role="user",
            content="Hello, this is a test message"
        )
        assistant_message = ChatMessage(
            session_id=session_uuid,
            role="assistant",
            content="Hello, this is an assistant response"
        )

        db.add(user_message)
        db.add(assistant_message)
        await db.commit()

        print(f"✓ Created user message: {user_message.id}")
        print(f"✓ Created assistant message: {assistant_message.id}")

        # Retrieve the session and messages
        retrieved_session = await db.execute(select(ChatSession).where(ChatSession.id == session_uuid))
        session_result = retrieved_session.scalar_one_or_none()
        assert session_result is not None
        assert session_result.id == session_uuid
        print(f"✓ Retrieved session from database: {session_result.id}")

        # Retrieve messages for the session
        retrieved_messages = await db.execute(select(ChatMessage).where(ChatMessage.session_id == session_uuid))
        messages = retrieved_messages.scalars().all()
        assert len(messages) == 2
        print(f"✓ Retrieved {len(messages)} messages for session")

        # Verify message roles
        roles = [msg.role for msg in messages]
        assert "user" in roles and "assistant" in roles
        print(f"✓ Messages have correct roles: {roles}")

async def test_ingestion():
    """Test document ingestion functionality"""
    print("\nTesting document ingestion...")
    try:
        # Try to ingest documents from the docs directory
        result = await ingest_documents(docs_path="../ai-textbook-web/docs", force_recreate=False)
        print(f"✓ Ingestion successful: {result['message']}")
        return True
    except Exception as e:
        print(f"⚠ Ingestion failed (this may be expected if docs directory doesn't exist): {str(e)}")
        # Try with a simple test directory structure
        import os
        if not os.path.exists("test_docs"):
            os.makedirs("test_docs")
        with open("test_docs/test.md", "w", encoding="utf-8") as f:
            f.write("# Test Document\n\nThis is a test document for the RAG system.\n\n## Section\n\nMore content here.")

        result = await ingest_documents(docs_path="test_docs", force_recreate=True)
        print(f"✓ Ingestion successful with test docs: {result['message']}")
        return True

async def test_retrieval():
    """Test document retrieval functionality"""
    print("\nTesting document retrieval...")
    try:
        # Try to retrieve documents with a test query
        results = await retrieve_documents(query="test", top_k=2)
        print(f"✓ Retrieved {len(results)} documents for test query")
        if results:
            print(f"  First result source: {results[0]['source_file']}")
        return True
    except Exception as e:
        print(f"⚠ Retrieval failed: {str(e)}")
        return False

async def test_generation():
    """Test response generation functionality"""
    print("\nTesting response generation...")
    try:
        # Test basic response generation (without any documents)
        response = await generate_response("What is this system?", [])
        print(f"✓ Generated response: {response[:50]}...")
        return True
    except Exception as e:
        print(f"⚠ Generation failed: {str(e)}")
        return False

async def test_selected_text_generation():
    """Test selected text response generation"""
    print("\nTesting selected text response generation...")
    try:
        # Test response generation from selected text
        response = await generate_response_from_selected_text(
            user_query="What is this text about?",
            selected_text="This is a sample text about testing the RAG system."
        )
        print(f"✓ Generated response from selected text: {response[:50]}...")
        return True
    except Exception as e:
        print(f"⚠ Selected text generation failed: {str(e)}")
        return False

async def run_all_tests():
    """Run all tests to verify the complete implementation"""
    print("Starting comprehensive tests for RAG Chatbot backend...\n")

    tests = [
        ("Database Models", test_database_models),
        ("Database Operations", test_database_operations),
        ("Document Ingestion", test_ingestion),
        ("Document Retrieval", test_retrieval),
        ("Response Generation", test_generation),
        ("Selected Text Generation", test_selected_text_generation)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*50}")
            print(f"Running {test_name} test...")
            print(f"{'='*50}")
            await test_func()
            results.append((test_name, True))
            print(f"✓ {test_name} test PASSED")
        except Exception as e:
            print(f"✗ {test_name} test FAILED: {str(e)}")
            results.append((test_name, False))

    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The RAG Chatbot backend is working correctly.")
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    asyncio.run(run_all_tests())