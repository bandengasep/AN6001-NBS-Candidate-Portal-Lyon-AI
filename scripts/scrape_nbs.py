#!/usr/bin/env python3
"""Script to scrape NBS website for degree program information."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.scrapers.nbs_scraper_legacy import scrape_nbs_programs


def main():
    """Run the NBS scraper."""
    print("Starting NBS website scraper...")
    print("=" * 50)

    output_dir = Path(__file__).parent.parent / "data" / "scraped"
    programs = scrape_nbs_programs(str(output_dir))

    print("=" * 50)
    print(f"Scraping complete!")
    print(f"Successfully scraped: {len([p for p in programs if 'error' not in p])} programs")
    print(f"Errors: {len([p for p in programs if 'error' in p])} programs")

    for program in programs:
        status = "OK" if "error" not in program else f"ERROR: {program.get('error', 'Unknown')}"
        print(f"  - {program['name']}: {status}")


if __name__ == "__main__":
    main()
