import json

from crewai import Crew, Process

from agents.requirement_agent import create_requirement_agent
from tasks.requirement_tasks import create_requirement_analysis_task


PROJECT_IDEA = """
I want to build a Hospital Management System for a hospital.
It should manage patients, doctors, appointments, and medical records.
"""


def run_requirement_round(
    agent,
    project_idea: str,
    previous_answers: str,
    round_number: int,
) -> dict:
    """Run one clarification round and return the parsed JSON result."""

    task = create_requirement_analysis_task(
        agent=agent,
        project_idea=project_idea,
        previous_answers=previous_answers,
        round_number=round_number,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    raw_result = str(result).strip()

    # Defensive handling in case the model adds code fences.
    if raw_result.startswith("```"):
        raw_result = raw_result.replace("```json", "")
        raw_result = raw_result.replace("```", "")
        raw_result = raw_result.strip()

    try:
        return json.loads(raw_result)
    except json.JSONDecodeError as exc:
        print("\n❌ Invalid JSON returned by Requirement Agent.")
        print("\nRaw result:")
        print(raw_result)
        raise exc


def print_round(result: dict) -> None:
    """Display a readable clarification round."""

    round_info = result["clarification_round"]

    print("\n" + "=" * 70)
    print(f"ROUND {round_info['round_number']}: {round_info['title']}")
    print("=" * 70)

    print("\nReason:")
    print(round_info["reason"])

    print("\nExplicit requirements:")
    for item in result["explicit_requirements"]:
        print(f"  ✅ {item}")

    print("\nInferred information:")
    for item in result["inferred_information"]:
        print(f"  ⚠️ {item}")

    print("\nMissing information:")
    for item in result["missing_information"]:
        print(f"  ❓ {item}")

    print("\nClarification questions:")
    for index, question in enumerate(
        result["clarification_questions"],
        start=1,
    ):
        print(f"  {index}. {question}")

    print(f"\nCompleteness: {result['completeness']}")


def main() -> None:
    print("=" * 70)
    print("CodeForge AI — Iterative Requirement Clarification Test")
    print("=" * 70)

    agent = create_requirement_agent()

    # ----------------------------------------------------------
    # ROUND 1
    # ----------------------------------------------------------

    result_round_1 = run_requirement_round(
        agent=agent,
        project_idea=PROJECT_IDEA,
        previous_answers="",
        round_number=1,
    )

    print_round(result_round_1)

    if result_round_1["completeness"] == "COMPLETE":
        print("\n✅ Requirements are already sufficiently complete.")
        return

    # ----------------------------------------------------------
    # SIMULATED USER ANSWERS
    # ----------------------------------------------------------
    #
    # Later, Streamlit will replace this hardcoded block with
    # actual answers entered by the user.
    #

    user_answers_round_1 = """
    The system should be a web application.

    The users are Admin, Doctor, and Patient.

    The project should focus only on patient management,
    doctor management, appointment management, and medical
    records. Billing, pharmacy, and laboratory modules are
    not required for this project.
    """

    print("\n" + "=" * 70)
    print("SIMULATED USER ANSWERS — ROUND 1")
    print("=" * 70)
    print(user_answers_round_1.strip())

    # ----------------------------------------------------------
    # ROUND 2
    # ----------------------------------------------------------

    result_round_2 = run_requirement_round(
        agent=agent,
        project_idea=PROJECT_IDEA,
        previous_answers=user_answers_round_1,
        round_number=2,
    )

    print_round(result_round_2)


if __name__ == "__main__":
    main()