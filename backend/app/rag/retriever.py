"""Vector similarity retrieval from Supabase pgvector."""

from app.config import get_settings
from app.db.supabase import get_supabase_client
from app.rag.embeddings import get_embedding


async def retrieve_relevant_documents(
    query: str,
    match_count: int | None = None,
    match_threshold: float = 0.5
) -> list[dict]:
    """Retrieve documents relevant to the query using vector similarity.

    Args:
        query: User query text
        match_count: Number of documents to retrieve (default from settings)
        match_threshold: Minimum similarity threshold (0-1)

    Returns:
        List of relevant documents with content, metadata, and similarity score
    """
    settings = get_settings()
    if match_count is None:
        match_count = settings.retrieval_k

    # Generate query embedding
    query_embedding = get_embedding(query)

    # Search using Supabase RPC function
    client = get_supabase_client()
    result = client.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": match_count,
            "match_threshold": match_threshold
        }
    ).execute()

    return result.data or []


async def retrieve_program_documents(
    program_name: str,
    match_count: int = 5
) -> list[dict]:
    """Retrieve documents specifically about a program.

    Args:
        program_name: Name of the program to search for
        match_count: Number of documents to retrieve

    Returns:
        List of relevant documents about the program
    """
    query = f"Information about {program_name} program at NBS Nanyang Business School"
    return await retrieve_relevant_documents(query, match_count=match_count)


async def retrieve_comparison_documents(
    programs: list[str],
    match_count: int = 8
) -> list[dict]:
    """Retrieve documents for comparing multiple programs.

    Args:
        programs: List of program names to compare
        match_count: Total number of documents to retrieve

    Returns:
        List of relevant documents about the programs
    """
    program_list = ", ".join(programs)
    query = f"Compare {program_list} programs at NBS: requirements, curriculum, career outcomes"
    return await retrieve_relevant_documents(query, match_count=match_count)
