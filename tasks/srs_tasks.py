from crewai import Task


def create_final_srs_prompt(
   project_idea: str,
   confirmed_requirements: str,
) -> str:
   """
   Create the final SRS-generation prompt.

   This version is provider-independent and can be used
   with Gemini, OpenRouter, or Groq through LLMService.
   """

   return f"""
Generate the final Software Requirements Specification (SRS) for
CodeForge AI using ONLY the confirmed information supplied by the user.

================ ORIGINAL PROJECT IDEA ================

{project_idea}

========================================================

================ CONFIRMED REQUIREMENTS ================

{confirmed_requirements}

========================================================

You are now in the FINAL REQUIREMENTS stage.

The clarification process has been completed.

Do not ask additional questions.

========================================================

CRITICAL RULE — NO INVENTED REQUIREMENTS
========================================================

The final SRS must contain only information confirmed by the user.

NEVER:

- Invent features.
- Invent user roles.
- Invent permissions.
- Invent workflows.
- Invent technologies.
- Invent integrations.
- Invent business rules.
- Invent compliance requirements.
- Convert AI inferences into confirmed requirements.
- Add common industry requirements merely because they are typical.

If a detail is not confirmed by the user, do not present it as a
confirmed requirement.

========================================================

REQUIREMENT CLASSIFICATION
========================================================

Use these definitions strictly.

FUNCTIONAL REQUIREMENTS:

Describe what the system must do.

Examples:

- Authenticate users.
- Manage patients.
- Allow patients to book appointments.
- Allow doctors to create medical records.

NON-FUNCTIONAL REQUIREMENTS:

Describe quality attributes or measurable characteristics of the system.

Examples include:

- Performance
- Availability
- Usability
- Scalability
- Reliability

IMPORTANT:

Only include a non-functional requirement if the user explicitly
confirmed it.

Do NOT turn a platform choice or functional access rule into a
non-functional requirement.

PLATFORM:

Describe the confirmed technical delivery platform.

Example:

- Web application

CONSTRAINTS:

Describe explicit boundaries or restrictions confirmed by the user.

Examples:

- Billing is excluded.
- Pharmacy is excluded.
- Laboratory is excluded.

========================================================

SRS CONTENT
========================================================

Create a structured Software Requirements Specification containing:

1. Project Overview

   - Project name
   - Purpose
   - Scope summary

2. Users and Roles

   - List ONLY confirmed roles.
   - Do not invent responsibilities.

3. Functional Requirements

   - Include only confirmed system behaviors.
   - Use identifiers such as FR-01, FR-02, FR-03.

4. Non-Functional Requirements

   - Include ONLY explicitly confirmed quality requirements.
   - If none were confirmed, clearly state:

   "No explicit non-functional requirements were confirmed."

5. Platform

   - Include confirmed platform requirements here.
   - Do not classify platform as an NFR.

6. Core Features

   - Summarize confirmed functionality.

7. Scope

   - Included functionality.
   - Explicitly excluded functionality.

8. Constraints

   - Include only confirmed constraints or restrictions.

9. Assumptions

   - Include only assumptions explicitly accepted or confirmed by
   the user.
   - Never promote an AI inference into an assumption.

10. Requirements Validation Summary

   - Explain that the SRS was generated from confirmed requirements
   after clarification.

========================================================

CLASSIFICATION EXAMPLES FOR THIS PROJECT
========================================================

The following are examples of how to classify information if present:

"All users must authenticate."

→ FUNCTIONAL REQUIREMENT

"Patients can book appointments."

→ FUNCTIONAL REQUIREMENT

"Doctors can create medical records."

→ FUNCTIONAL REQUIREMENT

"The application must be web-based."

→ PLATFORM

"Billing is not required."

→ SCOPE / CONSTRAINT

"The application must respond within 2 seconds."

→ NON-FUNCTIONAL REQUIREMENT

"System availability must be 99.9%."

→ NON-FUNCTIONAL REQUIREMENT

Only the last two examples should be classified as NFRs if the user
actually confirmed them.

========================================================

QUALITY RULES
========================================================

- Keep requirements precise and testable where possible.

- Preserve the user's confirmed intent.

- Do not make technical architecture decisions.

- Do not select a technology stack.

- Do not design database tables.

- Do not design API endpoints.

- Do not create software architecture.

- Those responsibilities belong to the Architect Agent later.

Return a professional, readable SRS in Markdown.
"""


def create_final_srs_task(
   agent,
   project_idea: str,
   confirmed_requirements: str,
) -> Task:
   """
   Backward-compatible CrewAI Task version.

   Preserved so existing CrewAI-based tests/code can still use it.
   """

   prompt = create_final_srs_prompt(
      project_idea=project_idea,
      confirmed_requirements=confirmed_requirements,
   )

   return Task(
      description=prompt,
      expected_output="""
A professional Software Requirements Specification in Markdown containing:

- Project Overview
- Users and Roles
- Functional Requirements
- Non-Functional Requirements
- Platform
- Core Features
- Scope
- Constraints
- Assumptions
- Requirements Validation Summary

Functional requirements must describe system behavior.

Platform information must not be classified as an NFR.

Only explicitly confirmed quality attributes may appear under
Non-Functional Requirements.

Do not invent requirements.
""",
      agent=agent,
   )