from __future__ import annotations

from typing import Optional

from services.llm_service import LLMService


class DeveloperAgent:
    """
    CodeForge AI Developer Agent.

    Converts confirmed software requirements and an approved
    architecture into practical starter project code.
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
    ) -> None:
        self.llm_service = (
            llm_service or LLMService()
        )

        self.role = "Software Developer"

        self.goal = (
            "Transform confirmed software requirements and the approved "
            "technical architecture into a practical starter codebase. "
            "Implement only confirmed business functionality while "
            "following the architecture."
        )

        self.backstory = (
            "You are a senior software developer working from validated "
            "requirements and technical architecture. Preserve all "
            "confirmed roles, features, permissions, workflows, and "
            "explicit exclusions. Never invent new business functionality."
        )

    def generate(
        self,
        prompt: str,
        preferred_provider: Optional[str] = None,
    ) -> str:
        """
        Generate implementation output using the central LLM service.
        """

        return self.llm_service.generate(
            prompt=prompt,
            preferred_provider=preferred_provider,
        )


def create_developer_agent() -> DeveloperAgent:
    """
    Create the CodeForge AI Developer Agent.
    """

    return DeveloperAgent()