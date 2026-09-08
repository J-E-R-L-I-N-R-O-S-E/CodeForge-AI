from __future__ import annotations

from pathlib import Path
from typing import Dict


class ProjectInspector:
    """
    Reads a generated CodeForge project and prepares
    its structure and source code for the Testing Agent.
    """

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".c",
        ".cpp",
        ".cs",
        ".go",
        ".html",
        ".css",
        ".json",
        ".md",
        ".txt",
        ".sql",
        ".prisma",
        ".yml",
        ".yaml",
        ".env",
    }

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
            path
            for path in self.project_path.rglob("*")
            if path.is_file()
        )

        if not files:
            return "(No files found.)"

        return "\n".join(
            str(path.relative_to(self.project_path))
            for path in files
        )

    def get_code(self, max_chars: int = 12000) -> str:
        """
        Collect project source code while enforcing a maximum
        total output-character budget, including file markers.
        """

        self.validate_project()

        if max_chars <= 0:
            raise ValueError(
                "max_chars must be greater than zero."
            )

        sections = []
        total_chars = 0

        files = sorted(
            path
            for path in self.project_path.rglob("*")
            if path.is_file()
        )

        for file_path in files:
            if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            try:
                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except OSError:
                continue

            relative_path = file_path.relative_to(
                self.project_path
            ).as_posix()

            prefix = (
                f"### File: {relative_path}\n"
                f"FILE_CONTENTS_START\n"
            )

            suffix = "\nFILE_CONTENTS_END"

            remaining = max_chars - total_chars

            # We need enough room for the complete file markers.
            marker_length = len(prefix) + len(suffix)

            if remaining <= marker_length:
                break

            available_content = remaining - marker_length

            truncated_content = content[:available_content]

            section = (
                prefix
                + truncated_content
                + suffix
            )

            sections.append(section)
            total_chars += len(section)

            if total_chars >= max_chars:
                break

        if not sections:
            return "(No supported source files found.)"[:max_chars]

        result = "\n\n".join(sections)

        # Final hard safety guarantee.
        return result[:max_chars]

    def inspect(self) -> Dict[str, str]:
        """
        Return both project structure and project code.
        """

        return {
            "project_structure": self.get_structure(),
            "project_code": self.get_code(max_chars=5000),
        }


def create_project_inspector(
    project_path: str | Path,
) -> ProjectInspector:
    """
    Create a ProjectInspector instance.
    """

    return ProjectInspector(project_path)