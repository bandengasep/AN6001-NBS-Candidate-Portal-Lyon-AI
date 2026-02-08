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

    # Clean text - strip null bytes (PostgreSQL rejects \u0000)
    text = text.replace("\x00", "")
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
            Supports both legacy format (flat dict) and new deep-scraper
            format with sub_pages and pdf_contents.

    Returns:
        Number of documents ingested
    """
    texts = []
    metadatas = []

    # Common metadata fields
    base_meta = {
        "program": program["name"],
        "degree_type": program.get("degree_type", ""),
        "category": program.get("category", ""),
        "language": program.get("language", "en"),
    }

    # Main program description
    if program.get("description"):
        texts.append(f"{program['name']}: {program['description']}")
        metadatas.append({
            **base_meta,
            "type": "program_description",
            "source_url": program.get("url", ""),
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
            **base_meta,
            "type": "requirements",
        })

    # Additional content sections (legacy keys)
    for key in ["curriculum", "career_outcomes", "faculty", "admissions"]:
        if program.get(key):
            texts.append(f"{program['name']} {key.replace('_', ' ').title()}: {program[key]}")
            metadatas.append({
                **base_meta,
                "type": key,
            })

    # Process sections dictionary if present
    if program.get("sections") and isinstance(program["sections"], dict):
        for section_name, section_content in program["sections"].items():
            if section_content and section_content.strip():
                texts.append(f"{program['name']} - {section_name}: {section_content}")
                metadatas.append({
                    **base_meta,
                    "type": "section",
                    "section_name": section_name,
                })

    # ── New deep-scraper fields ──────────────────────────────────────

    # Sub-pages: dict keyed by sub-page type (e.g. "admissions", "faqs")
    if program.get("sub_pages") and isinstance(program["sub_pages"], dict):
        for sub_page_type, sub_page in program["sub_pages"].items():
            content = sub_page.get("content", "") if isinstance(sub_page, dict) else str(sub_page)
            if not content or not content.strip():
                continue
            texts.append(f"{program['name']} - {sub_page_type}: {content}")
            metadatas.append({
                **base_meta,
                "type": "sub_page",
                "sub_page": sub_page_type,
                "source_url": sub_page.get("url", "") if isinstance(sub_page, dict) else "",
            })

            # Also ingest sub-page sections
            if isinstance(sub_page, dict) and sub_page.get("sections"):
                for sec_name, sec_content in sub_page["sections"].items():
                    if sec_content and sec_content.strip():
                        texts.append(
                            f"{program['name']} - {sub_page_type} - {sec_name}: {sec_content}"
                        )
                        metadatas.append({
                            **base_meta,
                            "type": "sub_page_section",
                            "sub_page": sub_page_type,
                            "section_name": sec_name,
                            "source_url": sub_page.get("url", ""),
                        })

    # PDF contents
    if program.get("pdf_contents") and isinstance(program["pdf_contents"], list):
        for pdf in program["pdf_contents"]:
            text = pdf.get("text", "") if isinstance(pdf, dict) else str(pdf)
            if not text or not text.strip():
                continue
            texts.append(f"{program['name']} (PDF Brochure): {text}")
            metadatas.append({
                **base_meta,
                "type": "pdf_brochure",
                "source_url": pdf.get("source_url", "") if isinstance(pdf, dict) else "",
            })

    return await ingest_documents(texts, metadatas)
