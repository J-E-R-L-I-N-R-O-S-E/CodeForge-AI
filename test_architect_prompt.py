from tasks.architect_tasks import create_architecture_prompt


def main():
    prompt = create_architecture_prompt(
        project_idea="Hospital Management System",
        confirmed_requirements="""
        - Web application
        - Roles: Admin, Doctor, Patient
        - Patient management
        - Doctor management
        - Appointment management
        - Medical records
        - Billing is excluded
        - Pharmacy is excluded
        - Laboratory is excluded
        """,
    )

    required_checks = [
    "preserve every confirmed requirement",
    "must not omit any confirmed user role",
    "must not omit any confirmed core feature",
    "must not omit any confirmed permission or workflow",
    "preserve every explicitly excluded feature/module",
    "never invent business functionality",
    "never invent user roles",
    "never invent permissions",
    "never invent workflows",
    "never invent business fields",
    "requirement traceability",
    ]

    prompt_lower = prompt.lower()

    for check in required_checks:
        assert check.lower() in prompt_lower, f"Missing safeguard: {check}"

    print("✅ ARCHITECT PROMPT VALIDATION PASSED")


if __name__ == "__main__":
    main()