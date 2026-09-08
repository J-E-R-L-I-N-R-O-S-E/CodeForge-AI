from tasks.fix_tasks import create_format_repair_prompt


def main():
    previous_output = """
### File: frontend/src/pages/Dashboard.js
import React from "react";
FILE_CONTENTS_START
export default function Dashboard() {
    return <div>Dashboard</div>;
}
FILE_CONTENTS_END
"""

    prompt = create_format_repair_prompt(
        previous_output=previous_output
    )

    checks = {
        "format_instruction": (
            "invalid file format" in prompt.lower()
        ),
        "same_line_rule": (
            "`### File: <relative path>` must be one complete line."
            in prompt
        ),
        "start_marker": (
            "FILE_CONTENTS_START" in prompt
        ),
        "end_marker": (
            "FILE_CONTENTS_END" in prompt
        ),
        "no_fences": (
            "Do not use markdown code fences." in prompt
        ),
        "no_explanations": (
            "Do not add explanations." in prompt
        ),
        "implementation_preserved": (
            "Preserve the implementation exactly." in prompt
        ),
        "only_file_blocks": (
            "RETURN ONLY THE CORRECTED FILE BLOCKS." in prompt
        ),
    }

    for name, passed in checks.items():
        print(f"{'✅' if passed else '❌'} {name}")

    assert all(checks.values())

    print("\n✅ Format Repair Prompt Test PASSED")


if __name__ == "__main__":
    main()