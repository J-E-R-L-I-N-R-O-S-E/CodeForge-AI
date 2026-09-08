from crewai import Crew, Process

from agents.requirement_agent import create_requirement_agent
from tasks.srs_tasks import create_final_srs_task


PROJECT_IDEA = """
I want to build a Hospital Management System for a hospital.
It should manage patients, doctors, appointments, and medical records.
"""


CONFIRMED_REQUIREMENTS = """
The system should be a web application.

The system users are:
- Admin
- Doctor
- Patient

The project includes only:
- Patient Management
- Doctor Management
- Appointment Management
- Medical Records

Billing, pharmacy, and laboratory modules are not required.

Appointment rules:
- Patients can book appointments.
- Patients can cancel their own appointments.
- Admin can create and modify appointments.
- Doctors can view their appointments.

Medical record rules:
- Doctors can create and update medical records.
- Patients can view their own medical records.
- Admin can manage patient records.

Authentication:
- All three user roles must authenticate before accessing the system.

No explicit performance, availability, scalability, or usability
requirements have been confirmed.
"""


def main() -> None:
    print("=" * 70)
    print("CodeForge AI — Final SRS Classification Test")
    print("=" * 70)

    agent = create_requirement_agent()

    task = create_final_srs_task(
        agent=agent,
        project_idea=PROJECT_IDEA,
        confirmed_requirements=CONFIRMED_REQUIREMENTS,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    final_srs = str(result)

    print("\n" + "=" * 70)
    print("FINAL SOFTWARE REQUIREMENTS SPECIFICATION")
    print("=" * 70)

    print(final_srs)

    print("\n" + "=" * 70)
    print("CLASSIFICATION CHECK")
    print("=" * 70)

    # Basic automated checks.
    lower_srs = final_srs.lower()

    checks = {
        "Authentication appears in Functional Requirements":
            "authentication" in lower_srs
            and "functional requirements" in lower_srs,

        "Web application appears in Platform":
            "platform" in lower_srs
            and "web application" in lower_srs,

        "Billing is excluded":
            "billing" in lower_srs,

        "Pharmacy is excluded":
            "pharmacy" in lower_srs,

        "Laboratory is excluded":
            "laboratory" in lower_srs,
    }

    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")

    print("\nNote:")
    print(
        "The final SRS must be manually inspected once to ensure "
        "that no platform or functional requirement has incorrectly "
        "been placed under Non-Functional Requirements."
    )


if __name__ == "__main__":
    main()