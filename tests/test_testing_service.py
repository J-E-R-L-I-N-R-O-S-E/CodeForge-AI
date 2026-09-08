from pathlib import Path

from services.testing_service import create_testing_service


def main():
    print("=" * 70)
    print("CODEFORGE AI - TESTING SERVICE TEST")
    print("=" * 70)

    project_path = Path(
        "outputs/hospital-management-generated"
    )

    if not project_path.exists():
        raise FileNotFoundError(
            f"Generated project not found: {project_path}"
        )

    service = create_testing_service()

    print("\nInspecting generated project...")

    inspection = service.inspect_project(
        str(project_path)
    )

    assert "project_structure" in inspection
    assert "project_code" in inspection

    assert inspection["project_structure"].strip()
    assert inspection["project_code"].strip()

    print("✅ TestingService inspection wiring passed")

    print("\nChecking project structure...")

    structure = inspection["project_structure"].lower()

    required_structure_items = [
        "backend",
        "frontend",
        "prisma",
        "schema.prisma",
    ]

    for item in required_structure_items:
        assert item in structure, (
            f"Missing expected structure item: {item}"
        )

    print("✅ Project structure passed")

    print("\nChecking project code...")

    code = inspection["project_code"].lower()

    required_code_items = [
        "prisma",
        "patient",
        "doctor",
        "appointment",
        "medical",
        "jwt",
    ]

    for item in required_code_items:
        assert item in code, (
            f"Missing expected code item: {item}"
        )

    print("✅ Project code passed")

    print("\nChecking Testing Agent connection...")

    assert service.testing_agent is not None
    assert service.testing_agent.role == (
        "Software Testing Engineer"
    )

    print("✅ Testing Agent connection passed")

    print("\n" + "=" * 70)
    print("✅ TESTING SERVICE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()