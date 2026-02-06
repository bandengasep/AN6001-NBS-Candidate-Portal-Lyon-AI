"""Main NBS Advisor Agent using LangChain."""

import uuid
from typing import Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from app.config import get_settings
from app.agents.tools import create_rag_tool, create_compare_tool, create_faq_tool
from app.db.supabase import get_chat_history, store_chat_message


# System prompt for the NBS Advisor
NBS_ADVISOR_SYSTEM_PROMPT = """You are an AI advisor for Nanyang Business School (NBS), one of Asia's top business schools located at Nanyang Technological University (NTU) in Singapore.

Your role is to help prospective students, current students, and other inquirers with information about:
- NBS degree programmes (MBA, EMBA, MSc programmes, PhD, Bachelor of Business)
- Admission requirements and application processes
- Programme curriculum and structure
- Career outcomes and opportunities
- Campus life and student experience
- Scholarships and financial aid
- General information about NBS and NTU

Guidelines:
1. Be helpful, professional, and informative
2. Use the tools available to search for accurate, up-to-date information
3. When comparing programmes, use the compare_programs tool
4. For general FAQs, check the FAQ tool first
5. For specific programme details, use the search_nbs_knowledge tool
6. If you're unsure about something, say so and suggest contacting NBS directly
7. Always encourage users to verify important information (deadlines, fees) on the official NBS website
8. Be concise but thorough in your responses

Remember: You represent NBS, so maintain a professional and welcoming tone."""


class NBSAdvisorAgent:
    """NBS Degree Advisor Agent."""

    def __init__(self):
        """Initialize the agent with tools and LLM."""
        settings = get_settings()

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=settings.chat_model,
            temperature=0.7,
            api_key=settings.openai_api_key
        )

        # Create tools
        self.tools = [
            create_rag_tool(),
            create_compare_tool(),
            create_faq_tool()
        ]

        # Create agent using LangChain v1 API
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=NBS_ADVISOR_SYSTEM_PROMPT
        )

    async def chat(
        self,
        message: str,
        conversation_id: str | None = None
    ) -> dict[str, Any]:
        """Process a chat message and return a response.

        Args:
            message: User message
            conversation_id: Optional conversation ID for history

        Returns:
            Dict with response, conversation_id, and sources
        """
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        # Load chat history
        chat_history = []
        try:
            history_records = await get_chat_history(conversation_id, limit=10)
            for record in history_records:
                chat_history.append({
                    "role": record["role"],
                    "content": record["content"]
                })
        except Exception:
            # Continue without history if loading fails
            pass

        # Store user message
        try:
            await store_chat_message(conversation_id, "user", message)
        except Exception:
            pass

        # Run agent
        try:
            # Build messages list
            messages = []
            for msg in chat_history:
                messages.append((msg["role"], msg["content"]))
            messages.append(("user", message))

            # Invoke agent
            result = await self.agent.ainvoke({"messages": messages})

            # Extract response from result
            response = ""
            if "messages" in result:
                # Get the last AI message
                for msg in reversed(result["messages"]):
                    if hasattr(msg, "content") and msg.type == "ai":
                        response = msg.content
                        break

            if not response:
                response = "I apologize, but I couldn't generate a response. Please try again."

            # Store assistant response
            try:
                await store_chat_message(conversation_id, "assistant", response)
            except Exception:
                pass

            return {
                "response": response,
                "conversation_id": conversation_id,
                "sources": []
            }

        except Exception as e:
            error_msg = f"I encountered an error while processing your request: {str(e)}. Please try again or rephrase your question."
            return {
                "response": error_msg,
                "conversation_id": conversation_id,
                "sources": []
            }


# Global agent instance
_agent_instance: NBSAdvisorAgent | None = None


def create_nbs_agent() -> NBSAdvisorAgent:
    """Get or create the NBS Advisor agent singleton.

    Returns:
        NBSAdvisorAgent instance
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = NBSAdvisorAgent()
    return _agent_instance
