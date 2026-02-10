"""Hand-off tool for connecting users with NBS advisors."""

from langchain_core.tools import tool


def create_handoff_tool():
    """Create the advisor hand-off tool.

    Returns:
        LangChain tool for scheduling advisor sessions
    """

    @tool
    def schedule_advisor_session(reason: str) -> str:
        """Use this when the user wants to speak with a real NBS advisor or when you cannot find the information they need in the knowledge base. This will show the user a form to schedule a 1-on-1 session.

        Args:
            reason: Brief description of why the hand-off is needed (e.g. "user wants to discuss scholarship options in detail" or "cannot find specific intake deadline")

        Returns:
            Confirmation message for Lyon to relay to the user
        """
        return "Advisor session request noted. A scheduling form will appear for the student. Let them know they can fill in their details and an NBS advisor will reach out to them."

    return schedule_advisor_session
