from __future__ import annotations


def create_fix_prompt(
    project_idea: str,
    confirmed_requirements: str,
    architecture: str,
    testing_report: str,
    project_structure: str,
    project_code: str,
) -> str:
    """
    Create a strict prompt for the Developer Agent to fix
    defects identified by the Testing Agent.
    """

    return f"""
You are the CodeForge AI Developer Agent.

TASK:
Fix the EXISTING project using ONLY defects explicitly
identified by the Testing Agent.

Do not redesign the project.
Do not add business functionality.
Do not invent requirements.

==================================================
PROJECT IDEA
==================================================

{project_idea}

==================================================
CONFIRMED REQUIREMENTS
==================================================

{confirmed_requirements}

==================================================
APPROVED ARCHITECTURE
==================================================

{architecture}

==================================================
TESTING REPORT
==================================================

{testing_report}

==================================================
CURRENT PROJECT STRUCTURE
==================================================

{project_structure}

==================================================
CURRENT PROJECT CODE
==================================================

{project_code}

==================================================
FIX RULES
==================================================

1. Fix reported CRITICAL, HIGH and MEDIUM defects.

2. Do not invent new business functionality.

3. Do not invent roles.

4. Do not invent permissions.

5. Do not invent workflows.

6. Do not remove confirmed functionality.

7. Preserve explicit exclusions.

8. Preserve the approved architecture.

9. Preserve the selected:
   - framework
   - database
   - ORM
   - authentication
   - API approach
   - project structure

10. Change only files that actually need fixing.

11. Do not create duplicate or alternative files.

12. Keep the project at 15 files or fewer.

13. Keep imports, APIs, frontend, backend and database
    consistent.

14. Every returned file must contain COMPLETE contents.

==================================================
MANDATORY OUTPUT FORMAT
==================================================

Your response MUST contain ONLY file blocks.

For every changed file:

### File: <relative path>
FILE_CONTENTS_START
<complete file contents>
FILE_CONTENTS_END

IMPORTANT:

- Put the file path ONLY on the ### File line.
- Put FILE_CONTENTS_START on the next line.
- Put the COMPLETE source code after FILE_CONTENTS_START.
- Put FILE_CONTENTS_END after the COMPLETE source code.
- Never put source code on the ### File line.
- Never use markdown code fences.
- Never add explanations.
- Never add text before the first ### File.
- Never add text after the final FILE_CONTENTS_END.
- Return ONLY files that were changed.

==================================================
FINAL CHECK
==================================================

Before responding, verify:

- Every reported fix is addressed.
- Requirements are preserved.
- Architecture is preserved.
- Explicit exclusions are preserved.
- No business functionality was invented.
- Every file has complete contents.
- File markers are exactly correct.

RETURN ONLY THE FILE BLOCKS.
"""


def create_format_repair_prompt(
    previous_output: str,
) -> str:
    """
    Ask the Developer Agent to return the same implementation
    using the required machine-readable file format.
    """

    return f"""
The previous Developer Agent response had an invalid file format.

DO NOT change the implementation.
DO NOT redesign anything.
DO NOT add functionality.

Convert the previous response into the exact format below.

PREVIOUS RESPONSE:
{previous_output}

MANDATORY FORMAT:

### File: <relative path>
FILE_CONTENTS_START
<complete file contents>
FILE_CONTENTS_END

RULES:

1. `### File: <relative path>` must be one complete line.
2. FILE_CONTENTS_START must be on the immediately next line.
3. Complete source code follows.
4. FILE_CONTENTS_END must be after the complete source.
5. Do not place source code on the file-header line.
6. Do not use markdown code fences.
7. Do not add explanations.
8. Return ONLY file blocks.
9. Preserve the implementation exactly.
10. Do not create new files.

RETURN ONLY THE CORRECTED FILE BLOCKS.
"""