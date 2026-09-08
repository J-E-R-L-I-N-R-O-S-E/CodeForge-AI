from __future__ import annotations

from typing import Dict, Any

from agents.testing_agent import create_testing_agent
from services.project_inspector import create_project_inspector
from tasks.testing_tasks import create_testing_prompt


class TestingService:
    """
    Coordinates the CodeForge AI Testing workflow.

    Workflow:
        Generated Project
            ↓
        ProjectInspector
            ↓
        Testing Agent
            ↓
        Testing Report
    """

    def __init__(self) -> None:
        self.testing_agent = create_testing_agent()

    def analyze_project(
        self,
        project_path: str,
        confirmed_requirements: str,
        architecture: str,
        project_idea: str = "",
    ) -> str:
        """
        Inspect a generated project and ask the Testing Agent
        to evaluate it.
        """

        inspector = create_project_inspector(
            project_path
        )

        inspection = inspector.inspect()

        prompt = create_testing_prompt(
            project_idea=project_idea,
            confirmed_requirements=confirmed_requirements,
            architecture=architecture,
            project_structure=inspection["project_structure"],
            project_code=inspection["project_code"],
        )

        return self.testing_agent.generate(
            prompt=prompt,
            preferred_provider="openrouter",
        )

    def inspect_project(
        self,
        project_path: str,
    ) -> Dict[str, str]:
        """
        Return the deterministic project inspection result.
        """

        inspector = create_project_inspector(
            project_path
        )

        return inspector.inspect()


def create_testing_service() -> TestingService:
    """
    Create the CodeForge AI Testing Service.
    """

    return TestingService()