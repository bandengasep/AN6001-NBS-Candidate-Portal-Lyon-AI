"""Recommendation API routes."""

import json
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import pdfplumber
import io

from app.config import get_settings
from app.rag.embeddings import get_openai_client
from app.api.deps import SupabaseDep

router = APIRouter(prefix="/recommend", tags=["recommend"])


# The 11 in-scope Graduate Studies programmes
IN_SCOPE_PROGRAMMES = {
    "Nanyang MBA",
    "Nanyang Fellows MBA",
    "Nanyang Executive MBA",
    "Nanyang Professional MBA",
    "MSc Business Analytics",
    "MSc Finance",
    "MSc Financial Engineering",
    "MSc Marketing Science",
    "MSc Actuarial and Risk Analytics",
    "MSc Accountancy",
    "Master in Management",
}


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


class BranchAnswers(BaseModel):
    """User's branching quiz answers."""
    experience: str  # junior, mid, senior
    track_choice: str | None = None  # track-mba or track-masters (only for mid-experience)
    mba_choice: str | None = None  # MBA sub-question answer
    masters_choice: str | None = None  # Masters sub-question answer


class ProgramMatch(BaseModel):
    """A matched programme."""
    program_id: str
    name: str
    degree_type: str
    url: str | None
    rationale: str


class MatchResponse(BaseModel):
    """Recommendation results."""
    matches: list[ProgramMatch]


# Mapping from quiz branch answers to programme names
MBA_BRANCH_MAP = {
    "full-time-career-switch": ["Nanyang MBA"],
    "full-time-elite": ["Nanyang Fellows MBA"],
    "part-time": ["Nanyang Professional MBA", "Nanyang Executive MBA"],
    "senior-leadership": ["Nanyang Executive MBA"],
}

MASTERS_BRANCH_MAP = {
    "data-analytics": ["MSc Business Analytics", "MSc Financial Engineering"],
    "finance": ["MSc Finance", "MSc Financial Engineering", "MSc Actuarial and Risk Analytics"],
    "accounting": ["MSc Accountancy"],
    "marketing": ["MSc Marketing Science"],
    "general-management": ["Master in Management", "MSc Marketing Science"],
}

# Rationales for each programme
PROGRAMME_RATIONALES = {
    "Nanyang MBA": "A 12-month full-time programme designed for career switchers with 2+ years of experience. Strong global network and career services.",
    "Nanyang Fellows MBA": "An elite full-time MBA with a highly selective cohort, strong industry mentoring, and global exchange opportunities.",
    "Nanyang Executive MBA": "An 18-month part-time programme for senior leaders who want to advance while continuing to work. Requires 8+ years of experience.",
    "Nanyang Professional MBA": "A part-time MBA for working professionals who want to build leadership skills without leaving their careers.",
    "MSc Business Analytics": "Focuses on data science, machine learning, and analytics for business decision-making. Ideal for those who want to work at the intersection of tech and business.",
    "MSc Finance": "Covers investment analysis, portfolio management, and corporate finance. Strong placement into banking and asset management roles.",
    "MSc Financial Engineering": "A quantitative programme covering derivatives, risk modelling, and algorithmic trading. Available in full-time and part-time tracks.",
    "MSc Marketing Science": "Blends marketing strategy with data analytics, consumer insights, and branding. Strong industry partnerships.",
    "MSc Actuarial and Risk Analytics": "Trains actuaries and risk professionals with a mix of statistics, finance, and insurance knowledge.",
    "MSc Accountancy": "Prepares graduates for careers in audit, tax, and advisory. Recognized by CPA and ACCA professional bodies.",
    "Master in Management": "A broad-based management degree for early-career professionals or fresh graduates who want a solid business foundation.",
}


@router.post("/match", response_model=MatchResponse)
async def match_programmes(answers: BranchAnswers, supabase: SupabaseDep) -> MatchResponse:
    """Match user to programmes based on branching quiz answers.

    Uses direct lookup from branch answers to programme names,
    then fetches programme details from the database.
    """
    # Determine track from experience
    track_map = {"junior": "masters", "mid": "both", "senior": "mba"}
    track = track_map.get(answers.experience, "masters")

    if track == "both" and answers.track_choice:
        track = "mba" if answers.track_choice == "track-mba" else "masters"

    # Resolve programme names from branch answer
    if track == "mba":
        programme_names = MBA_BRANCH_MAP.get(answers.mba_choice, [])
    else:
        programme_names = MASTERS_BRANCH_MAP.get(answers.masters_choice, [])

    if not programme_names:
        return MatchResponse(matches=[])

    # Fetch programme details from database
    all_programs = supabase.table("programs").select("*").execute()
    prog_lookup = {p["name"]: p for p in (all_programs.data or []) if p["name"] in IN_SCOPE_PROGRAMMES}

    matches = []
    for name in programme_names:
        prog = prog_lookup.get(name)
        if prog:
            matches.append(ProgramMatch(
                program_id=prog["id"],
                name=prog["name"],
                degree_type=prog["degree_type"],
                url=prog.get("url"),
                rationale=PROGRAMME_RATIONALES.get(name, ""),
            ))

    return MatchResponse(matches=matches)
