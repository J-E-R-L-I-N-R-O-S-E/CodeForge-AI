from pathlib import Path

from services.test_fix_service import create_test_fix_service


PROJECT_PATH = Path("outputs/hospital-management-generated")


def main():
    if not PROJECT_PATH.exists():
        raise FileNotFoundError(
            f"Generated HMS project not found: {PROJECT_PATH}"
        )

    confirmed_requirements = """
Hospital Management System for a web application.

Confirmed users:
- Admin
- Doctor
- Patient

Core functionality:
- User authentication
- Role-based access
- Appointment management

Explicit exclusions:
- Billing
- Pharmacy
- Laboratory management
"""

    architecture = """
Frontend:
- React

Backend:
- Node.js
- Express

Database:
- PostgreSQL

ORM:
- Prisma

API:
- REST

Authentication:
- JWT

Authorization:
- Role-based access control
"""

    project_idea = "Hospital Management System"

    service = create_test_fix_service()

    print("=" * 70)
    print("CODEFORGE AI — LIVE TEST ↔ FIX LOOP")
    print("=" * 70)
    print(f"Project: {PROJECT_PATH}")
    print("Maximum fix attempts: 1")
    print()

    result = service.run(
        project_path=PROJECT_PATH,
        confirmed_requirements=confirmed_requirements,
        architecture=architecture,
        project_idea=project_idea,
        max_retries=1,
    )

    print()
    print("=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(f"Final Status : {result['final_status']}")
    print(f"Fix Attempts : {result['attempts']}")
    print(
        f"Fixes Applied: {len(result['fixes_applied'])}"
    )

    print()
    print("=" * 70)
    print("FIX HISTORY")
    print("=" * 70)

    for fix in result["fixes_applied"]:
        print(
            f"Attempt {fix['attempt']}: "
            f"{fix['files']}"
        )

    print()
    print("=" * 70)
    print("FINAL TESTING REPORT")
    print("=" * 70)

    print(result["final_report"])

    print()
    print("=" * 70)

    if result["final_status"] in {
        "PASS",
        "PASS WITH WARNINGS",
    }:
        print("✅ PHASE 12 LIVE LOOP EXECUTED")
    else:
        print("⚠️ PHASE 12.3 LIVE LOOP COMPLETED WITH REMAINING DEFECTS")

    print("=" * 70)


if __name__ == "__main__":
    main()