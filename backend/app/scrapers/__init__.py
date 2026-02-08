"""Web scrapers module."""

from .deep_scraper import NBSDeepScraper, ScrapedPage, ScrapedProgramme
from .programme_registry import (
    ProgrammeEntry,
    get_registry,
    get_registry_by_category,
    get_registry_by_slug,
)

# Legacy scraper still available for backward compatibility
from .nbs_scraper_legacy import NBSScraper, scrape_nbs_programs

__all__ = [
    "NBSDeepScraper",
    "ScrapedPage",
    "ScrapedProgramme",
    "ProgrammeEntry",
    "get_registry",
    "get_registry_by_category",
    "get_registry_by_slug",
    # Legacy
    "NBSScraper",
    "scrape_nbs_programs",
]
