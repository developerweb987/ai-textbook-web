from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
from rag.ingest import ingest_documents
from rag.retrieve import retrieve_documents
from rag.generate import generate_response, generate_response_from_selected_text
from db.postgres import get_db_session
from db.models import ChatSession, ChatMessage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config import settings

router = APIRouter()

class IngestRequest(BaseModel):
    force_recreate: bool = False
    docs_path: Optional[str] = None

class IngestResponse(BaseModel):
    message: str
    documents_processed: int
    chunks_created: int

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class SelectedTextChatRequest(BaseModel):
    message: str
    selected_text: str
    session_id: Optional[str] = None

@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    """
    Ingest documents from the docs directory and store embeddings in Qdrant
    """
    try:
        docs_path = request.docs_path or settings.DOCS_PATH
        result = await ingest_documents(docs_path, request.force_recreate)
        return IngestResponse(
            message=result["message"],
            documents_processed=result["documents_processed"],
            chunks_created=result["chunks_created"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during ingestion: {str(e)}")

@router.post("/chat")
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db_session)):
    """
    Chat endpoint that uses RAG to answer questions based on ingested documents
    Returns JSON compatible with ChatKit format
    """
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())

        # 1. Retrieve relevant documents (top 5 chunks)
        retrieved_docs = await retrieve_documents(request.message, top_k=5)

        # 2. Generate response using the RAG system
        response_text = await generate_response(request.message, retrieved_docs)

        # 5. Store messages in database
        session = await db.execute(select(ChatSession).filter(ChatSession.session_id == session_id))
        session_obj = session.scalar_one_or_none()
        if not session_obj:
            session_obj = ChatSession(session_id=session_id)
            db.add(session_obj)

        user_message = ChatMessage(session_id=session_id, role="user", content=request.message)
        assistant_message = ChatMessage(session_id=session_id, role="assistant", content=response_text)

        db.add(user_message)
        db.add(assistant_message)
        await db.commit()

        # 6. Return JSON compatible with ChatKit format
        return {
            "role": "assistant",
            "content": response_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")

@router.post("/chat/selected-text")
async def chat_selected_text(request: SelectedTextChatRequest, db: AsyncSession = Depends(get_db_session)):
    """
    Chat endpoint that answers questions based only on the selected/highlighted text
    """
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())

        # Generate response using only the selected text
        response_text = await generate_response_from_selected_text(request.message, request.selected_text)

        # Store messages in database
        session = await db.execute(select(ChatSession).filter(ChatSession.session_id == session_id))
        session_obj = session.scalar_one_or_none()
        if not session_obj:
            session_obj = ChatSession(session_id=session_id)
            db.add(session_obj)

        user_message = ChatMessage(
            session_id=session_id,
            role="user",
            content=f"Question: {request.message}\nSelected text: {request.selected_text}"
        )
        assistant_message = ChatMessage(session_id=session_id, role="assistant", content=response_text)

        db.add(user_message)
        db.add(assistant_message)
        await db.commit()

        return {
            "role": "assistant",
            "content": response_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during selected text chat: {str(e)}")