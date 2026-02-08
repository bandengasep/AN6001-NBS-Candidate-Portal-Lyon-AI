"""Programs API routes."""

from fastapi import APIRouter, HTTPException
from app.api.deps import SupabaseDep
from app.db.models import Program

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get("/", response_model=list[Program])
async def list_programs(supabase: SupabaseDep) -> list[Program]:
    """List all NBS degree programs."""
    result = supabase.table("programs").select("*").execute()
    return [Program(**p) for p in result.data] if result.data else []


@router.get("/{program_id}", response_model=Program)
async def get_program(program_id: str, supabase: SupabaseDep) -> Program:
    """Get a specific program by ID."""
    result = supabase.table("programs").select("*").eq("id", program_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Program not found")
    return Program(**result.data)


@router.get("/type/{degree_type}", response_model=list[Program])
async def get_programs_by_type(degree_type: str, supabase: SupabaseDep) -> list[Program]:
    """Get programs by degree type (MBA, MSc, PhD, etc.)."""
    result = supabase.table("programs").select("*").ilike("degree_type", f"%{degree_type}%").execute()
    return [Program(**p) for p in result.data] if result.data else []


@router.get("/{program_id}/profile")
async def get_program_profile(program_id: str, supabase: SupabaseDep) -> dict:
    """Get a programme's spider chart profile scores."""
    result = supabase.table("programs").select("name, profile_scores").eq("id", program_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Program not found")
    return result.data
