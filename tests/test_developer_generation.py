from pathlib import Path
import shutil
import zipfile

from agents.developer_agent import create_developer_agent
from services.generation_service import create_generation_service
from tasks.developer_tasks import create_developer_prompt


PROJECT_NAME = "hospital-management-generated"


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
    print("CODEFORGE AI - DEVELOPER → GENERATION INTEGRATION TEST")
    print("=" * 70)

    output_root = Path("outputs")
    project_directory = output_root / PROJECT_NAME
    zip_path = output_root / f"{PROJECT_NAME}.zip"

    # Remove previous integration-test output.
    if project_directory.exists():
        shutil.rmtree(project_directory)

    if zip_path.exists():
        zip_path.unlink()

    print("\nCreating Developer Agent...")

    developer_agent = create_developer_agent()

    print("✅ Developer Agent created")

    print("\nBuilding Developer prompt...")

    prompt = create_developer_prompt(
        project_idea=PROJECT_IDEA,
        confirmed_requirements=CONFIRMED_REQUIREMENTS,
        architecture=ARCHITECTURE,
    )

    print("✅ Developer prompt created")

    print("\nGenerating starter code with the real Developer Agent...")
    print("⚠️ This makes ONE real LLM request.\n")

    developer_output = developer_agent.generate(prompt)
    
    output_lower = developer_output.lower()

    if "file_contents_start" not in output_lower:
        raise RuntimeError(
            "Developer Agent output does not contain the required "
            "FILE_CONTENTS_START marker."
        )

    if "file_contents_end" not in output_lower:
        raise RuntimeError(
            "Developer Agent output does not contain the required "
            "FILE_CONTENTS_END marker."
        )

    start_count = output_lower.count("file_contents_start")
    end_count = output_lower.count("file_contents_end")

    if start_count != end_count:
        raise RuntimeError(
            "Developer Agent returned mismatched file-content markers: "
            f"{start_count} START markers vs {end_count} END markers."
        )

    print("✅ Developer output format validated")

    if not developer_output.strip():
        raise RuntimeError(
            "Developer Agent returned empty output."
        )

    print("✅ Developer Agent returned output")

    print("\nSending Developer output to Generation Service...")

    generation_service = create_generation_service(
        output_root=str(output_root)
    )

    result = generation_service.generate_project(
        project_name=PROJECT_NAME,
        developer_output=developer_output,
    )

    print("✅ Generation Service completed")

    print("\n" + "=" * 70)
    print("GENERATION RESULT")
    print("=" * 70)

    print(f"Project name : {result['project_name']}")
    print(f"Project path : {result['project_path']}")
    print(f"File count   : {result['file_count']}")
    print(f"ZIP path     : {result['zip_path']}")

    print("\nGenerated files:")

    for file_path in result["files"]:
        print(f"  ✅ {file_path}")

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("INTEGRATION VALIDATION")
    print("=" * 70)

    generated_root = Path(result["project_path"])
    generated_zip = Path(result["zip_path"])

    # Project directory exists.
    assert generated_root.exists()
    assert generated_root.is_dir()

    print("✅ Generated project directory exists")

    # At least one file generated.
    assert result["file_count"] > 0

    print("✅ Generated project contains files")

    # ZIP exists.
    assert generated_zip.exists()
    assert generated_zip.is_file()

    print("✅ ZIP archive exists")

    # ZIP is non-empty.
    assert generated_zip.stat().st_size > 0

    print("✅ ZIP archive is non-empty")

    # Verify important project concepts were generated.
    files_text = "\n".join(
        path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
        for path in generated_root.rglob("*")
        if path.is_file()
    ).lower()

    important_terms = [
        "admin",
        "doctor",
        "patient",
        "appointment",
        "medical",
        "prisma",
        "jwt",
    ]

    for term in important_terms:
        assert term in files_text, (
            f"Generated project does not contain expected term: {term}"
        )

    print("✅ Generated project content validation passed")

    # Verify ZIP contains files.
    with zipfile.ZipFile(
        generated_zip,
        "r",
    ) as archive:

        zip_names = archive.namelist()

    assert len(zip_names) > 0

    print("✅ ZIP contains generated files")

    print("\n" + "=" * 70)
    print("✅ DEVELOPER → GENERATION INTEGRATION TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()