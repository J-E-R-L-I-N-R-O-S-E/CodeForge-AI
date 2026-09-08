from crew import run_demo


def main() -> None:
    print("Starting CodeForge AI CrewAI test...\n")

    result = run_demo()

    print("\nCrewAI test completed successfully!")
    print("\nFinal result:")
    print(result)


if __name__ == "__main__":
    main()