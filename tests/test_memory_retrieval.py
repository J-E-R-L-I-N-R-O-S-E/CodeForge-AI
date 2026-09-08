from memory.memory_service import MemoryService


def main():
    memory = MemoryService()

    project_id = "retrieval_demo"

    # Store project context
    memory.store_project_idea(
        project_id=project_id,
        project_idea=(
            "Hospital Management System for managing "
            "patients, doctors, appointments, and medical records."
        ),
    )

    memory.store_clarification(
        project_id=project_id,
        round_number=1,
        answer=(
            "The application is a web application with "
            "Admin, Doctor, and Patient users."
        ),
    )

    memory.store_requirements(
        project_id=project_id,
        requirements=[
            "Patients can book appointments.",
            "Doctors can create medical records.",
            "Admins can manage patient records.",
        ],
    )

    # Search ChromaDB
    query = "web application Admin Doctor Patient appointments"

    results = memory.search(
        query=query,
        n_results=5,
    )

    print("=" * 60)
    print("CODEFORGE AI - MEMORY RETRIEVAL TEST")
    print("=" * 60)

    print("\nQuery:")
    print(query)

    print(f"\nResults found: {len(results)}")

    for index, item in enumerate(results, start=1):
        print("\n" + "-" * 60)
        print(f"RESULT {index}")
        print("ID:", item["id"])
        print(
            "Type:",
            item["metadata"].get("type", "unknown"),
        )
        print("Project ID:", item["metadata"].get("project_id"))
        print("Text:")
        print(item["text"])

    # Build the exact context format used by RequirementService
    memory_context = "\n\n".join(
        (
            f"Memory ({item['metadata'].get('type', 'unknown')}):\n"
            f"{item['text']}"
        )
        for item in results
    )

    print("\n" + "=" * 60)
    print("RETRIEVED MEMORY CONTEXT")
    print("=" * 60)
    print(memory_context)


if __name__ == "__main__":
    main()