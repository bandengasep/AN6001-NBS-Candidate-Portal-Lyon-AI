"""HTML and PDF text cleaning utilities for NBS scraper."""

import re
from bs4 import BeautifulSoup, NavigableString, Tag


# NTU boilerplate selectors to remove before content extraction
_BOILERPLATE_SELECTORS = [
    "script", "style", "noscript", "iframe",
    "nav", "footer",
    "header",
    ".cookie-banner", ".cookie-consent",
    ".social-share", ".social-media",
    ".mega-menu", ".site-header",
    ".breadcrumb", ".breadcrumbs",
    "#onetrust-consent-sdk",
    ".back-to-top",
    "[role='navigation']",
]


def clean_html_content(soup: BeautifulSoup) -> str:
    """Remove NTU boilerplate and extract clean text content.

    Preserves lists and tables as readable text.

    Args:
        soup: BeautifulSoup parsed page

    Returns:
        Cleaned text content
    """
    # Work on a copy so we don't mutate the caller's soup
    soup = BeautifulSoup(str(soup), "html.parser")

    # Remove boilerplate elements
    for selector in _BOILERPLATE_SELECTORS:
        for tag in soup.select(selector):
            tag.decompose()

    # Find main content area
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", class_=re.compile(r"content|main", re.I))
        or soup
    )

    # Convert tables to readable text before extraction
    for table in main.find_all("table"):
        table.replace_with(_table_to_text(table))

    content = main.get_text(separator="\n", strip=True)

    # Clean up excessive whitespace
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = re.sub(r" {2,}", " ", content)
    # Remove very short orphan lines (nav artefacts)
    lines = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
    return "\n".join(lines)


def extract_sections(soup: BeautifulSoup) -> dict[str, str]:
    """Extract H2/H3 sections with nested heading support.

    Args:
        soup: BeautifulSoup parsed page

    Returns:
        Dict mapping section name -> section text content
    """
    # Work on a copy
    soup = BeautifulSoup(str(soup), "html.parser")
    for selector in _BOILERPLATE_SELECTORS:
        for tag in soup.select(selector):
            tag.decompose()

    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", class_=re.compile(r"content|main", re.I))
        or soup
    )

    sections: dict[str, str] = {}

    for heading in main.find_all(["h2", "h3"]):
        section_name = heading.get_text(strip=True)
        if not section_name or len(section_name) > 200:
            continue

        parts: list[str] = []
        for sibling in heading.find_next_siblings():
            if isinstance(sibling, Tag) and sibling.name in ("h2", "h3"):
                break
            text = sibling.get_text(strip=True) if isinstance(sibling, Tag) else str(sibling).strip()
            if text:
                parts.append(text)

        if parts:
            sections[section_name] = " ".join(parts)

    return sections


def extract_structured_data(content: str, sections: dict[str, str]) -> dict[str, str]:
    """Extract structured fields (duration, fees, deadlines) via regex.

    Args:
        content: Full page text
        sections: Extracted section dict

    Returns:
        Dict of extracted structured fields
    """
    combined = content + " " + " ".join(sections.values())
    data: dict[str, str] = {}

    # Duration patterns
    dur = re.search(
        r"(?:duration|length)[:\s]*(\d[\d\-–]?\s*(?:month|year|week|semester)s?(?:\s*(?:full|part)[\s\-]time)?)",
        combined,
        re.I,
    )
    if dur:
        data["duration"] = dur.group(1).strip()

    # Fees / tuition
    fee = re.search(
        r"(?:tuition|fee|cost)[:\s]*(?:S?\$|SGD)\s?[\d,]+(?:\.\d{2})?",
        combined,
        re.I,
    )
    if fee:
        data["fees"] = fee.group(0).strip()

    # Application deadline
    deadline = re.search(
        r"(?:application|submission)\s*deadline[:\s]*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})",
        combined,
        re.I,
    )
    if deadline:
        data["application_deadline"] = deadline.group(1).strip()

    # Intake
    intake = re.search(
        r"(?:intake|start(?:ing)?|commence)[:\s]*((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})",
        combined,
        re.I,
    )
    if intake:
        data["intake"] = intake.group(1).strip()

    return data


def clean_pdf_text(raw_text: str) -> str:
    """Clean extracted PDF text by removing repeated headers/footers and page numbers.

    Args:
        raw_text: Raw text from PDF extraction

    Returns:
        Cleaned text
    """
    lines = raw_text.split("\n")
    cleaned: list[str] = []

    for line in lines:
        stripped = line.strip()
        # Skip page numbers
        if re.match(r"^\d{1,3}$", stripped):
            continue
        # Skip common PDF artefacts
        if re.match(r"^(Page\s+\d+|©|www\.ntu\.edu\.sg|Nanyang Technological University)$", stripped, re.I):
            continue
        if stripped:
            cleaned.append(stripped)

    text = "\n".join(cleaned)
    # Collapse excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    """Find PDF download links in a page.

    Args:
        soup: BeautifulSoup parsed page
        base_url: Base URL for resolving relative links

    Returns:
        List of absolute PDF URLs
    """
    pdf_urls: list[str] = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True).lower()

        is_pdf = (
            href.lower().endswith(".pdf")
            or "brochure" in text
            or "factsheet" in text
            or "fact-sheet" in text
            or "download" in text and ("brochure" in href.lower() or "pdf" in href.lower())
        )

        if is_pdf:
            # Resolve relative URLs
            if href.startswith("/"):
                from urllib.parse import urlparse
                parsed = urlparse(base_url)
                href = f"{parsed.scheme}://{parsed.netloc}{href}"
            elif not href.startswith("http"):
                href = base_url.rstrip("/") + "/" + href

            if href not in pdf_urls:
                pdf_urls.append(href)

    return pdf_urls


def _table_to_text(table: Tag) -> NavigableString:
    """Convert an HTML table to readable plain text."""
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
        if any(cells):
            rows.append(" | ".join(cells))

    return NavigableString("\n".join(rows))
