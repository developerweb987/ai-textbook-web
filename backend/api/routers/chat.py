from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
import uuid
from services.gemini_service import gemini_service
from services.qdrant_service import qdrant_service
from services.db_service import db_service
from config import settings
from utils.logger import api_logger

router = APIRouter()



class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class SelectedTextChatRequest(BaseModel):
    message: str
    selected_text: str
    session_id: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str

class ChatKitRequest(BaseModel):
    messages: List[Message]
    stream: Optional[bool] = False

class ChatKitResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[dict]
    usage: dict

@router.post("/chat")
async def chat(request: Request):
    """
    Chat endpoint that uses RAG to answer questions based on ingested documents
    """
    try:
        # Parse JSON data from the request body
        json_data = await request.json()
        message = json_data.get("message")
        session_id = json_data.get("session_id")

        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        api_logger.info(f"Processing chat request for session: {session_id or 'new_session'}")

        # Generate a session ID if not provided
        session_id = session_id or str(uuid.uuid4())

        # Add user message to the session
        await db_service.add_message(session_id, "user", message)

        # Generate embedding for the user's query
        api_logger.debug("Generating embedding for user query")
        query_embeddings = await gemini_service.generate_embeddings([message])
        query_vector = query_embeddings[0]

        # Search for top 5 relevant chunks from Qdrant
        api_logger.debug("Searching for top 5 relevant chunks in Qdrant")
        search_results = await qdrant_service.search_similar(query_vector, limit=5)

        # Build context from search results
        context_parts = []
        for result in search_results:
            content = result['payload']['text']  # Using 'text' field as specified in the payload
            context_parts.append(f"Source: {result['payload']['source_file']}\nContent: {content}")

        context = "\n\n".join(context_parts)

        # Inject chunks as context into system prompt
        if context:
            system_prompt = f"You are an AI assistant for this book. Answer only using the book content.\n\nBook Content:\n{context}\n\nQuestion: {message}"
        else:
            system_prompt = f"You are an AI assistant for this book. Answer only using the book content.\n\nQuestion: {message}"

        # Generate response using Gemini Flash API
        api_logger.debug("Generating response with Gemini Flash model")
        response = await gemini_service.generate_response(system_prompt)

        # Add assistant response to the session
        await db_service.add_message(session_id, "assistant", response)

        api_logger.info(f"Chat response generated successfully for session: {session_id}")

        # Return a consistent response format
        return {
            "role": "assistant",
            "content": response,
            "session_id": session_id
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        api_logger.error(f"Error during chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")

@router.post("/chat/selected-text")
async def chat_selected_text(request: Request):
    """
    Chat endpoint that answers questions based only on the selected/highlighted text
    """
    try:
        # Parse JSON data from the request body
        json_data = await request.json()
        message = json_data.get("message")
        selected_text = json_data.get("selected_text")
        session_id = json_data.get("session_id")

        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        if not selected_text:
            raise HTTPException(status_code=400, detail="Selected text is required")

        api_logger.info(f"Processing selected text chat request for session: {session_id or 'new_session'}")

        # Generate a session ID if not provided
        session_id = session_id or str(uuid.uuid4())

        # Add user message to the session
        await db_service.add_message(session_id, "user", message)

        # Generate response using ONLY selected_text as context (no vector DB)
        api_logger.debug("Generating response based on selected text only, without vector DB")
        response = await gemini_service.generate_response_with_selected_text(message, selected_text)

        # Add assistant response to the session
        await db_service.add_message(session_id, "assistant", response)

        api_logger.info(f"Selected text chat response generated successfully for session: {session_id}")

        # Return a consistent response format
        return {
            "role": "assistant",
            "content": response,
            "session_id": session_id
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        api_logger.error(f"Error during selected text chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during selected text chat: {str(e)}")

@router.get("/chat/sessions")
async def get_chat_sessions():
    """
    Get recent chat sessions
    """
    try:
        api_logger.debug("Getting recent chat sessions")
        sessions = await db_service.get_recent_sessions(limit=20)
        api_logger.info(f"Retrieved {len(sessions)} recent chat sessions")

        return {
            "sessions": [
                {
                    "session_id": session.session_id,
                    "title": session.title,
                    "created_at": session.created_at,
                    "updated_at": session.updated_at
                }
                for session in sessions
            ]
        }
    except Exception as e:
        api_logger.error(f"Error getting chat sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting chat sessions: {str(e)}")

@router.get("/chat/session/{session_id}")
async def get_chat_session(session_id: str):
    """
    Get messages for a specific chat session
    """
    try:
        api_logger.debug(f"Getting chat session: {session_id}")
        messages = await db_service.get_messages_by_session(session_id)
        api_logger.info(f"Retrieved {len(messages)} messages for session: {session_id}")

        return {
            "session_id": session_id,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                    "timestamp": message.timestamp
                }
                for message in messages
            ]
        }
    except Exception as e:
        api_logger.error(f"Error getting chat session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting chat session: {str(e)}")

@router.post("/chat/completions", response_model=ChatKitResponse)
async def chat_completions(request: Request):
    """
    Chat completions endpoint compatible with ChatKit
    """
    try:
        # Parse JSON data from the request body
        json_data = await request.json()
        messages = json_data.get("messages", [])

        # Extract the last user message
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found in request")

        # Generate embedding for the user's query
        api_logger.debug("Generating embedding for user query")
        query_embeddings = await gemini_service.generate_embeddings([user_message])
        query_vector = query_embeddings[0]

        # Search for top 5 relevant chunks from Qdrant
        api_logger.debug("Searching for top 5 relevant chunks in Qdrant")
        search_results = await qdrant_service.search_similar(query_vector, limit=5)

        # Build context from search results
        context_parts = []
        for result in search_results:
            content = result['payload']['text']  # Using 'text' field as specified in the payload
            context_parts.append(content)

        context = "\n\n".join(context_parts)

        # Create a prompt that combines the user query with the retrieved context
        prompt = f"""
        You are a helpful assistant for a Physical AI textbook. Use the following context to answer the user's question.
        If the context doesn't contain enough information to answer the question, say so clearly.

        Context:
        {context}

        User Question: {user_message}

        Answer:
        """

        # Generate response using Gemini Flash API
        api_logger.debug("Generating response with Gemini Flash model")
        response_text = await gemini_service.generate_response(prompt)

        # Format response in ChatKit-compatible format
        import time
        import uuid

        response = ChatKitResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            created=int(time.time()),
            model="gemini-2.5-flash",
            choices=[
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ],
            usage={
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(user_message.split()) + len(response_text.split())
            }
        )

        return response

    except Exception as e:
        api_logger.error(f"Error in chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))