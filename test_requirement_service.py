from services.requirement_service import RequirementService


PROJECT_IDEA = """
Build a Hospital Management System for managing patients, doctors,
appointments, and medical records.
"""


ROUND_1_ANSWER = """
The system should be a web application.

The users are Admin, Doctor, and Patient.

Only patient management, doctor management, appointment management,
and medical records are required.

Billing, pharmacy, and laboratory are not required.
"""


ROUND_2_ANSWER = """
Patients can book appointments and cancel their own appointments.

Admins can create and modify appointments.

Doctors can view their own appointments.

Doctors can create and update medical records.

Patients can view their own medical records.

Admins can manage patient records.

All users must authenticate before accessing the system.
"""


ROUND_3_ANSWER = """
Admins are responsible for creating and managing Doctor accounts
and profiles.

Doctor medical records should contain patient details, diagnosis,
treatment, and prescription information.

There are no special cancellation time limits or appointment
overlap rules beyond the appointment permissions already specified.
"""


ROUND_4_ANSWER = """
Patients will be provided accounts by the Admin.

No specific healthcare compliance standard is required for this
academic project beyond the authentication and access rules
already specified.
"""


def print_state(state, label):
    print("\n" + "=" * 70)
    print(label)
    print("=" * 70)

    print(f"\nRound Number: {state.round_number}")
    print(f"Completeness: {state.completeness}")

    print("\nExplicit Requirements:")
    for item in state.explicit_requirements:
        print(f"  - {item}")

    print("\nInferred Information:")
    for item in state.inferred_information:
        print(f"  - {item}")

    print("\nEssential Missing Information:")
    for item in state.essential_missing_information:
        print(f"  - {item}")

    print("\nOptional Missing Information:")
    for item in state.optional_missing_information:
        print(f"  - {item}")

    print("\nClarification Questions:")
    for index, question in enumerate(
        state.clarification_questions,
        start=1,
    ):
        print(f"  {index}. {question}")

    print("\nClarification Round:")
    print(f"  Title: {state.clarification_round_title}")
    print(f"  Reason: {state.clarification_round_reason}")


def main():
    service = RequirementService()

    print("=" * 70)
    print("CODEFORGE AI - REQUIREMENT SERVICE TEST")
    print("=" * 70)

    print("\nStarting requirement analysis...")

    state = service.start(PROJECT_IDEA)

    print_state(
        state,
        "ROUND 1 RESULT",
    )

    answers = [
        ROUND_1_ANSWER,
        ROUND_2_ANSWER,
        ROUND_3_ANSWER,
        ROUND_4_ANSWER,
    ]

    answer_number = 0

    while (
        state.completeness == "INCOMPLETE"
        and state.round_number < service.MAX_ROUNDS
        and answer_number < len(answers)
    ):
        answer = answers[answer_number]
        answer_number += 1

        print("\n" + "-" * 70)
        print(f"Submitting simulated user answer for Round {state.round_number + 1}")
        print("-" * 70)

        print(answer)

        state = service.continue_session(
            state,
            answer,
        )

        print_state(
            state,
            f"ROUND {state.round_number} RESULT",
        )

    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    if state.completeness == "COMPLETE":
        print("\nRequirements are COMPLETE.")
        print("\nGenerating Final SRS...")

        final_srs = service.generate_final_srs(state)

        print("\n" + "=" * 70)
        print("FINAL SRS")
        print("=" * 70)

        print(final_srs)

    else:
        print("\nRequirements are still INCOMPLETE.")
        print(
            f"Maximum rounds available: {service.MAX_ROUNDS}"
        )

        print("\nRemaining Essential Missing Information:")

        for item in state.essential_missing_information:
            print(f"  - {item}")

        print("\nRemaining Optional Missing Information:")

        for item in state.optional_missing_information:
            print(f"  - {item}")


if __name__ == "__main__":
    main()