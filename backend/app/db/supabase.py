"""Supabase client initialization and utilities."""

from functools import lru_cache
from supabase import create_client, Client

from app.config import get_settings


@lru_cache
def get_supabase_client() -> Client:
    """Get cached Supabase client instance."""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def get_supabase_admin_client() -> Client:
    """Get Supabase client with service role key for admin operations."""
    settings = get_settings()
    key = settings.supabase_service_key or settings.supabase_key
    return create_client(settings.supabase_url, key)


async def store_document(content: str, embedding: list[float], metadata: dict) -> dict:
    """Store a document with its embedding in Supabase."""
    client = get_supabase_admin_client()
    result = client.table("documents").insert({
        "content": content,
        "embedding": embedding,
        "metadata": metadata
    }).execute()
    return result.data[0] if result.data else {}


async def search_documents(embedding: list[float], match_count: int = 4) -> list[dict]:
    """Search for similar documents using vector similarity."""
    client = get_supabase_client()
    result = client.rpc(
        "match_documents",
        {
            "query_embedding": embedding,
            "match_count": match_count
        }
    ).execute()
    return result.data or []


async def store_chat_message(conversation_id: str, role: str, content: str) -> dict:
    """Store a chat message in the conversation history."""
    client = get_supabase_client()
    result = client.table("chat_history").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content
    }).execute()
    return result.data[0] if result.data else {}


async def get_chat_history(conversation_id: str, limit: int = 10) -> list[dict]:
    """Retrieve chat history for a conversation."""
    client = get_supabase_client()
    result = client.table("chat_history").select("*").eq(
        "conversation_id", conversation_id
    ).order("created_at", desc=False).limit(limit).execute()
    return result.data or []
