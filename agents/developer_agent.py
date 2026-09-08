from __future__ import annotations

from typing import Optional

from services.llm_service import LLMService


class DeveloperAgent:
    """
    CodeForge AI Developer Agent.

    Converts confirmed software requirements and an approved
    architecture into practical starter project code.

    The Developer Agent must:
    - follow confirmed requirements
    - follow the architecture
    - preserve roles, permissions, and workflows
    - avoid inventing business functionality
    - distinguish technical implementation from business requirements
    """

    def __init__(self, llm_service: Optional[LLMService] = None) -> None:
        self.llm_service = llm_service or LLMService()

        self.role = "Software Developer"

        self.goal = (
            "Transform confirmed software requirements and the approved "
            "technical architecture into a practical starter codebase. "
            "Implement only confirmed business functionality while "
            "following the architecture and making reasonable technical "
            "implementation decisions."
        )

        self.backstory = (
            "You are a senior software developer working from validated "
            "requirements and a technical architecture. You must treat "
            "confirmed requirements as authoritative, preserve all "
            "confirmed roles, features, permissions, workflows, and "
            "explicit exclusions, and never invent new business "
            "functionality merely because it is common in similar systems."
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