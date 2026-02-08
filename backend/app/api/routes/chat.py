"""Chat API routes."""

import base64
import io
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import pdfplumber

from app.db.models import ChatRequest, ChatResponse
from app.agents import create_nbs_agent
from app.config import get_settings
from app.rag.embeddings import get_openai_client

router = APIRouter(prefix="/chat", tags=["chat"])

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


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


class FileExtractResponse(BaseModel):
    """Extracted text from an uploaded file."""
    text: str
    file_type: str
    filename: str


@router.post("/upload-file", response_model=FileExtractResponse)
async def upload_file(file: UploadFile = File(...)) -> FileExtractResponse:
    """Extract text content from an uploaded PDF or image.

    - PDF: text extracted via pdfplumber
    - Images (JPG/PNG): content described via GPT vision

    Returns extracted text that the frontend can include in a chat message.
    """
    import os
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Accepted: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")

    try:
        if ext == ".pdf":
            pdf = pdfplumber.open(io.BytesIO(contents))
            raw_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            pdf.close()
            if not raw_text.strip():
                raise HTTPException(status_code=400, detail="Could not extract text from PDF")
            # Truncate to reasonable length for chat context
            extracted = raw_text[:3000]
            return FileExtractResponse(text=extracted, file_type="pdf", filename=file.filename)

        else:
            # Image: use GPT vision to describe/extract content
            settings = get_settings()
            client = get_openai_client()
            b64_image = base64.b64encode(contents).decode("utf-8")
            mime = "image/jpeg" if ext in {".jpg", ".jpeg"} else "image/png"

            response = client.chat.completions.create(
                model=settings.chat_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Extract all visible text and data from this image. If it's a transcript or grade sheet, list all courses and grades. If it's a certificate, note the details. Be thorough and structured."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please extract all text and information from this document image:"},
                            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64_image}"}}
                        ]
                    }
                ],
                max_tokens=1500
            )
            extracted = response.choices[0].message.content
            return FileExtractResponse(text=extracted, file_type="image", filename=file.filename)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


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
