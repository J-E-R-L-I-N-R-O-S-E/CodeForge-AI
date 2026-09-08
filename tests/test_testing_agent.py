from pathlib import Path

from agents.testing_agent import create_testing_agent
from services.project_inspector import create_project_inspector
from tasks.testing_tasks import create_testing_prompt


PROJECT_PATH = Path(
    "outputs/hospital-management-generated"
)


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
# Hospital Management System - Approved Technical Architecture

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
    print("CODEFORGE AI - TESTING AGENT LIVE TEST")
    print("=" * 70)

    if not PROJECT_PATH.exists():
        raise FileNotFoundError(
            f"Generated project not found: {PROJECT_PATH}"
        )

    print("\nCreating Testing Agent...")

    agent = create_testing_agent()

    print("✅ Testing Agent created")

    print("\nInspecting generated project...")

    inspector = create_project_inspector(
        PROJECT_PATH
    )

    inspection = inspector.inspect()

    print("✅ Project inspected")

    print("\nBuilding Testing Agent prompt...")

    prompt = create_testing_prompt(
        project_idea=PROJECT_IDEA,
        confirmed_requirements=CONFIRMED_REQUIREMENTS,
        architecture=ARCHITECTURE,
        project_structure=inspection["project_structure"],
        project_code=inspection["project_code"],
    )

    print("✅ Testing prompt created")

    print("\nRunning Testing Agent...")
    print("⚠️ This makes ONE real LLM request.\n")

    report = agent.generate(prompt)

    if not report.strip():
        raise RuntimeError(
            "Testing Agent returned an empty report."
        )

    print("\n" + "=" * 70)
    print("TESTING AGENT REPORT")
    print("=" * 70)

    print(report)

    print("\n" + "=" * 70)
    print("BASIC REPORT CHECKS")
    print("=" * 70)

    report_lower = report.lower()

    checks = {
        "Test Summary": "test summary" in report_lower,
        "Requirement Validation": (
            "requirement validation" in report_lower
        ),
        "Architecture Validation": (
            "architecture validation" in report_lower
        ),
        "Defects Found": (
            "defects found" in report_lower
        ),
        "Explicit Exclusions": (
            "explicit exclusions" in report_lower
        ),
        "Test Coverage": (
            "test coverage" in report_lower
        ),
        "Recommended Fixes": (
            "recommended fixes" in report_lower
        ),
        "Final Testing Decision": (
            "final testing decision" in report_lower
        ),
    }

    for name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {name}")

    if all(checks.values()):
        print("\n✅ TESTING AGENT LIVE TEST PASSED")
    else:
        print("\n⚠️ TESTING AGENT NEEDS REVIEW")


if __name__ == "__main__":
    main()