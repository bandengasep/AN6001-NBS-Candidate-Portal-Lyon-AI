"""Deep crawling engine for NBS programme pages.

Scrapes landing pages, sub-pages, and PDF brochures for each programme
in the registry, with rate limiting, retries, and error isolation.
"""

import logging
import time
from dataclasses import dataclass, field
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from .content_cleaner import (
    clean_html_content,
    extract_pdf_links,
    extract_sections,
    extract_structured_data,
)
from .pdf_extractor import PDFContent, extract_all_pdfs
from .programme_registry import ProgrammeEntry

logger = logging.getLogger(__name__)


@dataclass
class ScrapedPage:
    """Content extracted from a single web page."""

    url: str
    title: str
    content: str
    sections: dict[str, str] = field(default_factory=dict)
    links: list[str] = field(default_factory=list)
    pdf_links: list[str] = field(default_factory=list)
    tables: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass
class ScrapedProgramme:
    """All scraped data for one programme."""

    entry: ProgrammeEntry
    landing_page: ScrapedPage | None = None
    sub_pages: dict[str, ScrapedPage] = field(default_factory=dict)
    pdf_contents: list[PDFContent] = field(default_factory=list)
    structured_data: dict[str, str] = field(default_factory=dict)


# Transient HTTP status codes worth retrying
_RETRYABLE_STATUSES = {429, 500, 502, 503}

# Max retries with exponential backoff
_MAX_RETRIES = 3
_BACKOFF_BASE = 2.0

# Delay between requests (seconds)
_REQUEST_DELAY = 1.5


class NBSDeepScraper:
    """Deep web scraper for NBS programme pages."""

    def __init__(
        self,
        request_delay: float = _REQUEST_DELAY,
        pdf_download_dir: str = "data/pdfs",
        skip_pdfs: bool = False,
    ):
        self.request_delay = request_delay
        self.pdf_download_dir = pdf_download_dir
        self.skip_pdfs = skip_pdfs
        self._client = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; NBSAdvisor/2.0; +https://ntu.edu.sg)"
            },
        )
        self._last_request_time: float = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._client.close()

    def close(self):
        self._client.close()

    # ── HTTP layer ────────────────────────────────────────────────────

    def _rate_limit(self):
        """Enforce minimum delay between HTTP requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)

    def _fetch(self, url: str) -> httpx.Response | None:
        """Fetch a URL with retries and rate limiting.

        Returns:
            httpx.Response or None on persistent failure
        """
        for attempt in range(_MAX_RETRIES):
            self._rate_limit()
            self._last_request_time = time.time()

            try:
                response = self._client.get(url)

                if response.status_code in _RETRYABLE_STATUSES:
                    wait = _BACKOFF_BASE ** attempt
                    logger.warning(
                        "HTTP %d for %s - retrying in %.1fs (attempt %d/%d)",
                        response.status_code, url, wait, attempt + 1, _MAX_RETRIES,
                    )
                    time.sleep(wait)
                    continue

                response.raise_for_status()
                return response

            except httpx.TimeoutException:
                wait = _BACKOFF_BASE ** attempt
                logger.warning("Timeout for %s - retrying in %.1fs", url, wait)
                time.sleep(wait)
            except httpx.HTTPStatusError as e:
                logger.error("HTTP error for %s: %s", url, e)
                return None
            except httpx.RequestError as e:
                logger.error("Request error for %s: %s", url, e)
                return None

        logger.error("All %d retries exhausted for %s", _MAX_RETRIES, url)
        return None

    # ── Page scraping ─────────────────────────────────────────────────

    def _scrape_response(self, url: str, response: httpx.Response) -> ScrapedPage:
        """Parse an already-fetched response into a ScrapedPage."""
        final_url = str(response.url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title = ""
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True)

        # Content
        content = clean_html_content(soup)

        # Sections
        sections = extract_sections(soup)

        # Links on page
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/"):
                parsed = urlparse(final_url)
                href = f"{parsed.scheme}://{parsed.netloc}{href}"
            if href.startswith("http"):
                links.append(href)

        # PDF links
        pdf_links = extract_pdf_links(soup, final_url)

        return ScrapedPage(
            url=final_url,
            title=title,
            content=content,
            sections=sections,
            links=links,
            pdf_links=pdf_links,
        )

    def scrape_page(self, url: str) -> ScrapedPage:
        """Fetch and parse a single URL.

        Args:
            url: Full URL to scrape

        Returns:
            ScrapedPage with extracted content (error field set on failure)
        """
        response = self._fetch(url)
        if response is None:
            return ScrapedPage(url=url, title="", content="", error="Failed to fetch")

        return self._scrape_response(url, response)

    # ── Sub-page discovery ────────────────────────────────────────────

    def discover_sub_pages(
        self, entry: ProgrammeEntry, landing_html: str
    ) -> list[tuple[str, str]]:
        """Find programme sub-page URLs from landing page + registry patterns.

        Args:
            entry: Programme registry entry
            landing_html: HTML of the landing page

        Returns:
            List of (suffix_label, full_url) tuples
        """
        if entry.is_external:
            return []

        base_url = entry.landing_url.rstrip("/")
        # Strip trailing /home suffix for building sub-page URLs
        if base_url.endswith("/home"):
            base_url = base_url[: -len("/home")]

        found: list[tuple[str, str]] = []
        seen_urls: set[str] = set()

        # 1. Use known suffixes from registry
        for suffix in entry.sub_page_suffixes:
            url = f"{base_url}/{suffix}"
            if url not in seen_urls:
                found.append((suffix, url))
                seen_urls.add(url)

        # 2. Also scan the HTML for links that look like sub-pages
        soup = BeautifulSoup(landing_html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            # Strip fragment identifiers
            if "#" in href:
                href = href.split("#")[0]
            if not href:
                continue
            # Resolve relative
            if href.startswith("/"):
                parsed = urlparse(entry.landing_url)
                href = f"{parsed.scheme}://{parsed.netloc}{href}"

            # Must be under the same programme path
            if not href.startswith(base_url + "/"):
                continue
            # Must be one level deep
            remainder = href[len(base_url) + 1 :].strip("/")
            if "/" in remainder or not remainder:
                continue
            if remainder in ("home",):
                continue
            if href not in seen_urls:
                found.append((remainder, href))
                seen_urls.add(href)

        return found

    # ── Programme-level scraping ──────────────────────────────────────

    def scrape_programme(self, entry: ProgrammeEntry) -> ScrapedProgramme:
        """Full deep crawl for a single programme.

        Scrapes landing page, all sub-pages, and PDF brochures.

        Args:
            entry: Programme registry entry

        Returns:
            ScrapedProgramme with all collected data
        """
        result = ScrapedProgramme(entry=entry)
        logger.info("Scraping programme: %s", entry.name)

        # 1. Landing page - fetch once, reuse for both parsing and link discovery
        response = self._fetch(entry.landing_url)
        if response is None:
            landing = ScrapedPage(url=entry.landing_url, title="", content="", error="Failed to fetch")
            result.landing_page = landing
            logger.error("Failed to scrape landing page for %s", entry.name)
            return result

        landing = self._scrape_response(entry.landing_url, response)
        result.landing_page = landing
        all_pdf_links = list(landing.pdf_links)

        # 2. Sub-pages - discover from the same response HTML
        sub_page_targets = self.discover_sub_pages(entry, response.text)

        for suffix, url in sub_page_targets:
            logger.info("  Sub-page: %s -> %s", suffix, url)
            page = self.scrape_page(url)
            if page.error:
                logger.warning("  Failed sub-page %s: %s", suffix, page.error)
                continue
            result.sub_pages[suffix] = page
            all_pdf_links.extend(page.pdf_links)

        # 3. PDFs
        if not self.skip_pdfs and all_pdf_links:
            unique_pdfs = list(dict.fromkeys(all_pdf_links))  # deduplicate, preserve order
            logger.info("  Extracting %d PDF(s)...", len(unique_pdfs))
            result.pdf_contents = extract_all_pdfs(unique_pdfs, self.pdf_download_dir)

        # 4. Structured data extraction
        all_content = landing.content
        all_sections = dict(landing.sections)
        for page in result.sub_pages.values():
            all_content += " " + page.content
            all_sections.update(page.sections)
        result.structured_data = extract_structured_data(all_content, all_sections)

        return result

    def scrape_all(
        self, registry: list[ProgrammeEntry]
    ) -> list[ScrapedProgramme]:
        """Iterate all programmes with progress reporting.

        Individual programme failures are logged and skipped.

        Args:
            registry: List of programme entries to scrape

        Returns:
            List of ScrapedProgramme results
        """
        results: list[ScrapedProgramme] = []
        total = len(registry)

        for i, entry in enumerate(registry, 1):
            print(f"[{i}/{total}] Scraping {entry.name}...")
            try:
                programme = self.scrape_programme(entry)
                results.append(programme)

                # Progress summary
                n_sub = len(programme.sub_pages)
                n_pdf = len(programme.pdf_contents)
                status = "OK" if programme.landing_page and not programme.landing_page.error else "FAILED"
                print(f"  -> {status} | {n_sub} sub-pages | {n_pdf} PDFs")

            except Exception as e:
                logger.error("Unexpected error scraping %s: %s", entry.name, e, exc_info=True)
                print(f"  -> ERROR: {e}")

        return results
