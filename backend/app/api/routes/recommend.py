"""Recommendation API routes."""

import json
import math
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


class QuizAnswers(BaseModel):
    """User's quiz answers as scores per axis."""
    quantitative: int  # 1-5
    experience: int
    leadership: int
    tech_analytics: int
    business_domain: int
    career_ambition: int
    study_flexibility: int
    cv_text: str | None = None  # Optional raw CV text


class ProgramMatch(BaseModel):
    """A matched programme with score."""
    program_id: str
    name: str
    degree_type: str
    url: str | None
    similarity: float
    profile_scores: dict


class MatchResponse(BaseModel):
    """Recommendation results."""
    user_scores: dict
    matches: list[ProgramMatch]


@router.post("/match", response_model=MatchResponse)
async def match_programmes(answers: QuizAnswers, supabase: SupabaseDep) -> MatchResponse:
    """Match user profile to programmes using hybrid scoring.

    Combines direct spider-chart profile similarity (normalized Euclidean
    distance on 7 axes) with semantic embedding similarity against programme
    documents. Uses adaptive weights based on whether CV text is present.
    """
    user_scores = {
        "quantitative": answers.quantitative,
        "experience": answers.experience,
        "leadership": answers.leadership,
        "tech_analytics": answers.tech_analytics,
        "business_domain": answers.business_domain,
        "career_ambition": answers.career_ambition,
        "study_flexibility": answers.study_flexibility,
    }
    axes = list(user_scores.keys())

    # --- Semantic similarity via vector search ---
    profile_parts = [
        f"I have {_experience_label(answers.experience)} of work experience.",
        f"My quantitative skills are {_level_label(answers.quantitative)}.",
        f"My leadership experience is {_level_label(answers.leadership)}.",
        f"My interest in technology and analytics is {_level_label(answers.tech_analytics)}.",
        f"I am interested in {_domain_label(answers.business_domain)}.",
        f"My career goal is to {_ambition_label(answers.career_ambition)}.",
        f"I prefer {_flexibility_label(answers.study_flexibility)} study.",
    ]
    if answers.cv_text:
        profile_parts.append(f"Background from CV: {answers.cv_text[:1000]}")
    profile_text = " ".join(profile_parts)

    user_embedding = get_embedding(profile_text)
    result = supabase.rpc(
        "match_documents",
        {
            "query_embedding": user_embedding,
            "match_count": 20,
            "match_threshold": 0.25
        }
    ).execute()

    # Best semantic similarity per programme
    semantic_scores: dict[str, float] = {}
    for doc in (result.data or []):
        prog_name = doc.get("metadata", {}).get("program", "")
        sim = doc.get("similarity", 0)
        if prog_name and (prog_name not in semantic_scores or sim > semantic_scores[prog_name]):
            semantic_scores[prog_name] = sim

    # --- Profile similarity + hybrid scoring for ALL programmes ---
    all_programs = supabase.table("programs").select("*").execute()

    has_cv = bool(answers.cv_text)
    w_profile = 0.4 if has_cv else 0.8
    w_semantic = 0.6 if has_cv else 0.2

    scored: list[tuple[dict, float]] = []
    for prog in (all_programs.data or []):
        prog_scores = prog.get("profile_scores") or {}
        if not prog_scores:
            continue

        profile_sim = _profile_similarity(user_scores, prog_scores, axes)
        raw_semantic = semantic_scores.get(prog["name"], 0.0)
        semantic_sim = _rescale_semantic(raw_semantic)

        final = w_profile * profile_sim + w_semantic * semantic_sim
        scored.append((prog, round(final, 3)))

    scored.sort(key=lambda x: -x[1])

    matches = []
    for prog, score in scored[:3]:
        matches.append(ProgramMatch(
            program_id=prog["id"],
            name=prog["name"],
            degree_type=prog["degree_type"],
            url=prog.get("url"),
            similarity=score,
            profile_scores=prog.get("profile_scores") or {}
        ))

    return MatchResponse(user_scores=user_scores, matches=matches)


# Helper functions to convert numeric scores to natural language
def _level_label(score: int) -> str:
    return {1: "very limited", 2: "limited", 3: "moderate", 4: "strong", 5: "very strong"}.get(score, "moderate")

def _experience_label(score: int) -> str:
    return {1: "no", 2: "1-2 years", 3: "3-5 years", 4: "6-10 years", 5: "10+ years"}.get(score, "some")

def _domain_label(score: int) -> str:
    return {1: "general business", 2: "marketing and strategy", 3: "finance and accounting", 4: "technology and analytics", 5: "quantitative research"}.get(score, "business")

def _ambition_label(score: int) -> str:
    return {1: "explore options", 2: "advance in current field", 3: "switch careers", 4: "move into leadership", 5: "pursue research or academia"}.get(score, "advance my career")

def _flexibility_label(score: int) -> str:
    return {1: "full-time intensive", 2: "full-time standard", 3: "either full or part-time", 4: "part-time preferred", 5: "part-time or online only"}.get(score, "flexible")


_MAX_EUCLIDEAN = math.sqrt(7 * (5 - 1) ** 2)  # ~10.583


def _profile_similarity(user: dict, programme: dict, axes: list[str]) -> float:
    """Normalized Euclidean distance between user and programme scores (0-1)."""
    dist_sq = sum((user.get(a, 3) - programme.get(a, 3)) ** 2 for a in axes)
    return 1.0 - math.sqrt(dist_sq) / _MAX_EUCLIDEAN


def _rescale_semantic(raw: float, lo: float = 0.25, hi: float = 0.60) -> float:
    """Rescale raw cosine similarity from [lo, hi] to [0, 1]."""
    if raw <= lo:
        return 0.0
    if raw >= hi:
        return 1.0
    return (raw - lo) / (hi - lo)
