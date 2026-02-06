"""Dependency injection for API routes."""

from typing import Annotated
from fastapi import Depends

from app.config import Settings, get_settings
from app.db.supabase import get_supabase_client
from supabase import Client


SettingsDep = Annotated[Settings, Depends(get_settings)]
SupabaseDep = Annotated[Client, Depends(get_supabase_client)]
