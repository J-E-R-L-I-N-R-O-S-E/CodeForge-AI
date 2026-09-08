from memory.memory_service import MemoryService


def main():
    memory = MemoryService()

    project_id = "memory_demo_project"

    # Store demo project information
    memory.store_project_idea(
        project_id=project_id,
        project_idea=(
            "Hospital Management System for managing "
            "patients, doctors, appointments, and medical records."
        ),
    )

    # Store a clarification answer
    memory.store_clarification(
        project_id=project_id,
        round_number=1,
        answer=(
            "The system should be a web application with "
            "Admin, Doctor, and Patient users."
        ),
    )

    # Store confirmed requirements
    memory.store_requirements(
        project_id=project_id,
        requirements=[
            "Manage patient information.",
            "Manage doctor information.",
            "Manage appointments.",
            "Manage medical records.",
        ],
    )

    # Retrieve project memory
    memories = memory.get_project_memory(
        project_id=project_id
    )

    print("=" * 60)
    print("CODEFORGE AI - MEMORY TEST")
    print("=" * 60)

    print(f"\nProject ID: {project_id}")
    print(f"Memories found: {len(memories)}")

    for item in memories:
        print("\n" + "-" * 60)
        print("ID:", item["id"])
        print("Type:", item["metadata"].get("type"))
        print("Text:")
        print(item["text"])

    # Semantic search
    results = memory.search(
        "patients appointments medical records",
        n_results=5,
    )

    print("\n" + "=" * 60)
    print("SEMANTIC SEARCH")
    print("=" * 60)

    for item in results:
        print("\nID:", item["id"])
        print("Distance:", item["distance"])
        print("Text:", item["text"])


if __name__ == "__main__":
    main()