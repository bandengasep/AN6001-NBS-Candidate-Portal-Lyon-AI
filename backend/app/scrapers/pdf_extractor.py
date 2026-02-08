"""PDF download and text extraction for NBS programme brochures."""

import hashlib
import logging
from dataclasses import dataclass, field
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

try:
    import pdfplumber
except ImportError:
    pdfplumber = None  # type: ignore[assignment]
    logger.warning("pdfplumber not installed – PDF extraction disabled. Run: pip install pdfplumber")


@dataclass
class PDFContent:
    """Extracted content from a single PDF."""

    source_url: str
    file_path: str
    full_text: str
    page_count: int
    tables: list[list[list[str]]] = field(default_factory=list)


def download_pdf(url: str, download_dir: str | Path) -> Path | None:
    """Stream-download a PDF to disk with deterministic filename.

    Args:
        url: Remote PDF URL
        download_dir: Local directory to save into

    Returns:
        Path to downloaded file, or None on failure
    """
    download_dir = Path(download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    # Deterministic filename from URL
    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
    # Try to preserve a readable suffix from the URL
    url_path = url.split("?")[0]
    name_part = url_path.split("/")[-1] if "/" in url_path else "document"
    if not name_part.lower().endswith(".pdf"):
        name_part += ".pdf"
    filename = f"{url_hash}_{name_part}"
    dest = download_dir / filename

    # Skip if already downloaded
    if dest.exists() and dest.stat().st_size > 0:
        logger.info("PDF already downloaded: %s", dest.name)
        return dest

    try:
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            with client.stream("GET", url) as response:
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                if "pdf" not in content_type and "octet-stream" not in content_type:
                    logger.warning("URL %s returned content-type %s, skipping", url, content_type)
                    return None

                with open(dest, "wb") as f:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)

        logger.info("Downloaded PDF: %s (%d KB)", dest.name, dest.stat().st_size // 1024)
        return dest

    except Exception as e:
        logger.error("Failed to download PDF %s: %s", url, e)
        # Clean up partial download
        if dest.exists():
            dest.unlink()
        return None


def extract_pdf_text(pdf_path: str | Path) -> PDFContent | None:
    """Extract text and tables from a PDF file using pdfplumber.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        PDFContent dataclass, or None on failure
    """
    if pdfplumber is None:
        logger.error("pdfplumber not installed – cannot extract PDF text")
        return None

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        logger.error("PDF file not found: %s", pdf_path)
        return None

    try:
        pages_text: list[str] = []
        all_tables: list[list[list[str]]] = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                pages_text.append(text)

                # Extract tables
                for table in page.extract_tables():
                    if table:
                        cleaned = [
                            [cell or "" for cell in row]
                            for row in table
                            if row
                        ]
                        if cleaned:
                            all_tables.append(cleaned)

        full_text = "\n\n".join(pages_text)

        if not full_text.strip():
            logger.warning("PDF %s yielded no text (may be image-based)", pdf_path.name)
            return None

        return PDFContent(
            source_url="",  # Caller sets this
            file_path=str(pdf_path),
            full_text=full_text,
            page_count=len(pages_text),
            tables=all_tables,
        )

    except Exception as e:
        logger.error("Failed to extract text from %s: %s", pdf_path.name, e)
        return None


def extract_all_pdfs(
    urls: list[str],
    download_dir: str | Path,
) -> list[PDFContent]:
    """Batch download and extract text from multiple PDFs.

    Skips password-protected or corrupt files with a warning.

    Args:
        urls: List of PDF URLs
        download_dir: Local directory for downloads

    Returns:
        List of successfully extracted PDFContent objects
    """
    results: list[PDFContent] = []

    for url in urls:
        path = download_pdf(url, download_dir)
        if path is None:
            continue

        content = extract_pdf_text(path)
        if content is not None:
            content.source_url = url
            results.append(content)

    return results
