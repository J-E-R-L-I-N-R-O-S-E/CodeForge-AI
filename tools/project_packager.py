from __future__ import annotations

import shutil
from pathlib import Path


class ProjectPackager:
    """
    CodeForge AI project packaging tool.

    Creates a ZIP archive from a generated project directory.
    """

    def __init__(self, output_root: str = "outputs") -> None:
        self.output_root = Path(output_root)

    def create_zip(
        self,
        project_name: str,
        project_directory: str | Path | None = None,
    ) -> Path:
        """
        Create a ZIP archive for a generated project.

        Args:
            project_name:
                Name of the generated project.

            project_directory:
                Optional project directory.
                Defaults to outputs/<project_name>.

        Returns:
            Path to the generated ZIP file.
        """

        if not project_name or not project_name.strip():
            raise ValueError("Project name cannot be empty.")

        if project_directory is None:
            project_directory = self.output_root / project_name

        project_directory = Path(project_directory)

        if not project_directory.exists():
            raise FileNotFoundError(
                f"Project directory not found: {project_directory}"
            )

        if not project_directory.is_dir():
            raise ValueError(
                f"Project path is not a directory: {project_directory}"
            )

        zip_base = self.output_root / project_name

        archive_path = shutil.make_archive(
            base_name=str(zip_base),
            format="zip",
            root_dir=project_directory.parent,
            base_dir=project_directory.name,
        )

        return Path(archive_path)


def create_project_packager(
    output_root: str = "outputs",
) -> ProjectPackager:
    """
    Create the CodeForge AI project packager.
    """

    return ProjectPackager(output_root=output_root)