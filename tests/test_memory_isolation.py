from memory.memory_service import MemoryService


def main():
    memory = MemoryService()

    project_a = "project_a_demo"
    project_b = "project_b_demo"

    # ---------------------------------------------------------
    # Store Project A memory
    # ---------------------------------------------------------

    memory.store_project_idea(
        project_id=project_a,
        project_idea=(
            "Hospital Management System for patients and doctors."
        ),
    )

    memory.store_clarification(
        project_id=project_a,
        round_number=1,
        answer=(
            "Project A is a web application with Admin and Doctor users."
        ),
    )

    # ---------------------------------------------------------
    # Store Project B memory
    # ---------------------------------------------------------

    memory.store_project_idea(
        project_id=project_b,
        project_idea=(
            "Library Management System for books and members."
        ),
    )

    memory.store_clarification(
        project_id=project_b,
        round_number=1,
        answer=(
            "Project B is a desktop application with Librarian and Member users."
        ),
    )

    # ---------------------------------------------------------
    # Search ONLY Project A
    # ---------------------------------------------------------

    results_a = memory.search(
        query="users application",
        n_results=10,
        project_id=project_a,
    )

    # ---------------------------------------------------------
    # Search ONLY Project B
    # ---------------------------------------------------------

    results_b = memory.search(
        query="users application",
        n_results=10,
        project_id=project_b,
    )

    print("=" * 60)
    print("CODEFORGE AI - MEMORY ISOLATION TEST")
    print("=" * 60)

    print("\nPROJECT A RESULTS")
    print("-" * 60)

    for item in results_a:
        print(
            item["id"],
            "|",
            item["metadata"].get("project_id"),
        )
        print(item["text"])
        print()

    print("\nPROJECT B RESULTS")
    print("-" * 60)

    for item in results_b:
        print(
            item["id"],
            "|",
            item["metadata"].get("project_id"),
        )
        print(item["text"])
        print()

    # ---------------------------------------------------------
    # Validate isolation
    # ---------------------------------------------------------

    a_isolated = all(
        item["metadata"].get("project_id") == project_a
        for item in results_a
    )

    b_isolated = all(
        item["metadata"].get("project_id") == project_b
        for item in results_b
    )

    print("=" * 60)
    print("ISOLATION RESULT")
    print("=" * 60)

    print("Project A isolated:", a_isolated)
    print("Project B isolated:", b_isolated)

    if a_isolated and b_isolated:
        print("\n✅ MEMORY ISOLATION PASSED")
    else:
        print("\n❌ MEMORY ISOLATION FAILED")


if __name__ == "__main__":
    main()