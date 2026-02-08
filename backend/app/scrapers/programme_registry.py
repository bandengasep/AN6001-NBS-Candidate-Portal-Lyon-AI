"""Curated registry of all NBS programmes with metadata.

This replaces the hardcoded PROGRAM_URLS dict in the old scraper.
Auto-discovery from index pages is unreliable (JS-rendered cards),
so we curate the list but make it easy to update.
"""

from dataclasses import dataclass, field


@dataclass
class ProgrammeEntry:
    """A single NBS programme with scraping metadata."""

    name: str
    slug: str
    category: str  # mba, msc, undergraduate, phd, executive_education, china
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

# PhD has its own sub-page pattern
PHD_SUB_PAGES = [
    "curriculum",
    "admission",
    "contact-us",
]

# Some newer programmes only have a subset
MINIMAL_SUB_PAGES = [
    "programme-overview",
    "admissions",
    "faqs",
]


NBS_PROGRAMME_REGISTRY: list[ProgrammeEntry] = [
    # ── MBA Programmes ──────────────────────────────────────────────
    ProgrammeEntry(
        name="Nanyang MBA",
        slug="nanyang-mba",
        category="mba",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-mba",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="Nanyang Professional MBA",
        slug="nanyang-professional-mba",
        category="mba",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-professional-mba/home",
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
        category="mba",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-executive-mba",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="NTU IMBA (Vietnam)",
        slug="ntu-imba",
        category="mba",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/ntu-imba",
        sub_page_suffixes=MINIMAL_SUB_PAGES,
    ),

    # ── MSc Programmes ──────────────────────────────────────────────
    ProgrammeEntry(
        name="MSc Accountancy",
        slug="msc-accountancy",
        category="msc",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-accountancy/home",
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
        name="MSc Business Analytics",
        slug="msc-business-analytics",
        category="msc",
        landing_url="https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-business-analytics",
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
        name="MSc Finance",
        slug="msc-finance",
        category="msc",
        landing_url="https://ntu.sg/nbs-msf",
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
        name="Master in Management",
        slug="master-in-management",
        category="msc",
        landing_url="https://ntu.sg/nbs-mim",
        sub_page_suffixes=DEFAULT_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="NTU-PKU Double Masters in Finance",
        slug="ntu-pku-double-masters",
        category="msc",
        landing_url="https://ntu.sg/nbs-MSCF-DM",
        sub_page_suffixes=MINIMAL_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="MSc Blockchain",
        slug="msc-blockchain",
        category="msc",
        landing_url="https://www.ntu.edu.sg/education/graduate-programme/master-of-science-in-blockchain",
        sub_page_suffixes=MINIMAL_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="MSc Asset and Wealth Management",
        slug="msc-asset-wealth-management",
        category="msc",
        landing_url="https://wmi.edu.sg/programmes/master-of-science-in-asset-wealth-management/",
        is_external=True,
        sub_page_suffixes=[],
    ),

    # ── PhD ──────────────────────────────────────────────────────────
    ProgrammeEntry(
        name="PhD in Business",
        slug="phd-business",
        category="phd",
        landing_url="https://www.ntu.edu.sg/business/admissions/phd-programme",
        sub_page_suffixes=PHD_SUB_PAGES,
    ),

    # ── Undergraduate ────────────────────────────────────────────────
    ProgrammeEntry(
        name="Bachelor of Business",
        slug="bachelor-business",
        category="undergraduate",
        landing_url="https://www.ntu.edu.sg/business/admissions/ugadmission",
        sub_page_suffixes=[],
    ),

    # ── China / ASEAN Programmes ─────────────────────────────────────
    ProgrammeEntry(
        name="Nanyang-SJTU Executive MBA (Chinese)",
        slug="emba-cn",
        category="china",
        landing_url="https://www.ntu.edu.sg/business/admissions/china-programmes-cn/emba-cn",
        language="zh",
        sub_page_suffixes=[],
    ),
    ProgrammeEntry(
        name="Nanyang Executive MBA Singapore (Chinese)",
        slug="embac",
        category="china",
        landing_url="https://www.ntu.edu.sg/business/admissions/china-programmes-cn/embac",
        language="zh",
        sub_page_suffixes=[],
    ),

    # ── Executive Education ──────────────────────────────────────────
    ProgrammeEntry(
        name="Executive Master of Science in Sustainability Management",
        slug="exec-msc-sustainability",
        category="executive_education",
        landing_url="https://www.ntu.edu.sg/business/admissions/NEE/Executive-Master-of-Science-in-Sustainability-Management",
        sub_page_suffixes=MINIMAL_SUB_PAGES,
    ),
    ProgrammeEntry(
        name="FlexiMasters",
        slug="fleximasters",
        category="executive_education",
        landing_url="https://www.ntu.edu.sg/business/admissions/NEE/FlexiMasters",
        sub_page_suffixes=[],
    ),
    ProgrammeEntry(
        name="Public Programmes for Professionals",
        slug="public-programmes",
        category="executive_education",
        landing_url="https://www.ntu.edu.sg/business/admissions/NEE/public-programmes-for-professionals",
        sub_page_suffixes=[],
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
