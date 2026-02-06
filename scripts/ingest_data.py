#!/usr/bin/env python3
"""Script to ingest scraped NBS data into Supabase vector store."""

import asyncio
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(env_path)

from app.rag.ingestion import ingest_documents, ingest_program_data


async def ingest_programs_from_json(json_path: Path) -> int:
    """Ingest programs from JSON file.

    Args:
        json_path: Path to JSON file with program data

    Returns:
        Number of documents ingested
    """
    with open(json_path, "r", encoding="utf-8") as f:
        programs = json.load(f)

    total_ingested = 0

    for program in programs:
        if "error" in program:
            print(f"Skipping {program.get('name', 'Unknown')} due to error")
            continue

        print(f"Ingesting {program['name']}...")
        count = await ingest_program_data(program)
        total_ingested += count
        print(f"  -> Ingested {count} document chunks")

    return total_ingested


async def ingest_additional_content(content_dir: Path) -> int:
    """Ingest additional content files (markdown, txt).

    Args:
        content_dir: Directory containing content files

    Returns:
        Number of documents ingested
    """
    total_ingested = 0

    for filepath in content_dir.glob("*.md"):
        print(f"Ingesting {filepath.name}...")
        content = filepath.read_text(encoding="utf-8")
        count = await ingest_documents(
            [content],
            [{"source": filepath.name, "type": "additional_content"}]
        )
        total_ingested += count

    for filepath in content_dir.glob("*.txt"):
        print(f"Ingesting {filepath.name}...")
        content = filepath.read_text(encoding="utf-8")
        count = await ingest_documents(
            [content],
            [{"source": filepath.name, "type": "additional_content"}]
        )
        total_ingested += count

    return total_ingested


async def main():
    """Run the data ingestion pipeline."""
    print("Starting data ingestion...")
    print("=" * 50)

    data_dir = Path(__file__).parent.parent / "data" / "scraped"
    total = 0

    # Ingest programs from JSON
    programs_json = data_dir / "all_programs.json"
    if programs_json.exists():
        count = await ingest_programs_from_json(programs_json)
        total += count
        print(f"\nIngested {count} documents from programs")
    else:
        print(f"No programs file found at {programs_json}")
        print("Run scrape_nbs.py first to scrape program data")

    # Ingest additional content if present
    additional_count = await ingest_additional_content(data_dir)
    total += additional_count

    print("=" * 50)
    print(f"Ingestion complete! Total documents: {total}")


if __name__ == "__main__":
    asyncio.run(main())
