from __future__ import annotations

import re
from pathlib import Path

from agents.developer_agent import create_developer_agent
from services.testing_service import create_testing_service
from tasks.fix_tasks import (
    create_fix_prompt,
    create_format_repair_prompt,
)
from tools.code_generator import create_code_generator


class TestFixService:
    """
    Coordinates the Testing Agent and Developer Agent for a
    bounded test -> fix -> re-test workflow.
    """

    MAX_RETRIES = 1

    def __init__(
        self,
        testing_service=None,
        developer_agent=None,
        code_generator=None,
    ):
        self.testing_service = (
            testing_service or create_testing_service()
        )
        self.developer_agent = (
            developer_agent or create_developer_agent()
        )
        self.code_generator = (
            code_generator or create_code_generator()
        )

    # =============================================================
    # Developer output normalization
    # =============================================================

    @staticmethod
    def _normalize_developer_output(
        developer_output: str,
    ) -> str:
        """
        Convert common Developer Agent formatting variations into
        the exact canonical CodeForge format expected by the
        CodeGenerator.

        The parser is line-based instead of relying on a large
        regex, making it more tolerant of LLM formatting mistakes.
        """

        if not developer_output or not developer_output.strip():
            return developer_output

        lines = developer_output.splitlines()

        file_blocks = []
        current_path = None
        current_content = []
        inside_content = False

        header_pattern = re.compile(
            r"^\s*###\s*File:\s*(.*?)\s*$",
            re.IGNORECASE,
        )

        for line in lines:
            header_match = header_pattern.match(line)

            # -----------------------------------------------------
            # New file header
            # -----------------------------------------------------
            if header_match:
                # Save previous file.
                if current_path is not None:
                    file_blocks.append(
                        (
                            current_path,
                            current_content,
                        )
                    )

                current_path = header_match.group(1).strip()
                current_content = []
                inside_content = False
                continue

            # Ignore content before the first file header.
            if current_path is None:
                continue

            # -----------------------------------------------------
            # File content markers
            # -----------------------------------------------------
            if line.strip().upper() == "FILE_CONTENTS_START":
                inside_content = True
                continue

            if line.strip().upper() == "FILE_CONTENTS_END":
                inside_content = False
                continue

            # -----------------------------------------------------
            # Collect source code.
            #
            # We intentionally collect lines both before and after
            # FILE_CONTENTS_START because some LLMs place source
            # before the marker.
            # -----------------------------------------------------
            current_content.append(line)

        # Save final file.
        if current_path is not None:
            file_blocks.append(
                (
                    current_path,
                    current_content,
                )
            )

        canonical_blocks = []

        for file_path, content_lines in file_blocks:

            file_path = file_path.strip()

            if not file_path:
                continue

            # Remove accidental markdown fences.
            cleaned_lines = []

            for line in content_lines:
                stripped = line.strip()

                if stripped in {
                    "```",
                    "```javascript",
                    "```js",
                    "```jsx",
                    "```typescript",
                    "```tsx",
                    "```python",
                    "```json",
                    "```html",
                    "```css",
                    "```sql",
                }:
                    continue

                cleaned_lines.append(line)

            content = "\n".join(
                cleaned_lines
            ).strip()

            canonical_blocks.append(
                "\n".join(
                    [
                        f"### File: {file_path}",
                        "FILE_CONTENTS_START",
                        content,
                        "FILE_CONTENTS_END",
                    ]
                )
            )

        return "\n\n".join(canonical_blocks)

    # =============================================================
    # Developer output validation
    # =============================================================

    @staticmethod
    def _validate_developer_output(
        developer_output: str,
    ) -> None:
        """
        Validate canonical Developer Agent output.

        Validation is intentionally line-based and strict about
        file headers, while allowing normal source-code content.
        """

        if not developer_output or not developer_output.strip():
            raise ValueError(
                "Developer Agent returned empty output."
            )

        lines = developer_output.splitlines()

        header_pattern = re.compile(
            r"^###\s*File:\s*(.+?)$",
            re.IGNORECASE,
        )

        file_count = 0
        index = 0

        while index < len(lines):

            line = lines[index].strip()

            if not line:
                index += 1
                continue

            header_match = header_pattern.match(line)

            if not header_match:
                raise ValueError(
                    "Developer Agent returned invalid file format. "
                    "Every file must begin with '### File: <path>'."
                )

            file_path = header_match.group(1).strip()

            if not file_path:
                raise ValueError(
                    "Developer Agent produced an empty file path."
                )

            if "\n" in file_path or "\r" in file_path:
                raise ValueError(
                    "Developer Agent produced a malformed file path."
                )

            index += 1

            if (
                index >= len(lines)
                or lines[index].strip().upper()
                != "FILE_CONTENTS_START"
            ):
                raise ValueError(
                    f"Missing FILE_CONTENTS_START for: {file_path}"
                )

            index += 1

            found_end = False

            while index < len(lines):
                if (
                    lines[index].strip().upper()
                    == "FILE_CONTENTS_END"
                ):
                    found_end = True
                    index += 1
                    break

                index += 1

            if not found_end:
                raise ValueError(
                    f"Missing FILE_CONTENTS_END for: {file_path}"
                )

            file_count += 1

        if file_count == 0:
            raise ValueError(
                "Developer Agent returned no file blocks."
            )

    # =============================================================
    # Status extraction
    # =============================================================

    @staticmethod
    def _extract_status(report: str) -> str:
        """
        Extract the final testing decision.
        """

        if not report:
            return "UNKNOWN"

        normalized = report.upper()

        marker = "FINAL TESTING DECISION"

        if marker in normalized:
            decision_section = normalized.split(
                marker,
                1,
            )[1]

            lines = [
                line.strip()
                for line in decision_section.splitlines()
                if line.strip()
            ]

            for line in lines[:5]:

                if line == "PASS WITH WARNINGS":
                    return "PASS WITH WARNINGS"

                if line == "PASS":
                    return "PASS"

                if line == "FAIL":
                    return "FAIL"

        if "OVERALL STATUS: FAIL" in normalized:
            return "FAIL"

        if "OVERALL STATUS: PASS WITH WARNINGS" in normalized:
            return "PASS WITH WARNINGS"

        if "OVERALL STATUS: PASS" in normalized:
            return "PASS"

        return "UNKNOWN"

    @classmethod
    def _report_is_pass(
        cls,
        report: str,
    ) -> bool:
        """
        Stop the loop on PASS or PASS WITH WARNINGS.
        """

        status = cls._extract_status(report)

        return status in {
            "PASS",
            "PASS WITH WARNINGS",
        }

    # =============================================================
    # Main test -> fix -> re-test loop
    # =============================================================

    def run(
        self,
        project_path: str | Path,
        confirmed_requirements: str,
        architecture: str,
        project_idea: str = "",
        max_retries: int = MAX_RETRIES,
    ) -> dict:
        """
        Run the bounded test -> fix -> re-test workflow.
        """

        if max_retries < 0:
            raise ValueError(
                "max_retries cannot be negative."
            )

        max_retries = min(
            max_retries,
            self.MAX_RETRIES,
        )

        project_path = Path(project_path)

        if not project_path.exists():
            raise FileNotFoundError(
                f"Project path does not exist: {project_path}"
            )

        if not project_path.is_dir():
            raise ValueError(
                f"Project path is not a directory: {project_path}"
            )

        reports = []
        fixes_applied = []

        # ---------------------------------------------------------
        # Initial test
        # ---------------------------------------------------------
        report = self.testing_service.analyze_project(
            project_path=project_path,
            confirmed_requirements=confirmed_requirements,
            architecture=architecture,
            project_idea=project_idea,
        )

        reports.append(
            {
                "attempt": 0,
                "type": "test",
                "report": report,
            }
        )

        # ---------------------------------------------------------
        # Fix -> Re-test loop
        # ---------------------------------------------------------
        for attempt in range(
            1,
            max_retries + 1,
        ):

            if self._report_is_pass(report):
                break

            inspection = self.testing_service.inspect_project(
                project_path
            )

            fix_prompt = create_fix_prompt(
                project_idea=project_idea,
                confirmed_requirements=confirmed_requirements,
                architecture=architecture,
                testing_report=report,
                project_structure=inspection[
                    "project_structure"
                ],
                project_code=inspection["project_code"][:8000],
            )

            developer_output = self.developer_agent.generate(
                prompt=fix_prompt,
                preferred_provider="groq",
            )

            # -----------------------------------------------------
            # Normalize first.
            # -----------------------------------------------------
            developer_output = (
                self._normalize_developer_output(
                    developer_output
                )
            )

            # -----------------------------------------------------
            # Validate.
            # -----------------------------------------------------
            try:
                self._validate_developer_output(
                    developer_output
                )

            except ValueError:

                # -------------------------------------------------
                # One controlled format-repair attempt.
                # -------------------------------------------------
                repair_prompt = (
                    create_format_repair_prompt(
                        previous_output=developer_output
                    )
                )

                developer_output = self.developer_agent.generate(
                    prompt=repair_prompt,
                    preferred_provider="groq",
                )

                developer_output = (
                    self._normalize_developer_output(
                        developer_output
                    )
                )

                self._validate_developer_output(
                    developer_output
                )

            # -----------------------------------------------------
            # Apply the generated files.
            # -----------------------------------------------------
            written_files = (
                self.code_generator.write_project(
                    project_path.name,
                    developer_output,
                )
            )

            fixes_applied.append(
                {
                    "attempt": attempt,
                    "files": written_files,
                }
            )

            reports.append(
                {
                    "attempt": attempt,
                    "type": "fix",
                    "files": written_files,
                }
            )

            # -----------------------------------------------------
            # Re-test.
            # -----------------------------------------------------
            report = self.testing_service.analyze_project(
                project_path=project_path,
                confirmed_requirements=confirmed_requirements,
                architecture=architecture,
                project_idea=project_idea,
            )

            reports.append(
                {
                    "attempt": attempt,
                    "type": "retest",
                    "report": report,
                }
            )

        return {
            "attempts": len(
                [
                    item
                    for item in reports
                    if item["type"] == "retest"
                ]
            ),
            "reports": reports,
            "final_report": report,
            "final_status": self._extract_status(
                report
            ),
            "fixes_applied": fixes_applied,
        }


def create_test_fix_service() -> TestFixService:
    """Create a TestFixService instance."""
    return TestFixService()