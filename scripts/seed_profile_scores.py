"""Seed spider chart profile scores for all programmes.

Each programme gets scores on 7 axes (1-5):
- quantitative: Math/stats intensity
- experience: Work experience expected
- leadership: Leadership focus
- tech_analytics: Tech/data orientation
- business_domain: Business breadth (1=general, 5=specialized/research)
- career_ambition: Career trajectory (1=explore, 5=research/academia)
- study_flexibility: Study mode flexibility (1=full-time intensive, 5=part-time/flexible)

Run: "/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" scripts/seed_profile_scores.py
"""

import os
import sys
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

from supabase import create_client

PROFILE_SCORES = {
    # MBA programmes
    "Nanyang MBA": {
        "quantitative": 3, "experience": 4, "leadership": 5,
        "tech_analytics": 3, "business_domain": 1, "career_ambition": 4, "study_flexibility": 2
    },
    "Nanyang Executive MBA": {
        "quantitative": 3, "experience": 5, "leadership": 5,
        "tech_analytics": 2, "business_domain": 1, "career_ambition": 4, "study_flexibility": 4
    },
    "Nanyang Executive MBA Singapore (Chinese)": {
        "quantitative": 3, "experience": 5, "leadership": 5,
        "tech_analytics": 2, "business_domain": 1, "career_ambition": 4, "study_flexibility": 4
    },
    "Nanyang-SJTU Executive MBA (Chinese)": {
        "quantitative": 3, "experience": 5, "leadership": 5,
        "tech_analytics": 2, "business_domain": 1, "career_ambition": 4, "study_flexibility": 4
    },
    "Nanyang Professional MBA": {
        "quantitative": 3, "experience": 4, "leadership": 4,
        "tech_analytics": 3, "business_domain": 1, "career_ambition": 4, "study_flexibility": 4
    },
    "Nanyang Fellows MBA": {
        "quantitative": 3, "experience": 3, "leadership": 4,
        "tech_analytics": 3, "business_domain": 1, "career_ambition": 4, "study_flexibility": 2
    },
    "NTU IMBA (Vietnam)": {
        "quantitative": 3, "experience": 3, "leadership": 3,
        "tech_analytics": 3, "business_domain": 1, "career_ambition": 3, "study_flexibility": 2
    },
    # MSc programmes
    "MSc Business Analytics": {
        "quantitative": 5, "experience": 2, "leadership": 2,
        "tech_analytics": 5, "business_domain": 4, "career_ambition": 3, "study_flexibility": 2
    },
    "MSc Financial Engineering": {
        "quantitative": 5, "experience": 2, "leadership": 2,
        "tech_analytics": 4, "business_domain": 3, "career_ambition": 3, "study_flexibility": 2
    },
    "MSc Accountancy": {
        "quantitative": 4, "experience": 2, "leadership": 2,
        "tech_analytics": 2, "business_domain": 3, "career_ambition": 2, "study_flexibility": 2
    },
    "MSc Marketing Science": {
        "quantitative": 4, "experience": 2, "leadership": 2,
        "tech_analytics": 3, "business_domain": 2, "career_ambition": 3, "study_flexibility": 2
    },
    "MSc Asset and Wealth Management": {
        "quantitative": 4, "experience": 3, "leadership": 3,
        "tech_analytics": 3, "business_domain": 3, "career_ambition": 3, "study_flexibility": 2
    },
    "MSc Finance": {
        "quantitative": 4, "experience": 2, "leadership": 2,
        "tech_analytics": 3, "business_domain": 3, "career_ambition": 3, "study_flexibility": 2
    },
    "MSc Blockchain": {
        "quantitative": 5, "experience": 2, "leadership": 2,
        "tech_analytics": 5, "business_domain": 4, "career_ambition": 3, "study_flexibility": 2
    },
    "MSc Actuarial and Risk Analytics": {
        "quantitative": 5, "experience": 2, "leadership": 2,
        "tech_analytics": 4, "business_domain": 3, "career_ambition": 3, "study_flexibility": 2
    },
    "NTU-PKU Double Masters in Finance": {
        "quantitative": 4, "experience": 2, "leadership": 2,
        "tech_analytics": 3, "business_domain": 3, "career_ambition": 3, "study_flexibility": 2
    },
    "Master in Management": {
        "quantitative": 3, "experience": 2, "leadership": 2,
        "tech_analytics": 2, "business_domain": 1, "career_ambition": 2, "study_flexibility": 2
    },
    "Executive Master of Science in Sustainability Management": {
        "quantitative": 3, "experience": 4, "leadership": 3,
        "tech_analytics": 2, "business_domain": 2, "career_ambition": 3, "study_flexibility": 4
    },
    # PhD
    "PhD in Business": {
        "quantitative": 5, "experience": 2, "leadership": 2,
        "tech_analytics": 4, "business_domain": 5, "career_ambition": 5, "study_flexibility": 1
    },
    # Bachelor
    "Bachelor of Business": {
        "quantitative": 2, "experience": 1, "leadership": 2,
        "tech_analytics": 2, "business_domain": 1, "career_ambition": 1, "study_flexibility": 1
    },
    # Professional
    "FlexiMasters": {
        "quantitative": 2, "experience": 3, "leadership": 2,
        "tech_analytics": 2, "business_domain": 2, "career_ambition": 2, "study_flexibility": 5
    },
    "Public Programmes for Professionals": {
        "quantitative": 2, "experience": 3, "leadership": 2,
        "tech_analytics": 2, "business_domain": 2, "career_ambition": 2, "study_flexibility": 5
    },
}


def main():
    url = os.environ["SUPABASE_URL"]
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ["SUPABASE_KEY"]
    supabase = create_client(url, key)

    # Get all programmes
    result = supabase.table("programs").select("id, name").execute()
    if not result.data:
        print("No programmes found in database!")
        return

    updated = 0
    for prog in result.data:
        name = prog["name"]
        scores = PROFILE_SCORES.get(name)
        if scores:
            supabase.table("programs").update(
                {"profile_scores": json.dumps(scores)}
            ).eq("id", prog["id"]).execute()
            print(f"  Updated: {name}")
            updated += 1
        else:
            print(f"  Skipped (no scores defined): {name}")

    print(f"\nDone! Updated {updated}/{len(result.data)} programmes.")


if __name__ == "__main__":
    main()
