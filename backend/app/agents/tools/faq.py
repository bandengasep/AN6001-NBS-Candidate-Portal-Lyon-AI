"""FAQ tool for common NBS questions."""

from langchain_core.tools import tool

# Common FAQs about NBS
NBS_FAQS = {
    "location": {
        "question": "Where is NBS located?",
        "answer": "Nanyang Business School (NBS) is located at Nanyang Technological University (NTU) in Singapore. The main campus is at 50 Nanyang Avenue, Singapore 639798. NBS is situated in the western part of Singapore with excellent connectivity via MRT and bus services."
    },
    "rankings": {
        "question": "How is NBS ranked?",
        "answer": "Nanyang Business School consistently ranks among the top business schools globally. The MBA programme is ranked in the top 30 globally by Financial Times. NBS is triple-accredited by AACSB, EQUIS, and AMBA, a distinction held by less than 1% of business schools worldwide."
    },
    "application_deadline": {
        "question": "What are the application deadlines?",
        "answer": "Application deadlines vary by programme. Generally, MBA programmes have multiple intake rounds throughout the year. MSc programmes typically have deadlines between January-April for August intake. Please check the specific programme page for exact deadlines or contact admissions."
    },
    "gmat_gre": {
        "question": "Is GMAT/GRE required?",
        "answer": "GMAT or GRE is typically required for MBA and most MSc programmes. Some programmes may offer waivers for candidates with significant work experience or advanced degrees. Check specific programme requirements for details."
    },
    "work_experience": {
        "question": "How much work experience is required?",
        "answer": "Work experience requirements vary: MBA typically requires 3-5 years, EMBA requires 8-10 years of managerial experience, MSc programmes often accept fresh graduates but prefer 1-2 years experience. PhD programmes welcome candidates with strong academic backgrounds."
    },
    "scholarships": {
        "question": "Are scholarships available?",
        "answer": "Yes, NBS offers various scholarships and financial aid options. Merit-based scholarships are available for outstanding candidates. Teaching/Research assistantships are available for PhD students. Check with the admissions office for current scholarship opportunities."
    },
    "language": {
        "question": "What is the language of instruction?",
        "answer": "All programmes at NBS are conducted in English. International students are required to demonstrate English proficiency through TOEFL or IELTS scores unless they have completed prior education in English."
    },
    "international_students": {
        "question": "Does NBS accept international students?",
        "answer": "Yes, NBS welcomes international students from all over the world. The student body is highly diverse with students from 40+ countries. International students can apply for student visas with support from NTU's international services office."
    },
    "career_services": {
        "question": "What career services are available?",
        "answer": "NBS offers comprehensive career services including: dedicated career coaches, resume and interview workshops, networking events with industry partners, on-campus recruitment, internship placements, and alumni mentoring programmes."
    },
    "contact": {
        "question": "How can I contact NBS?",
        "answer": "You can contact NBS through: Email: nbs_admissions@ntu.edu.sg, Phone: +65 6790 4803, Website: www.ntu.edu.sg/business. For specific programme enquiries, please visit the programme page for dedicated contact information."
    }
}


def create_faq_tool():
    """Create the FAQ lookup tool.

    Returns:
        LangChain tool for FAQ lookup
    """

    @tool
    def lookup_faq(topic: str) -> str:
        """Look up frequently asked questions about NBS.

        Use this tool for general questions about NBS that are commonly asked, such as:
        - Location and contact information
        - Rankings and accreditations
        - Application deadlines
        - GMAT/GRE requirements
        - Work experience requirements
        - Scholarships and financial aid
        - Language requirements
        - International students
        - Career services

        Args:
            topic: The FAQ topic to look up (e.g., "scholarships", "rankings", "location")

        Returns:
            Answer to the FAQ
        """
        topic_lower = topic.lower().strip()

        # Direct match
        if topic_lower in NBS_FAQS:
            faq = NBS_FAQS[topic_lower]
            return f"**{faq['question']}**\n\n{faq['answer']}"

        # Keyword matching
        matches = []
        for key, faq in NBS_FAQS.items():
            if (topic_lower in key or
                topic_lower in faq['question'].lower() or
                topic_lower in faq['answer'].lower()):
                matches.append(faq)

        if matches:
            results = []
            for faq in matches[:3]:  # Return up to 3 matches
                results.append(f"**{faq['question']}**\n{faq['answer']}")
            return "\n\n---\n\n".join(results)

        # No match found
        available_topics = ", ".join(NBS_FAQS.keys())
        return f"No FAQ found for '{topic}'. Available topics: {available_topics}. For specific programme questions, please use the search_nbs_knowledge tool."

    return lookup_faq
