from pathlib import Path

from services.project_inspector import ProjectInspector


def main():
    project_path = Path("outputs/test-inspector-limit")
    project_path.mkdir(parents=True, exist_ok=True)

    large_file = project_path / "large.js"

    large_file.write_text(
        "A" * 20000,
        encoding="utf-8",
    )

    inspector = ProjectInspector(project_path)

    code = inspector.get_code(max_chars=12000)

    print(f"Generated code size: {len(code)} characters")

    assert len(code) <= 12000

    print("✅ project code size limit enforced")
    print("✅ Phase 12 Prompt Size Control Test PASSED")


if __name__ == "__main__":
    main()