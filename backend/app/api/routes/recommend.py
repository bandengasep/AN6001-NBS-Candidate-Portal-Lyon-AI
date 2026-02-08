"""Recommendation API routes."""

import json
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import pdfplumber
import io

from app.config import get_settings
from app.rag.embeddings import get_embedding, get_openai_client
from app.api.deps import SupabaseDep

router = APIRouter(prefix="/recommend", tags=["recommend"])


class CVParseResponse(BaseModel):
    """Structured fields extracted from CV."""
    years_experience: int | None = None
    industry: str | None = None
    education_level: str | None = None
    skills: list[str] = []
    quantitative_background: str | None = None
    leadership_experience: str | None = None
    raw_text: str = ""


@router.post("/parse-cv", response_model=CVParseResponse)
async def parse_cv(file: UploadFile = File(...)) -> CVParseResponse:
    """Upload and parse a PDF CV into structured fields.

    Extracts text with pdfplumber, then uses GPT to extract
    structured fields for quiz pre-fill.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    try:
        contents = await file.read()
        pdf = pdfplumber.open(io.BytesIO(contents))
        raw_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        pdf.close()

        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        settings = get_settings()
        client = get_openai_client()

        response = client.chat.completions.create(
            model=settings.chat_model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": """Extract structured information from this CV/resume.
Return JSON with these fields:
- years_experience: integer (total years of work experience, 0 if fresh graduate)
- industry: string (primary industry, e.g. "Finance", "Technology", "Consulting")
- education_level: string (one of: "Diploma", "Bachelor", "Master", "PhD")
- skills: array of strings (top 5-8 relevant skills)
- quantitative_background: string (one of: "Strong", "Moderate", "Limited")
- leadership_experience: string (one of: "Senior/Executive", "Mid-level/Manager", "Junior/None")"""},
                {"role": "user", "content": raw_text[:4000]}
            ]
        )

        parsed = json.loads(response.choices[0].message.content)
        return CVParseResponse(**parsed, raw_text=raw_text[:2000])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing CV: {str(e)}")
