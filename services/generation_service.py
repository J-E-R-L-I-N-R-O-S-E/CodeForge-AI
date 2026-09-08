from __future__ import annotations

from typing import Dict, Any

from tools.code_generator import CodeGenerator
from tools.project_packager import ProjectPackager


class GenerationService:
    """
    Coordinates CodeForge AI project generation.

    Workflow:
        Developer output
            ↓
        CodeGenerator
            ↓
        Project directory
            ↓
        ProjectPackager
            ↓
        ZIP archive
    """

    def __init__(
        self,
        output_root: str = "outputs",
    ) -> None:
        self.output_root = output_root

        self.code_generator = CodeGenerator(
            output_root=output_root
        )

        self.project_packager = ProjectPackager(
            output_root=output_root
        )

    def generate_project(
        self,
        project_name: str,
        developer_output: str,
    ) -> Dict[str, Any]:
        """
        Generate the project files and create a ZIP archive.

        Returns:
            Generation summary containing project path,
            file count, generated files, and ZIP path.
        """

        generation_result = self.code_generator.generate_project(
            project_name=project_name,
            developer_output=developer_output,
        )

        zip_path = self.project_packager.create_zip(
            project_name=project_name,
            project_directory=generation_result["project_path"],
        )

        generation_result["zip_path"] = str(zip_path)

        return generation_result


def create_generation_service(
    output_root: str = "outputs",
) -> GenerationService:
    """
    Create the CodeForge AI Generation Service.
    """

    return GenerationService(
        output_root=output_root
    )