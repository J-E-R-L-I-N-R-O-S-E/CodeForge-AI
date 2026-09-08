from agents.testing_agent import create_testing_agent
from tasks.testing_tasks import create_testing_prompt


def main():
    confirmed_requirements = """
    - Web application
    - Roles: Admin, Doctor, Patient
    - Patient management
    - Doctor management
    - Appointment management
    - Medical records
    - Patients can book appointments
    - Patients can cancel their own appointments
    - Admins can create and modify appointments
    - Doctors can view their own appointments
    - Doctors can create and update medical records
    - Patients can view their own medical records
    - Admins can manage patient records
    - All users must authenticate
    - Billing is excluded
    - Pharmacy is excluded
    - Laboratory is excluded
    """

    architecture = """
    React frontend
    Node.js + Express backend
    PostgreSQL database
    Prisma ORM
    REST API
    JWT authentication
    Role-Based Access Control
    """

    project_structure = """
    hospital-management/
    ├── backend/
    ├── frontend/
    ├── prisma/
    └── README.md
    """

    project_code = """
    Sample generated project code.
    """

    prompt = create_testing_prompt(
        project_idea="Hospital Management System",
        confirmed_requirements=confirmed_requirements,
        architecture=architecture,
        project_structure=project_structure,
        project_code=project_code,
    )

    prompt_lower = prompt.lower()

    required_checks = [
        "confirmed requirements are the source of truth",
        "approved architecture is the source of truth",
        "verify every confirmed role",
        "verify every confirmed feature",
        "verify every confirmed permission",
        "verify every confirmed workflow",
        "verify every explicitly excluded feature",
        "do not invent new business requirements",
        "requirement coverage",
        "architecture check",
        "api consistency check",
        "database consistency check",
        "authentication check",
        "authorization check",
        "test coverage check",
        "defects found",
        "recommended fixes",
        "pass with warnings",
    ]

    for check in required_checks:
        assert check.lower() in prompt_lower, (
            f"Missing Testing safeguard: {check}"
        )

    agent = create_testing_agent()

    assert agent.role == "Software Testing Engineer"
    assert agent.goal
    assert agent.backstory

    print("✅ TESTING AGENT CREATED")
    print("✅ TESTING PROMPT VALIDATION PASSED")


if __name__ == "__main__":
    main()