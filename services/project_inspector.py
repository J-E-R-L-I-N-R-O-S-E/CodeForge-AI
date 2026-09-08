from __future__ import annotations

from pathlib import Path
from typing import Dict


class ProjectInspector:
    """
    Reads a generated CodeForge project and prepares
    its structure and source code for the Testing Agent.
    """

    def __init__(self, project_path: str | Path) -> None:
        self.project_path = Path(project_path)

    def validate_project(self) -> None:
        """Validate that the project directory exists."""

        if not self.project_path.exists():
            raise FileNotFoundError(
                f"Project directory not found: {self.project_path}"
            )

        if not self.project_path.is_dir():
            raise ValueError(
                f"Project path is not a directory: {self.project_path}"
            )

    def get_structure(self) -> str:
        """
        Return a readable project file structure.
        """

        self.validate_project()

        files = sorted(
            path for path in self.project_path.rglob("*")
            if path.is_file()
        )

        if not files:
            return "(No files found.)"

        return "\n".join(
            str(path.relative_to(self.project_path))
            for path in files
        )

    def get_code(self) -> str:
        """
        Read generated text/code files.

        Binary files are skipped.
        """

        self.validate_project()

        supported_extensions = {
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".json",
            ".prisma",
            ".md",
            ".txt",
            ".env",
            ".sql",
            ".css",
            ".html",
        }

        sections: list[str] = []

        files = sorted(
            path for path in self.project_path.rglob("*")
            if path.is_file()
        )

        for path in files:
            if path.suffix.lower() not in supported_extensions:
                continue

            try:
                content = path.read_text(
                    encoding="utf-8"
                )
            except UnicodeDecodeError:
                continue

            relative_path = path.relative_to(
                self.project_path
            )

            sections.append(
                f"### File: {relative_path}\n"
                f"FILE_CONTENTS_START\n"
                f"{content}\n"
                f"FILE_CONTENTS_END"
            )

        if not sections:
            return "(No readable source files found.)"

        return "\n\n".join(sections)

    def inspect(self) -> Dict[str, str]:
        """
        Return both project structure and project code.
        """

        return {
            "project_structure": self.get_structure(),
            "project_code": self.get_code(),
        }


def create_project_inspector(
    project_path: str | Path,
) -> ProjectInspector:
    """
    Create a ProjectInspector instance.
    """

    return ProjectInspector(project_path)