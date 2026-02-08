#!/usr/bin/env python3
"""Unified script to deep-scrape NBS programmes and ingest into Supabase.

Replaces the separate scrape_nbs.py and ingest_data.py scripts.

Usage:
    python scripts/scrape_and_ingest.py                # Scrape all programmes and ingest
    python scripts/scrape_and_ingest.py --clean         # Truncate DB first, then scrape + ingest
    python scripts/scrape_and_ingest.py --programme mba # Scrape only programmes matching 'mba'
    python scripts/scrape_and_ingest.py --no-pdfs       # Skip PDF download/extraction
    python scripts/scrape_and_ingest.py --dry-run       # Scrape only, don't write to DB
    python scripts/scrape_and_ingest.py --save-json     # Also save scraped data to JSON
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from dotenv import load_dotenv

# Load environment variables from backend/.env
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(env_path)

from app.scrapers.deep_scraper import NBSDeepScraper, ScrapedProgramme
from app.scrapers.programme_registry import (
    ProgrammeEntry,
    get_registry,
    get_registry_by_slug,
)
from app.scrapers.content_cleaner import clean_pdf_text
from app.rag.ingestion import ingest_program_data
from app.db.supabase import get_supabase_admin_client

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deep-scrape NBS programmes and ingest into Supabase vector store."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Truncate documents table and delete all programmes before ingesting.",
    )
    parser.add_argument(
        "--programme",
        type=str,
        default=None,
        help="Only scrape programmes whose name/slug contains this string (case-insensitive).",
    )
    parser.add_argument(
        "--no-pdfs",
        action="store_true",
        help="Skip PDF download and extraction.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scrape only; do not write anything to the database.",
    )
    parser.add_argument(
        "--save-json",
        action="store_true",
        help="Save scraped data to data/scraped/ as JSON alongside DB ingestion.",
    )
    return parser.parse_args()


def filter_registry(
    registry: list[ProgrammeEntry], filter_text: str | None
) -> list[ProgrammeEntry]:
    """Filter registry by name/slug substring match."""
    if not filter_text:
        return registry
    ft = filter_text.lower()
    return [
        p for p in registry
        if ft in p.name.lower() or ft in p.slug.lower()
    ]


def clean_database():
    """Truncate documents table and delete all programme rows."""
    print("Cleaning database...")
    client = get_supabase_admin_client()

    # Delete all documents
    client.table("documents").delete().neq("id", 0).execute()
    print("  -> Deleted all rows from 'documents'")

    # Delete all programmes
    try:
        client.table("programs").delete().neq("id", 0).execute()
        print("  -> Deleted all rows from 'programs'")
    except Exception as e:
        logger.warning("Could not clean 'programs' table: %s", e)


def _extract_degree_type(entry: ProgrammeEntry) -> str:
    """Derive degree_type from programme name/category."""
    name_upper = entry.name.upper()
    if entry.category == "phd":
        return "PhD"
    if entry.category == "undergraduate":
        return "Bachelor"
    if "EMBA" in name_upper or "EXECUTIVE MBA" in name_upper:
        return "EMBA"
    if "MBA" in name_upper:
        return "MBA"
    if "MSC" in name_upper or "MASTER" in name_upper:
        return "MSc"
    return "Other"


def upsert_programme(entry: ProgrammeEntry, scraped: ScrapedProgramme):
    """Write programme metadata to the programs table."""
    client = get_supabase_admin_client()

    landing = scraped.landing_page
    description = ""
    if landing and landing.content:
        description = landing.content[:3000]

    record = {
        "name": entry.name,
        "degree_type": _extract_degree_type(entry),
        "description": description,
        "url": entry.landing_url,
        "metadata": {
            "category": entry.category,
            "slug": entry.slug,
            "language": entry.language,
            "is_external": entry.is_external,
            **scraped.structured_data,
        },
    }

    # Try upsert by name
    try:
        existing = (
            client.table("programs")
            .select("id")
            .eq("name", entry.name)
            .execute()
        )
        if existing.data:
            client.table("programs").update(record).eq("name", entry.name).execute()
        else:
            client.table("programs").insert(record).execute()
    except Exception as e:
        logger.warning("Failed to upsert programme %s: %s", entry.name, e)


def build_program_dict(entry: ProgrammeEntry, scraped: ScrapedProgramme) -> dict:
    """Convert ScrapedProgramme into the dict format expected by ingest_program_data."""
    landing = scraped.landing_page

    program = {
        "name": entry.name,
        "url": entry.landing_url,
        "degree_type": _extract_degree_type(entry),
        "category": entry.category,
        "language": entry.language,
        "description": landing.content if landing and not landing.error else "",
        "sections": landing.sections if landing else {},
        "requirements": {},
    }

    # Sub-pages
    sub_pages: dict[str, dict] = {}
    for suffix, page in scraped.sub_pages.items():
        sub_pages[suffix] = {
            "url": page.url,
            "content": page.content,
            "sections": page.sections,
        }
        # Extract requirements from admissions sub-page
        if suffix in ("admissions", "admission"):
            for sec_key, sec_val in page.sections.items():
                if any(t in sec_key.lower() for t in ("requirement", "eligibility", "admission")):
                    program["requirements"][sec_key] = sec_val
    program["sub_pages"] = sub_pages

    # PDF contents
    pdf_contents: list[dict] = []
    for pdf in scraped.pdf_contents:
        if not pdf.full_text:
            continue
        cleaned = clean_pdf_text(pdf.full_text)
        if cleaned:
            pdf_contents.append({
                "source_url": pdf.source_url,
                "text": cleaned,
            })
    program["pdf_contents"] = pdf_contents

    return program


async def ingest_one_programme(entry: ProgrammeEntry, scraped: ScrapedProgramme, dry_run: bool) -> int:
    """Upsert programme metadata and ingest all documents for one programme."""
    if dry_run:
        return 0

    # Upsert to programs table
    upsert_programme(entry, scraped)

    # Build dict and ingest documents
    program_dict = build_program_dict(entry, scraped)
    count = await ingest_program_data(program_dict)
    return count


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    args = parse_args()
    registry = filter_registry(get_registry(), args.programme)

    if not registry:
        print("No programmes matched the filter. Exiting.")
        return

    print(f"NBS Deep Scraper + Ingest")
    print(f"=" * 60)
    print(f"Programmes to scrape: {len(registry)}")
    print(f"PDF extraction: {'OFF' if args.no_pdfs else 'ON'}")
    print(f"Dry run: {'YES' if args.dry_run else 'NO'}")
    print(f"=" * 60)

    # Clean DB if requested
    if args.clean and not args.dry_run:
        clean_database()

    # Scrape
    pdf_dir = str(Path(__file__).parent.parent / "data" / "pdfs")
    with NBSDeepScraper(skip_pdfs=args.no_pdfs, pdf_download_dir=pdf_dir) as scraper:
        results = scraper.scrape_all(registry)

    # Ingest
    total_chunks = 0
    total_pages = 0
    total_pdfs = 0
    successful = 0
    all_program_dicts = []

    for scraped in results:
        entry = scraped.entry

        if scraped.landing_page and scraped.landing_page.error:
            print(f"  Skipping {entry.name} (landing page failed)")
            continue

        n_sub = len(scraped.sub_pages)
        n_pdf = len(scraped.pdf_contents)
        total_pages += 1 + n_sub
        total_pdfs += n_pdf

        count = await ingest_one_programme(entry, scraped, args.dry_run)
        total_chunks += count
        successful += 1
        print(f"  Ingested {entry.name}: {count} chunks")

        if args.save_json:
            all_program_dicts.append(build_program_dict(entry, scraped))

    # Save JSON if requested
    if args.save_json and all_program_dicts:
        json_dir = Path(__file__).parent.parent / "data" / "scraped"
        json_dir.mkdir(parents=True, exist_ok=True)
        json_path = json_dir / "all_programs_deep.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_program_dicts, f, indent=2, ensure_ascii=False)
        print(f"\nSaved JSON to {json_path}")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"SCRAPE + INGEST COMPLETE")
    print(f"{'=' * 60}")
    print(f"Programmes scraped:  {successful}/{len(registry)}")
    print(f"Pages crawled:       {total_pages}")
    print(f"PDFs extracted:      {total_pdfs}")
    print(f"Document chunks:     {total_chunks}")
    if args.dry_run:
        print(f"(Dry run - nothing written to database)")


if __name__ == "__main__":
    asyncio.run(main())
