"""Chat API routes."""

from fastapi import APIRouter, HTTPException
from app.db.models import ChatRequest, ChatResponse
from app.agents import create_nbs_agent

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message and return AI response.

    Args:
        request: Chat request with message and optional conversation_id

    Returns:
        ChatResponse with AI response and conversation_id
    """
    try:
        agent = create_nbs_agent()
        result = await agent.chat(
            message=request.message,
            conversation_id=request.conversation_id
        )

        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            sources=result.get("sources", [])
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/history/{conversation_id}")
async def get_history(conversation_id: str, limit: int = 20):
    """Get chat history for a conversation.

    Args:
        conversation_id: Conversation ID
        limit: Maximum number of messages to return

    Returns:
        List of chat messages
    """
    from app.db.supabase import get_chat_history

    try:
        history = await get_chat_history(conversation_id, limit=limit)
        return {"conversation_id": conversation_id, "messages": history}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )
