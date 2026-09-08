from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List


class CodeGenerator:
    """
    CodeForge AI Generation Tool.

    Converts Developer Agent output into actual project files.

    Expected Developer Agent format:

    ### File: backend/src/app.js
    FILE_CONTENTS_START
    <file content>
    FILE_CONTENTS_END
    """

    FILE_PATTERN = re.compile(
        r"###\s*File:\s*(.+?)\s*\n"
        r"FILE_CONTENTS_START\s*\n"
        r"(.*?)"
        r"\nFILE_CONTENTS_END",
        re.DOTALL | re.IGNORECASE,
    )

    def __init__(self, output_root: str = "outputs") -> None:
        self.output_root = Path(output_root)

    @staticmethod
    def _safe_relative_path(file_path: str) -> Path:
        """
        Validate and normalize a generated relative file path.
        """

        cleaned = file_path.strip().strip("`").strip()

        if not cleaned:
            raise ValueError("Generated file path is empty.")

        # Convert Windows separators to a portable form.
        cleaned = cleaned.replace("\\", "/")

        path = Path(cleaned)

        if path.is_absolute():
            raise ValueError(
                f"Absolute paths are not allowed: {file_path}"
            )

        # Reject path traversal.
        if ".." in path.parts:
            raise ValueError(
                f"Path traversal is not allowed: {file_path}"
            )

        return path

    def parse_files(self, developer_output: str) -> Dict[str, str]:
        """
        Parse generated files from Developer Agent output.

        Returns:
            Dictionary mapping relative file paths to file contents.
        """

        if not developer_output or not developer_output.strip():
            raise ValueError(
                "Developer Agent output cannot be empty."
            )

        matches = self.FILE_PATTERN.findall(developer_output)

        if not matches:
            raise ValueError(
                "No generated files were found in the Developer Agent output."
            )

        files: Dict[str, str] = {}

        for raw_path, content in matches:
            safe_path = self._safe_relative_path(raw_path)
            normalized_path = safe_path.as_posix()

            if normalized_path in files:
                raise ValueError(
                    f"Duplicate generated file detected: {normalized_path}"
                )

            files[normalized_path] = content.rstrip()

        return files

    def write_project(
        self,
        project_name: str,
        developer_output: str,
    ) -> List[Path]:
        """
        Parse Developer Agent output and write the generated
        project to disk.

        Returns:
            List of generated file paths.
        """

        if not project_name or not project_name.strip():
            raise ValueError(
                "Project name cannot be empty."
            )

        project_name = project_name.strip()

        # Prevent project-level path traversal.
        project_path = Path(project_name)

        if (
            project_path.is_absolute()
            or ".." in project_path.parts
            or len(project_path.parts) != 1
        ):
            raise ValueError(
                "Project name must be a simple directory name."
            )

        files = self.parse_files(developer_output)

        project_root = self.output_root / project_name
        project_root.mkdir(parents=True, exist_ok=True)

        generated_paths: List[Path] = []

        for relative_path, content in files.items():
            target = project_root / Path(relative_path)

            # Final safety check.
            resolved_root = project_root.resolve()
            resolved_target = target.resolve()

            if resolved_root not in resolved_target.parents:
                raise ValueError(
                    f"Unsafe generated path: {relative_path}"
                )

            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            target.write_text(
                content,
                encoding="utf-8",
            )

            generated_paths.append(target)

        return generated_paths

    def generate_project(
        self,
        project_name: str,
        developer_output: str,
    ) -> Dict[str, object]:
        """
        Complete generation operation.

        Returns a summary containing:
        - project directory
        - number of generated files
        - generated file paths
        """

        generated_paths = self.write_project(
            project_name=project_name,
            developer_output=developer_output,
        )

        project_root = (
            self.output_root / project_name
        ).resolve()

        return {
            "project_name": project_name,
            "project_path": str(project_root),
            "file_count": len(generated_paths),
            "files": [
                str(path.resolve().relative_to(project_root))
                for path in generated_paths
            ],
        }


def create_code_generator(
    output_root: str = "outputs",
) -> CodeGenerator:
    """
    Create the CodeForge AI Code Generator.
    """

    return CodeGenerator(output_root=output_root)