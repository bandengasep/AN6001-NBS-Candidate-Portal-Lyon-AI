"""Curated registry of NBS Graduate Studies programmes.

Scoped to the 11 programmes managed by the NBS Graduate Studies Office.
Auto-discovery from index pages is unreliable (JS-rendered cards),
so we curate the list but make it easy to update.
"""

from dataclasses import dataclass, field


@dataclass
class ProgrammeEntry:
    """A single NBS programme with scraping metadata."""

    name: str
    slug: str
    category: str  # mba, msc, executive
    landing_url: str
    is_external: bool = False
    language: str = "en"
    sub_page_suffixes: list[str] = field(default_factory=list)


# Standard sub-page suffixes found on most NTU-hosted programme pages
DEFAULT_SUB_PAGES = [
    "programme-overview",
    "admissions",
    "faculty",
    "participants'-experience",
    "career-development",
    "faqs",
    "contact-us",
]

# Some newer programmes only have a subset
MINIMAL_SUB_PAGES = [
    "programme-overview",
    "admissions",
    "faqs",
]


NBS_PROGRAMME_REGISTRY: list[ProgrammeEntry] = [
    # ── MBA Track (4 programmes) ─────────────────────────────────────
    ProgrammeEntry(
        name="Nanyang MBA",
        slug="nanyang-mba",
        category="mba",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-mba",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="Nanyang Fellows MBA",
        slug="nanyang-fellows-mba",
        category="mba",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-fellows-mba/home",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="Nanyang Executive MBA",
        slug="nanyang-executive-mba",
        category="executive",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-executive-mba",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="Nanyang Professional MBA",
        slug="nanyang-professional-mba",
        category="mba",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-professional-mba/home",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),

    # ── Specialized Masters Track (7 programmes) ─────────────────────
    ProgrammeEntry(
        name="MSc Business Analytics",
        slug="msc-business-analytics",
        category="msc",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-business-analytics",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="MSc Finance",
        slug="msc-finance",
        category="msc",
        landing_url="https://ntu.sg/nbs-msf",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="MSc Financial Engineering",
        slug="msc-financial-engineering",
        category="msc",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-financial-engineering/home",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="MSc Marketing Science",
        slug="msc-marketing-science",
        category="msc",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-marketing-science/home",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="MSc Actuarial and Risk Analytics",
        slug="msc-actuarial-risk-analytics",
        category="msc",
        landing_url="https://ntu.sg/nbs-mara",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="MSc Accountancy",
        slug="msc-accountancy",
        category="msc",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-accountancy/home",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="Master in Management",
        slug="master-in-management",
        category="msc",
        landing_url="https://ntu.sg/nbs-mim",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
]


def get_registry() -> list[ProgrammeEntry]:
    """Return the full programme registry."""
    return NBS_PROGRAMME_REGISTRY


def get_registry_by_category(category: str) -> list[ProgrammeEntry]:
    """Return programmes filtered by category."""
    return [p for p in NBS_PROGRAMME_REGISTRY if p.category == category]


def get_registry_by_slug(slug: str) -> ProgrammeEntry | None:
    """Look up a single programme by slug."""
    for p in NBS_PROGRAMME_REGISTRY:
        if p.slug == slug:
            return p
    return None
