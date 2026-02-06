"""Program comparison tool for the NBS Advisor agent."""

from langchain_core.tools import tool
from app.rag.retriever import retrieve_comparison_documents
from app.db.supabase import get_supabase_client


def create_compare_tool():
    """Create the program comparison tool.

    Returns:
        LangChain tool for comparing programs
    """

    @tool
    async def compare_programs(program_names: str) -> str:
        """Compare two or more NBS degree programs.

        Use this tool when a user wants to compare different programs, such as:
        - MBA vs EMBA
        - Different MSc programs
        - Comparing admission requirements
        - Comparing career outcomes

        Args:
            program_names: Comma-separated list of program names to compare
                         (e.g., "MBA, EMBA" or "MSc Business Analytics, MSc Financial Engineering")

        Returns:
            Comparison information about the programs
        """
        try:
            # Parse program names
            programs = [p.strip() for p in program_names.split(",")]

            if len(programs) < 2:
                return "Please provide at least two programs to compare, separated by commas."

            # Get program data from database
            client = get_supabase_client()
            program_data = []

            for prog_name in programs:
                result = client.table("programs").select("*").ilike(
                    "name", f"%{prog_name}%"
                ).limit(1).execute()

                if result.data:
                    program_data.append(result.data[0])

            # Get additional context from RAG
            rag_results = await retrieve_comparison_documents(programs)

            # Format comparison
            comparison = []
            comparison.append(f"## Comparison: {' vs '.join(programs)}\n")

            # Structured program data
            if program_data:
                comparison.append("### Program Overview\n")
                for prog in program_data:
                    comparison.append(f"**{prog['name']}** ({prog['degree_type']})")
                    if prog.get('duration'):
                        comparison.append(f"- Duration: {prog['duration']}")
                    if prog.get('description'):
                        comparison.append(f"- {prog['description'][:300]}...")
                    comparison.append("")

            # RAG context
            if rag_results:
                comparison.append("### Additional Details\n")
                for doc in rag_results[:4]:
                    content = doc.get("content", "")
                    metadata = doc.get("metadata", {})
                    program = metadata.get("program", "")
                    if content:
                        comparison.append(f"**{program}**: {content[:400]}...\n")

            if not program_data and not rag_results:
                return f"Could not find detailed information for: {', '.join(programs)}. Please check the program names and try again."

            return "\n".join(comparison)

        except Exception as e:
            return f"Error comparing programs: {str(e)}"

    return compare_programs
