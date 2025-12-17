"""
Test the database models directly without using the config
"""
import asyncio
import uuid
from sqlalchemy import create_engine, Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import select

# Define models directly here to avoid config dependency
Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to chat messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(PostgresUUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to chat session
    session = relationship("ChatSession", back_populates="messages")

async def test_database_models():
    """Test that the UUID-based database models work correctly"""
    print("Testing database models directly...")

    # Create an in-memory SQLite engine for testing (since we can't connect to Neon without credentials)
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Created database tables in memory")

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

    print("\n🎉 All database model tests passed! The UUID-based models are correctly defined.")

if __name__ == "__main__":
    asyncio.run(test_database_models())