from tasks.fix_tasks import create_fix_prompt


def main():
    prompt = create_fix_prompt(
        project_idea="Hospital Management System",
        confirmed_requirements="Admin can manage appointments.",
        architecture="React frontend, Node.js backend, PostgreSQL, Prisma.",
        testing_report="D1 HIGH: Admin appointment management UI is missing.",
        project_structure="frontend/src/pages/Appointments.js",
        project_code="console.log('test');",
    )

    checks = {
        "fix_only": "Fix ONLY defects identified" in prompt,
        "requirements": "confirmed requirements" in prompt.lower(),
        "architecture": "approved architecture" in prompt.lower(),
        "no_invention": "Do not invent new business functionality." in prompt,
        "critical": "CRITICAL defects" in prompt,
        "high": "HIGH defects" in prompt,
        "medium": "MEDIUM defects" in prompt,
        "markers": "FILE_CONTENTS_START" in prompt
        and "FILE_CONTENTS_END" in prompt,
        "modified_only": "Only return files that actually need to be changed."
        in prompt,
        "max_files": "Maximum total project files: 15." in prompt,
    }

    for name, passed in checks.items():
        print(f"{'✅' if passed else '❌'} {name}")

    assert all(checks.values())

    print("\n✅ Phase 12.1 Fix Prompt Test PASSED")


if __name__ == "__main__":
    main()