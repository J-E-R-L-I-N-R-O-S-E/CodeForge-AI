from __future__ import annotations

from typing import Optional

from services.llm_service import LLMService


class ArchitectAgent:
    """
    CodeForge AI Architect Agent.

    Converts finalized software requirements into a technical
    architecture and implementation plan.

    Uses the central LLMService:

        Gemini → OpenRouter → Groq
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
    ) -> None:

        self.llm_service = llm_service or LLMService()

        self.role = "Software Architect"

        self.goal = (
            "Transform validated software requirements into a "
            "practical technical architecture, including technology "
            "choices, system components, database design, API design, "
            "authentication approach, project structure, and "
            "architecture decisions."
        )

        self.backstory = (
            "You are a senior software architect responsible for "
            "turning validated requirements into a clear and "
            "implementable technical design. You must respect the "
            "confirmed requirements, avoid inventing business "
            "features, and make reasonable technical decisions "
            "where architecture choices are required."
        )

    def generate(
        self,
        prompt: str,
        preferred_provider: Optional[str] = None,
    ) -> str:
        """
        Generate an architecture response through the central
        multi-LLM service.
        """

        return self.llm_service.generate(
            prompt=prompt,
            preferred_provider=preferred_provider,
        )


def create_architect_agent() -> ArchitectAgent:
    """Create the CodeForge AI Architect Agent."""

    return ArchitectAgent()