from agents.developer_agent import create_developer_agent
from tasks.developer_tasks import create_developer_prompt


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
    JWT authentication
    RBAC authorization
    REST APIs
    """

    prompt = create_developer_prompt(
        confirmed_requirements=confirmed_requirements,
        architecture=architecture,
        project_idea="Hospital Management System",
    )

    required_checks = [
    "confirmed requirements are the absolute source of truth",
    "preserve every confirmed user role",
    "preserve every confirmed core feature",
    "preserve every confirmed permission",
    "preserve every confirmed workflow",
    "preserve every explicitly excluded feature or module",
    "never invent new business functionality",
    "never invent new user roles",
    "never invent new permissions",
    "never invent new workflows",
    "technical decisions",
    "requirement-to-code mapping",
    "explicit exclusions",
    ]

    prompt_lower = prompt.lower()

    for check in required_checks:
        assert check.lower() in prompt_lower, (
            f"Missing Developer safeguard: {check}"
        )

    agent = create_developer_agent()

    assert agent.role == "Software Developer"
    assert agent.goal
    assert agent.backstory

    print("✅ DEVELOPER AGENT CREATED")
    print("✅ DEVELOPER PROMPT VALIDATION PASSED")


if __name__ == "__main__":
    main()