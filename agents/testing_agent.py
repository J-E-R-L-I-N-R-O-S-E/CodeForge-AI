from __future__ import annotations

from typing import Optional

from services.llm_service import LLMService


class TestingAgent:
    """
    CodeForge AI Testing Agent.

    Analyzes a generated software project, identifies possible
    defects and missing tests, and produces a structured testing
    assessment.

    The Testing Agent does not modify source code.
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
    ) -> None:
        self.llm_service = llm_service or LLMService()

        self.role = "Software Testing Engineer"

        self.goal = (
            "Analyze the generated project against the confirmed "
            "requirements and approved architecture, identify "
            "implementation defects, missing validations, and "
            "testable requirements, and produce a clear testing "
            "report."
        )

        self.backstory = (
            "You are a senior software testing engineer. "
            "You verify that generated software is consistent with "
            "confirmed requirements and the approved architecture. "
            "You identify functional defects, integration problems, "
            "missing tests, and implementation inconsistencies. "
            "You do not invent new business requirements and you do "
            "not modify source code."
        )

    def generate(
        self,
        prompt: str,
        preferred_provider: Optional[str] = None,
    ) -> str:
        """
        Generate a testing analysis using the central LLM service.
        """

        return self.llm_service.generate(
            prompt=prompt,
            preferred_provider=preferred_provider,
        )


def create_testing_agent() -> TestingAgent:
    """
    Create the CodeForge AI Testing Agent.
    """

    return TestingAgent()