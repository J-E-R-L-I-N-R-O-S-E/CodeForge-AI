from pathlib import Path

from services.project_inspector import create_project_inspector


def main():
    print("=" * 70)
    print("CODEFORGE AI - PROJECT INSPECTOR TEST")
    print("=" * 70)

    project_path = Path(
        "outputs/hospital-management-generated"
    )

    if not project_path.exists():
        raise FileNotFoundError(
            f"Generated project not found: {project_path}"
        )

    inspector = create_project_inspector(
        project_path
    )

    print("\nReading project structure...")

    structure = inspector.get_structure()

    assert structure.strip()
    print("✅ Project structure inspection passed")

    print("\nReading project source code...")

    code = inspector.get_code()

    assert code.strip()
    print("✅ Project source inspection passed")

    print("\nChecking important generated files...")

    structure_lower = structure.lower()
    code_lower = code.lower()

    required_items = [
        "backend",
        "frontend",
        "prisma",
        "schema.prisma",
        "package.json",
        "readme.md",
    ]

    for item in required_items:
        assert item.lower() in structure_lower, (
            f"Missing expected project item: {item}"
        )

    print("✅ Expected project files detected")

    print("\nChecking code content...")

    important_terms = [
        "prisma",
        "patient",
        "doctor",
        "appointment",
        "medical",
        "jwt",
    ]

    for term in important_terms:
        assert term in code_lower, (
            f"Missing expected code term: {term}"
        )

    print("✅ Expected code content detected")

    print("\nChecking combined inspection result...")

    result = inspector.inspect()

    assert "project_structure" in result
    assert "project_code" in result
    assert result["project_structure"].strip()
    assert result["project_code"].strip()

    print("✅ Combined inspection passed")

    print("\n" + "=" * 70)
    print("✅ PROJECT INSPECTOR TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()