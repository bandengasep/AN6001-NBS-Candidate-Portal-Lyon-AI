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
            # Try text extraction first
            pdf = pdfplumber.open(io.BytesIO(contents))
            raw_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            # Also try extracting tables
            for page in pdfplumber.open(io.BytesIO(contents)).pages:
                for table in (page.extract_tables() or []):
                    for row in table:
                        cells = [str(c) for c in row if c]
                        if cells:
                            raw_text += "\n" + " | ".join(cells)
            pdf.close()

            if raw_text.strip() and len(raw_text.strip()) > 50:
                extracted = raw_text.strip()[:3000]
                return FileExtractResponse(text=extracted, file_type="pdf", filename=file.filename)

            # Fallback: use GPT vision on the PDF (treat as image-based document)
            return _extract_with_vision(contents, "application/pdf", file.filename, "pdf")

        else:
            # Image: use GPT vision
            mime = "image/jpeg" if ext in {".jpg", ".jpeg"} else "image/png"
            return _extract_with_vision(contents, mime, file.filename, "image")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


def _extract_with_vision(contents: bytes, mime: str, filename: str, file_type: str) -> FileExtractResponse:
    """Extract content from a file using GPT vision API."""
    settings = get_settings()
    client = get_openai_client()
    b64_data = base64.b64encode(contents).decode("utf-8")

    # For PDFs, GPT vision needs image format -- use the first bytes as-is
    # GPT vision supports PDF data URLs directly with some models
    # Fall back to sending as a generic base64 document
    if mime == "application/pdf":
        data_url = f"data:application/pdf;base64,{b64_data}"
    else:
        data_url = f"data:{mime};base64,{b64_data}"

    response = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract all visible text, data, and information from this document. "
                    "If it is a transcript or grade sheet, list all courses, grades, and GPA. "
                    "If it is a certificate, note the qualification, institution, and date. "
                    "If it is a CV/resume, extract key details. "
                    "Be thorough, structured, and concise."
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please extract all text and information from this document:"},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ],
        max_tokens=1500
    )
    extracted = response.choices[0].message.content
    return FileExtractResponse(text=extracted, file_type=file_type, filename=filename)


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
