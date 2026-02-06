"""RAG retrieval tool for the NBS Advisor agent."""

from langchain_core.tools import tool
from app.rag.retriever import retrieve_relevant_documents


def create_rag_tool():
    """Create the RAG retrieval tool.

    Returns:
        LangChain tool for RAG retrieval
    """

    @tool
    async def search_nbs_knowledge(query: str) -> str:
        """Search the NBS knowledge base for information about degree programs.

        Use this tool to find specific information about NBS programs, including:
        - Program descriptions and curriculum
        - Admission requirements and deadlines
        - Career outcomes and alumni information
        - Fees and financial aid
        - Faculty and research areas

        Args:
            query: The search query about NBS programs

        Returns:
            Relevant information from the knowledge base
        """
        try:
            documents = await retrieve_relevant_documents(query, match_count=4)

            if not documents:
                return "No relevant information found in the knowledge base. Please try rephrasing your question or ask about specific NBS programs."

            # Format results
            results = []
            for i, doc in enumerate(documents, 1):
                content = doc.get("content", "")
                metadata = doc.get("metadata", {})
                program = metadata.get("program", "NBS")
                doc_type = metadata.get("type", "general")
                similarity = doc.get("similarity", 0)

                results.append(
                    f"[Source {i}] ({program} - {doc_type}, relevance: {similarity:.2f})\n{content}"
                )

            return "\n\n---\n\n".join(results)

        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"

    return search_nbs_knowledge
