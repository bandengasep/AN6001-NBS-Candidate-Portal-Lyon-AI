"""NBS website scraper for degree program information."""

import json
import re
from pathlib import Path
from typing import Any
import httpx
from bs4 import BeautifulSoup


class NBSScraper:
    """Scraper for Nanyang Business School website."""

    BASE_URL = "https://www.ntu.edu.sg/business"

    # Known program pages to scrape
    PROGRAM_URLS = {
        "MBA": "/admissions/graduate-studies/nanyang-mba",
        "EMBA": "/admissions/graduate-studies/executive-mba",
        "MSc Financial Engineering": "/admissions/graduate-studies/msc-financial-engineering",
        "MSc Accountancy": "/admissions/graduate-studies/msc-accountancy",
        "MSc Business Analytics": "/admissions/graduate-studies/msc-business-analytics",
        "MSc Marketing Science": "/admissions/graduate-studies/msc-marketing-science",
        "MSc Asset & Wealth Management": "/admissions/graduate-studies/master-of-science-in-asset-and-wealth-management",
        "PhD": "/admissions/phd-programme",
        "Bachelor of Business": "/admissions/ugadmission",
    }

    def __init__(self):
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; NBSAdvisor/1.0)"
            }
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.close()

    def scrape_page(self, url: str) -> dict[str, Any]:
        """Scrape a single page and extract content.

        Args:
            url: Full URL to scrape

        Returns:
            Dict with extracted content
        """
        try:
            response = self.client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove scripts and styles
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            # Extract title
            title = ""
            title_tag = soup.find("h1")
            if title_tag:
                title = title_tag.get_text(strip=True)

            # Extract main content
            main_content = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile(r"content|main", re.I))

            if main_content:
                content = main_content.get_text(separator="\n", strip=True)
            else:
                content = soup.get_text(separator="\n", strip=True)

            # Clean up content
            content = re.sub(r'\n{3,}', '\n\n', content)
            content = re.sub(r' {2,}', ' ', content)

            # Extract sections
            sections = {}
            for heading in soup.find_all(["h2", "h3"]):
                section_name = heading.get_text(strip=True)
                section_content = []
                for sibling in heading.find_next_siblings():
                    if sibling.name in ["h2", "h3"]:
                        break
                    text = sibling.get_text(strip=True)
                    if text:
                        section_content.append(text)
                if section_content:
                    sections[section_name] = " ".join(section_content)

            return {
                "url": url,
                "title": title,
                "content": content,
                "sections": sections
            }

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {"url": url, "error": str(e)}

    def scrape_program(self, name: str, path: str) -> dict[str, Any]:
        """Scrape a specific program page.

        Args:
            name: Program name
            path: URL path relative to base

        Returns:
            Program data dict
        """
        url = f"{self.BASE_URL}{path}"
        data = self.scrape_page(url)

        if "error" in data:
            return {"name": name, "error": data["error"]}

        # Structure the program data
        program = {
            "name": name,
            "url": url,
            "title": data.get("title", name),
            "description": data.get("content", "")[:2000],  # Limit description length
            "sections": data.get("sections", {}),
            "degree_type": self._extract_degree_type(name),
            "requirements": self._extract_requirements(data),
        }

        return program

    def _extract_degree_type(self, name: str) -> str:
        """Extract degree type from program name."""
        if "MBA" in name.upper():
            return "MBA"
        elif "MSC" in name.upper() or "MASTER" in name.upper():
            return "MSc"
        elif "PHD" in name.upper():
            return "PhD"
        elif "BACHELOR" in name.upper():
            return "Bachelor"
        return "Other"

    def _extract_requirements(self, data: dict) -> dict[str, str]:
        """Extract admission requirements from scraped data."""
        requirements = {}
        sections = data.get("sections", {})

        for key in sections:
            key_lower = key.lower()
            if any(term in key_lower for term in ["admission", "requirement", "eligibility", "apply"]):
                requirements[key] = sections[key]

        return requirements

    def scrape_all_programs(self) -> list[dict[str, Any]]:
        """Scrape all known program pages.

        Returns:
            List of program data dicts
        """
        programs = []
        for name, path in self.PROGRAM_URLS.items():
            print(f"Scraping {name}...")
            program = self.scrape_program(name, path)
            programs.append(program)
        return programs


def scrape_nbs_programs(output_dir: str = "data/scraped") -> list[dict]:
    """Scrape NBS programs and save to JSON files.

    Args:
        output_dir: Directory to save scraped data

    Returns:
        List of scraped program data
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with NBSScraper() as scraper:
        programs = scraper.scrape_all_programs()

    # Save individual program files
    for program in programs:
        if "error" not in program:
            filename = program["name"].lower().replace(" ", "_") + ".json"
            filepath = output_path / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(program, f, indent=2, ensure_ascii=False)

    # Save combined file
    combined_path = output_path / "all_programs.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(programs, f, indent=2, ensure_ascii=False)

    print(f"Scraped {len(programs)} programs to {output_dir}")
    return programs


if __name__ == "__main__":
    scrape_nbs_programs()
