from agents.developer_agent import create_developer_agent
from tasks.developer_tasks import create_developer_prompt


PROJECT_IDEA = """
Build a Hospital Management System for managing patients, doctors,
appointments, and medical records.
"""


CONFIRMED_REQUIREMENTS = """
- The system shall be implemented as a web application.
- The system supports three user roles: Admin, Doctor, and Patient.
- The system provides modules for patient management, doctor management,
  appointment management, and medical records.
- Patients can book appointments and cancel their own appointments.
- Admins can create and modify appointments.
- Doctors can view their own appointments.
- Doctors can create and update medical records.
- Patients can view their own medical records.
- Admins can manage patient records.
- All users must authenticate before accessing the system.
- Billing, pharmacy, and laboratory are explicitly excluded.
"""


ARCHITECTURE = """
# Hospital Management System - Technical Architecture

## Architecture
- Web application
- React frontend
- Node.js + Express backend
- PostgreSQL database
- Prisma ORM
- REST API
- JWT authentication
- Role-Based Access Control

## Roles
- Admin
- Doctor
- Patient

## Modules
- Patient Management
- Doctor Management
- Appointment Management
- Medical Records

## Confirmed Workflows
- Patient can book appointments.
- Patient can cancel their own appointments.
- Admin can create and modify appointments.
- Doctor can view their own appointments.
- Doctor can create and update medical records.
- Patient can view their own medical records.
- Admin can manage patient records.

## Exclusions
- Billing
- Pharmacy
- Laboratory
"""


def main():
    print("=" * 70)
    print("CODEFORGE AI - DEVELOPER AGENT TEST")
    print("=" * 70)

    print("\nChecking Developer Agent creation...")

    agent = create_developer_agent()

    assert agent.role == "Software Developer"
    assert agent.goal
    assert agent.backstory

    print("✅ Developer Agent created")

    print("\nChecking Developer prompt...")

    prompt = create_developer_prompt(
        project_idea=PROJECT_IDEA,
        confirmed_requirements=CONFIRMED_REQUIREMENTS,
        architecture=ARCHITECTURE,
    )

    prompt_lower = prompt.lower()

    prompt_checks = {
        "Confirmed requirements are authoritative": (
            "confirmed requirements are the absolute source of truth"
            in prompt_lower
        ),
        "Architecture is technically authoritative": (
            "approved architecture is authoritative for technical"
            in prompt_lower
        ),
        "Preserve confirmed roles": (
            "preserve every confirmed user role"
            in prompt_lower
        ),
        "Preserve confirmed features": (
            "preserve every confirmed core feature"
            in prompt_lower
        ),
        "Preserve confirmed permissions": (
            "preserve every confirmed permission"
            in prompt_lower
        ),
        "Preserve confirmed workflows": (
            "preserve every confirmed workflow"
            in prompt_lower
        ),
        "Preserve explicit exclusions": (
            "preserve every explicitly excluded feature or module"
            in prompt_lower
        ),
        "Do not invent business functionality": (
            "never invent new business functionality"
            in prompt_lower
        ),
        "Do not silently change architecture": (
            "do not change the selected database, orm, framework"
            in prompt_lower
        ),
        "Internal consistency validation": (
            "all generated files must be internally consistent"
            in prompt_lower
        ),
        "Frontend/backend consistency check": (
            "api endpoints match frontend requests"
            in prompt_lower
        ),
        "Database/model consistency check": (
            "database fields match the models used by the code"
            in prompt_lower
        ),
        "Requirement-to-Code Mapping": (
            "requirement-to-code mapping"
            in prompt_lower
        ),
        "Explicit Exclusions section": (
            "explicit exclusions"
            in prompt_lower
        ),
        "Final validation": (
            "no unexplained architecture deviation exists"
            in prompt_lower
        ),
    }

    for name, passed in prompt_checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {name}")

    assert all(prompt_checks.values()), (
        "Developer prompt validation failed."
    )

    print("\n✅ DEVELOPER PROMPT VALIDATION PASSED")

    print("\n" + "=" * 70)
    print("GENERATING STARTER IMPLEMENTATION")
    print("=" * 70)

    result = agent.generate(prompt)

    print("\n" + "=" * 70)
    print("DEVELOPER RESULT")
    print("=" * 70)

    print(result)

    print("\n" + "=" * 70)
    print("BASIC OUTPUT CHECKS")
    print("=" * 70)

    result_lower = result.lower()

    checks = {
        "Admin role": "admin" in result_lower,

        "Doctor role": "doctor" in result_lower,

        "Patient role": "patient" in result_lower,

        "Patient management": "patient" in result_lower,

        "Doctor management": "doctor" in result_lower,

        "Appointment implementation": (
            "appointment" in result_lower
        ),

        "Medical records implementation": (
            "medical" in result_lower
            and "record" in result_lower
        ),

        "Authentication": (
            "auth" in result_lower
            or "jwt" in result_lower
        ),

        "Requirement-to-Code Mapping": (
            "requirement-to-code" in result_lower
        ),

        "Explicit Exclusions": (
            "billing" in result_lower
            and "pharmacy" in result_lower
            and "laboratory" in result_lower
        ),

        "Prisma architecture preserved": (
            "prisma" in result_lower
        ),

        "No obvious Sequelize substitution": (
            "sequelize" not in result_lower
        ),

        "Complete file content markers": (
            "file_contents_start" in result_lower
            and "file_contents_end" in result_lower
        ),
    }

    for name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {name}")

    if all(checks.values()):
        print("\n✅ DEVELOPER AGENT LIVE TEST PASSED")
    else:
        print("\n⚠️ DEVELOPER AGENT NEEDS REVIEW")


if __name__ == "__main__":
    main()