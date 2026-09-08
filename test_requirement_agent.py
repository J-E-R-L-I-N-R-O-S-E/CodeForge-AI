import json

from crewai import Crew, Process

from agents.requirement_agent import create_requirement_agent
from tasks.requirement_tasks import create_requirement_analysis_task


def main() -> None:
    print("Starting CodeForge AI Requirement Agent test...\n")

    project_idea = """
    I want to build a Hospital Management System for a hospital.
    It should manage patients, doctors, appointments, and medical records.
    """

    agent = create_requirement_agent()

    task = create_requirement_analysis_task(
        agent=agent,
        project_idea=project_idea,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    print("\n" + "=" * 70)
    print("STRICT REQUIREMENT ANALYSIS")
    print("=" * 70)

    raw_result = str(result)

    print(raw_result)

    # Validate that the agent returned JSON.
    try:
        parsed = json.loads(raw_result)

        required_keys = {
            "project_understanding",
            "explicit_requirements",
            "inferred_information",
            "missing_information",
            "clarification_questions",
            "completeness",
        }

        missing_keys = required_keys - parsed.keys()

        if missing_keys:
            print("\n❌ Missing JSON fields:")
            for key in sorted(missing_keys):
                print(f"- {key}")
            return

        print("\n" + "=" * 70)
        print("JSON VALIDATION")
        print("=" * 70)
        print("✅ Valid JSON")
        print("✅ Required fields present")
        print(f"✅ Completeness: {parsed['completeness']}")

    except json.JSONDecodeError:
        print("\n❌ Agent did not return valid JSON.")


if __name__ == "__main__":
    main()