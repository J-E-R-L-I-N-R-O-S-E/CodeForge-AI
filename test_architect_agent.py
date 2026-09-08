from agents.architect_agent import create_architect_agent
from tasks.architect_tasks import create_architecture_prompt


PROJECT_IDEA = """
Build a Hospital Management System for managing patients, doctors,
appointments, and medical records.
"""


CONFIRMED_REQUIREMENTS = """
- The system shall be implemented as a web application.
- The system supports three user roles: Admin, Doctor, and Patient.
- The system provides modules for patient management, doctor management,
  appointment management, and medical records.
- Patients can book appointments and cancel their own appointments.
- Admins can create and modify appointments.
- Doctors can view their own appointments.
- Doctors can create and update medical records.
- Patients can view their own medical records.
- Admins can manage patient records.
- All users must authenticate before accessing the system.
- Billing, pharmacy, and laboratory are excluded.
"""


def main():
    agent = create_architect_agent()

    prompt = create_architecture_prompt(
        project_idea=PROJECT_IDEA,
        confirmed_requirements=CONFIRMED_REQUIREMENTS,
    )

    print("=" * 70)
    print("CODEFORGE AI - ARCHITECT AGENT TEST")
    print("=" * 70)

    print("\nGenerating architecture...")

    result = agent.generate(prompt)

    print("\n" + "=" * 70)
    print("ARCHITECTURE RESULT")
    print("=" * 70)

    print(result)


if __name__ == "__main__":
    main()