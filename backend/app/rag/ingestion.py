"""Document ingestion pipeline for RAG."""

import re
from typing import Any
from app.config import get_settings
from app.db.supabase import get_supabase_admin_client
from app.rag.embeddings import get_embeddings_batch


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None
) -> list[str]:
    """Split text into overlapping chunks.

    Args:
        text: Text to split
        chunk_size: Maximum characters per chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    settings = get_settings()
    if chunk_size is None:
        chunk_size = settings.chunk_size
    if chunk_overlap is None:
        chunk_overlap = settings.chunk_overlap

    # Clean text
    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings
            last_period = text.rfind('. ', start, end)
            last_newline = text.rfind('\n', start, end)
            break_point = max(last_period, last_newline)

            if break_point > start + chunk_size // 2:
                end = break_point + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - chunk_overlap

    return chunks


def prepare_documents(
    texts: list[str],
    metadatas: list[dict[str, Any]] | None = None
) -> list[dict]:
    """Prepare documents with chunking and metadata.

    Args:
        texts: List of document texts
        metadatas: Optional list of metadata dicts (one per text)

    Returns:
        List of prepared document dicts
    """
    if metadatas is None:
        metadatas = [{} for _ in texts]

    documents = []
    for text, metadata in zip(texts, metadatas):
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            doc_metadata = {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            documents.append({
                "content": chunk,
                "metadata": doc_metadata
            })

    return documents


async def ingest_documents(
    texts: list[str],
    metadatas: list[dict[str, Any]] | None = None,
    batch_size: int = 100
) -> int:
    """Ingest documents into the vector database.

    Args:
        texts: List of document texts
        metadatas: Optional list of metadata dicts
        batch_size: Number of documents to process at once

    Returns:
        Number of documents ingested
    """
    # Prepare documents with chunking
    documents = prepare_documents(texts, metadatas)

    if not documents:
        return 0

    client = get_supabase_admin_client()
    total_ingested = 0

    # Process in batches
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        contents = [doc["content"] for doc in batch]

        # Generate embeddings for batch
        embeddings = get_embeddings_batch(contents)

        # Prepare records for insertion
        records = [
            {
                "content": doc["content"],
                "metadata": doc["metadata"],
                "embedding": emb
            }
            for doc, emb in zip(batch, embeddings)
        ]

        # Insert into Supabase
        result = client.table("documents").insert(records).execute()
        total_ingested += len(result.data) if result.data else 0

    return total_ingested


async def ingest_program_data(program: dict) -> int:
    """Ingest a program's data into the vector database.

    Args:
        program: Program data dict with name, description, etc.

    Returns:
        Number of documents ingested
    """
    texts = []
    metadatas = []

    # Main program description
    if program.get("description"):
        texts.append(f"{program['name']}: {program['description']}")
        metadatas.append({
            "type": "program_description",
            "program": program["name"],
            "degree_type": program.get("degree_type", ""),
            "url": program.get("url", "")
        })

    # Requirements
    if program.get("requirements"):
        req_text = f"{program['name']} Requirements: "
        if isinstance(program["requirements"], dict):
            req_text += " ".join(f"{k}: {v}" for k, v in program["requirements"].items())
        else:
            req_text += str(program["requirements"])
        texts.append(req_text)
        metadatas.append({
            "type": "requirements",
            "program": program["name"],
            "degree_type": program.get("degree_type", "")
        })

    # Additional content sections
    for key in ["curriculum", "career_outcomes", "faculty", "admissions"]:
        if program.get(key):
            texts.append(f"{program['name']} {key.replace('_', ' ').title()}: {program[key]}")
            metadatas.append({
                "type": key,
                "program": program["name"],
                "degree_type": program.get("degree_type", "")
            })

    # Process sections dictionary if present
    if program.get("sections") and isinstance(program["sections"], dict):
        for section_name, section_content in program["sections"].items():
            if section_content and section_content.strip():
                texts.append(f"{program['name']} - {section_name}: {section_content}")
                metadatas.append({
                    "type": "section",
                    "section_name": section_name,
                    "program": program["name"],
                    "degree_type": program.get("degree_type", "")
                })

    return await ingest_documents(texts, metadatas)
