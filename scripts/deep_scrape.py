#!/usr/bin/env python3
"""Deep-scrape all NBS programmes (landing pages, sub-pages, PDFs).

Outputs one JSON file per programme into data/scraped/deep/, plus a
combined all_programs_deep.json for the ingestion pipeline.
"""

import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.scrapers.deep_scraper import NBSDeepScraper, ScrapedProgramme
from app.scrapers.programme_registry import get_registry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def programme_to_dict(sp: ScrapedProgramme) -> dict:
    """Convert a ScrapedProgramme to a JSON-serialisable dict.

    Reshapes the dataclass hierarchy into the flat-ish format that
    the ingestion pipeline (ingest_program_data) already understands.
    """
    entry = sp.entry
    landing = sp.landing_page

    prog: dict = {
        "name": entry.name,
        "slug": entry.slug,
        "category": entry.category,
        "language": entry.language,
        "url": entry.landing_url,
        "is_external": entry.is_external,
    }

    # Landing page content
    if landing and not landing.error:
        prog["title"] = landing.title
        prog["description"] = landing.content[:2000]  # truncate for overview
        prog["sections"] = landing.sections
    else:
        prog["title"] = entry.name
        prog["description"] = ""
        prog["sections"] = {}
        prog["error"] = landing.error if landing else "No landing page"

    # Sub-pages (keyed by suffix, e.g. "admissions", "faqs")
    sub_pages: dict = {}
    for suffix, page in sp.sub_pages.items():
        sub_pages[suffix] = {
            "url": page.url,
            "title": page.title,
            "content": page.content,
            "sections": page.sections,
        }
    prog["sub_pages"] = sub_pages

    # PDF contents
    pdf_list: list[dict] = []
    for pdf in sp.pdf_contents:
        pdf_list.append({
            "source_url": pdf.source_url,
            "text": pdf.full_text,
            "page_count": pdf.page_count,
        })
    prog["pdf_contents"] = pdf_list

    # Structured data extracted by regex (fees, deadlines, etc.)
    prog["structured_data"] = sp.structured_data

    return prog


def main():
    registry = get_registry()
    output_dir = Path(__file__).parent.parent / "data" / "scraped" / "deep"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Deep-scraping {len(registry)} programmes...")
    print("=" * 60)

    with NBSDeepScraper(skip_pdfs=False) as scraper:
        results = scraper.scrape_all(registry)

    # Write individual programme files + combined file
    all_programs: list[dict] = []

    for sp in results:
        prog_dict = programme_to_dict(sp)
        all_programs.append(prog_dict)

        # Individual file
        individual_path = output_dir / f"{sp.entry.slug}.json"
        with open(individual_path, "w", encoding="utf-8") as f:
            json.dump(prog_dict, f, indent=2, ensure_ascii=False)

    # Combined file
    combined_path = output_dir / "all_programs_deep.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(all_programs, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"Done! {len(all_programs)} programmes scraped.")
    print(f"Individual files: {output_dir}/")
    print(f"Combined file:    {combined_path}")

    # Summary
    ok = sum(1 for p in all_programs if "error" not in p)
    errs = len(all_programs) - ok
    total_sub = sum(len(p.get("sub_pages", {})) for p in all_programs)
    total_pdf = sum(len(p.get("pdf_contents", [])) for p in all_programs)
    print(f"\nSuccess: {ok} | Errors: {errs} | Sub-pages: {total_sub} | PDFs: {total_pdf}")


if __name__ == "__main__":
    main()
