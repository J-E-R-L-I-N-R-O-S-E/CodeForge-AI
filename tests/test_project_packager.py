from pathlib import Path

from tools.project_packager import create_project_packager


def main():
    print("=" * 70)
    print("CODEFORGE AI - PROJECT PACKAGER TEST")
    print("=" * 70)

    project_directory = Path("outputs") / "test-generated-project"

    if not project_directory.exists():
        raise FileNotFoundError(
            "Run the code generator test first."
        )

    packager = create_project_packager(
        output_root="outputs"
    )

    print("\nCreating ZIP archive...")

    zip_path = packager.create_zip(
        project_name="test-generated-project",
        project_directory=project_directory,
    )

    assert zip_path.exists()
    assert zip_path.suffix == ".zip"

    print(f"✅ ZIP created: {zip_path}")

    print("\nChecking ZIP file size...")

    assert zip_path.stat().st_size > 0

    print("✅ ZIP file validation passed")

    print("\n" + "=" * 70)
    print("✅ PROJECT PACKAGER TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()