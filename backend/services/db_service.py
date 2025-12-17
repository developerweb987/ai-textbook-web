from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, select, func
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
from config import settings
from utils.logger import db_logger
from db.database import AsyncSessionLocal, engine

# Use the same Base from the main database module
from db.models import Base, ChatSession as DbChatSession, ChatMessage as DbChatMessage

# Service class to handle database operations
class DatabaseService:
    @staticmethod
    async def create_session(session_id: str, title: str = None):
        """Create a new chat session"""
        try:
            db_logger.info(f"Creating new session: {session_id} with title: {title}")

            async with AsyncSessionLocal() as session:
                # Create the session object with required fields first
                new_session = DbChatSession(session_id=session_id)

                # Set title separately if the model supports it
                if hasattr(new_session, 'title'):
                    new_session.title = title
                else:
                    # If title attribute doesn't exist, try to create without it
                    # This shouldn't happen with our updated model, but just in case
                    new_session = DbChatSession(session_id=session_id)
                    if hasattr(new_session, 'title'):
                        new_session.title = title

                session.add(new_session)
                await session.commit()
                await session.refresh(new_session)
                db_logger.debug(f"Session created: {session_id}")
                return new_session
        except Exception as e:
            db_logger.error(f"Error creating session {session_id}: {str(e)}")
            raise

    @staticmethod
    async def add_message(session_id: str, role: str, content: str):
        """Add a message to a chat session"""
        try:
            db_logger.debug(f"Adding message to session {session_id}, role: {role}")
            async with AsyncSessionLocal() as session:
                # Get the session ID from the session table
                result = await session.execute(
                    select(DbChatSession).where(DbChatSession.session_id == session_id)
                )
                db_session = result.scalar_one_or_none()

                if not db_session:
                    # Create a new session if it doesn't exist
                    db_logger.info(f"Creating new session for {session_id}")
                    db_session = await DatabaseService.create_session(session_id)

                new_message = DbChatMessage(
                    session_id=db_session.session_id,  # Use the session_id string, not the object ID
                    role=role,
                    content=content
                )
                session.add(new_message)
                await session.commit()
                await session.refresh(new_message)
                db_logger.debug(f"Message added to session {session_id}")
                return new_message
        except Exception as e:
            db_logger.error(f"Error adding message to session {session_id}: {str(e)}")
            raise

    @staticmethod
    async def get_messages_by_session(session_id: str, limit: int = 50):
        """Get messages from a specific session"""
        try:
            db_logger.debug(f"Getting messages for session {session_id}, limit: {limit}")
            async with AsyncSessionLocal() as session:
                # Get the session ID from the session table
                result = await session.execute(
                    select(DbChatSession).where(DbChatSession.session_id == session_id)
                )
                db_session = result.scalar_one_or_none()

                if not db_session:
                    db_logger.warning(f"Session {session_id} not found")
                    return []

                messages_result = await session.execute(
                    select(DbChatMessage)
                    .where(DbChatMessage.session_id == session_id)  # Use session_id to match
                    .order_by(DbChatMessage.created_at.asc())
                    .limit(limit)
                )
                messages = messages_result.scalars().all()
                db_logger.debug(f"Retrieved {len(messages)} messages for session {session_id}")
                return messages
        except Exception as e:
            db_logger.error(f"Error getting messages for session {session_id}: {str(e)}")
            raise

    @staticmethod
    async def get_recent_sessions(limit: int = 10):
        """Get recent chat sessions"""
        try:
            db_logger.debug(f"Getting recent sessions, limit: {limit}")
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(DbChatSession)
                    .order_by(DbChatSession.updated_at.desc())
                    .limit(limit)
                )
                sessions = result.scalars().all()
                db_logger.debug(f"Retrieved {len(sessions)} recent sessions")
                return sessions
        except Exception as e:
            db_logger.error(f"Error getting recent sessions: {str(e)}")
            raise

# Initialize the service
db_service = DatabaseService()