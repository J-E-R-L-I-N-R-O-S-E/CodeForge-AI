from __future__ import annotations

from typing import Optional

from services.llm_service import LLMService


class RequirementAgent:
    """
    CodeForge AI Requirement Agent.

    Uses the central LLMService for:
        Gemini → OpenRouter → Groq
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
    ) -> None:

        self.llm_service = llm_service or LLMService()

        self.role = "Software Requirements Analyst"

        self.goal = (
            "Analyze a user's software idea strictly from the "
            "information provided by the user, distinguish explicit "
            "information from inferences, identify missing "
            "requirements, and generate only necessary clarification "
            "questions."
        )

        self.backstory = (
            "You are a senior software requirements analyst. "
            "Your job is to convert vague project ideas into reliable "
            "requirements without inventing facts. Carefully separate "
            "what the user explicitly stated from what can only be "
            "inferred and what is still unknown."
        )

    def generate(
        self,
        prompt: str,
        preferred_provider: Optional[str] = None,
    ) -> str:

        return self.llm_service.generate(
            prompt=prompt,
            preferred_provider=preferred_provider,
        )


def create_requirement_agent() -> RequirementAgent:
    """Create the CodeForge AI Requirement Agent."""

    return RequirementAgent()