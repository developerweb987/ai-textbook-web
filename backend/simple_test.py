"""
Simple test to verify the database models work correctly with UUIDs
"""
import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.db.models import ChatSession, ChatMessage, Base
from app.db.postgres import AsyncSessionLocal, engine

async def test_database_models():
    """Test that the UUID-based database models work correctly"""
    print("Testing database models...")

    # Create tables first
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Created database tables")

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

    # Test database operations
    async with AsyncSessionLocal() as db:
        # Create session
        new_session = ChatSession(id=session_id)
        db.add(new_session)
        await db.commit()

        print(f"✓ Created session in database with UUID: {new_session.id}")

        # Create messages
        user_message = ChatMessage(
            session_id=session_id,
            role="user",
            content="Hello, this is a test message"
        )
        assistant_message = ChatMessage(
            session_id=session_id,
            role="assistant",
            content="Hello, this is an assistant response"
        )

        db.add(user_message)
        db.add(assistant_message)
        await db.commit()

        print(f"✓ Created user message: {user_message.id}")
        print(f"✓ Created assistant message: {assistant_message.id}")

        # Retrieve the session and messages
        retrieved_session = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
        session_result = retrieved_session.scalar_one_or_none()
        assert session_result is not None
        assert session_result.id == session_id
        print(f"✓ Retrieved session from database: {session_result.id}")

        # Retrieve messages for the session
        retrieved_messages = await db.execute(select(ChatMessage).where(ChatMessage.session_id == session_id))
        messages = retrieved_messages.scalars().all()
        assert len(messages) == 2
        print(f"✓ Retrieved {len(messages)} messages for session")

        # Verify message roles
        roles = [msg.role for msg in messages]
        assert "user" in roles and "assistant" in roles
        print(f"✓ Messages have correct roles: {roles}")

    print("\n🎉 All database tests passed! The UUID-based models work correctly.")

if __name__ == "__main__":
    asyncio.run(test_database_models())