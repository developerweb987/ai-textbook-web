from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from rag.ingest import ingest_documents
from rag.retrieve import retrieve_documents
from rag.generate import generate_response, generate_response_from_selected_text
from db.postgres import get_db_session
from db.models import ChatSession, ChatMessage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config import settings
from mangum import Mangum  # Vercel serverless adapter

# --------------------------
# Step 1: FastAPI App + CORS
# --------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-textbook-web.vercel.app"],  # Replace with actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Step 2: Router
# --------------------------
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
    try:
        session_id = request.session_id or str(uuid.uuid4())
        retrieved_docs = await retrieve_documents(request.message, top_k=5)
        response_text = await generate_response(request.message, retrieved_docs)

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

        return {"role": "assistant", "content": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")

@router.post("/chat/selected-text")
async def chat_selected_text(request: SelectedTextChatRequest, db: AsyncSession = Depends(get_db_session)):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        response_text = await generate_response_from_selected_text(request.message, request.selected_text)

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

        return {"role": "assistant", "content": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during selected text chat: {str(e)}")

# --------------------------
# Step 3: Include Router & Mangum
# --------------------------
app.include_router(router, prefix="/api/v1")

handler = Mangum(app)  # Serverless adapter for Vercel
