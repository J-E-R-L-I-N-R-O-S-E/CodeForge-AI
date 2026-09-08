from crewai import Task


def create_requirement_analysis_prompt(
    project_idea: str,
    previous_answers: str = "",
    round_number: int = 1,
) -> str:
    """
    Create the requirement-analysis prompt used by the
    provider-independent LLMService.
    """

    previous_context = (
        previous_answers.strip()
        if previous_answers.strip()
        else "No previous clarification answers. This is the first analysis."
    )

    return f"""
Analyze the following software project idea for CodeForge AI.

================ PROJECT IDEA ================

{project_idea}

===============================================

================ PREVIOUS USER ANSWERS ================

{previous_context}

========================================================

This is clarification round {round_number}.

========================================================
CORE CLASSIFICATION
========================================================

Every piece of information belongs to one of these categories:

1. EXPLICIT
   Directly stated by the user in the original idea or previous answers.

2. INFERRED
   A reasonable interpretation, but not confirmed by the user.

3. MISSING
   Information not yet provided by the user.

========================================================
IMPORTANT COMPLETENESS RULE
========================================================

Not every missing detail should block SRS generation.

Separate missing information into:

A. ESSENTIAL MISSING INFORMATION

Information necessary to create a useful first SRS.

Examples:

- Main purpose of the system
- Core functionality
- Important user roles
- Major workflows
- Critical permissions
- Explicit project scope
- Important inclusions/exclusions

B. OPTIONAL MISSING INFORMATION

Useful details that can be decided later by the Architect Agent,
Developer Agent, or during refinement.

Examples:

- Technology stack preferences
- Hosting preferences
- Detailed compliance standards when not required for the demo
- Exact database fields when architecture has not started
- Minor workflow edge cases
- Detailed account onboarding decisions when not necessary
  to describe the core system
  

========================================================
MANDATORY FIRST-ROUND CHECKLIST
========================================================

For clarification round 1, perform a mandatory completeness check
against the following minimum checklist:

1. PURPOSE
   Is the main purpose of the system explicitly confirmed?

2. USERS AND ROLES
   Are the important user roles explicitly confirmed?

3. CORE FEATURES
   Are the main system features explicitly confirmed?

4. MAJOR WORKFLOWS AND PERMISSIONS
   Are the important workflows and critical access permissions
   sufficiently confirmed?

5. SCOPE BOUNDARIES
   Are important inclusions and exclusions explicitly confirmed?

6. PLATFORM
   Is the delivery platform explicitly confirmed when it is
   relevant to the requested project?

FIRST-ROUND COMPLETION RULE:

For round 1, do NOT return COMPLETE unless all applicable
checklist items are sufficiently confirmed by the user.

If one or more checklist items are not confirmed:

- completeness MUST be INCOMPLETE.
- clarification_questions MUST contain questions addressing
  the highest-priority missing checklist items.
- Ask at most 3 questions.
- Do not ask about optional technical details at this stage.

After round 1, use the normal essential-vs-optional completeness
rule.

The purpose of this checklist is to make the first clarification
round reliable and predictable while still allowing the AI to
reason about what information is essential.


========================================================
COMPLETENESS RULE
========================================================

Use:

COMPLETE

when there is enough ESSENTIAL information to produce a useful
first Software Requirements Specification.

Use:

INCOMPLETE

only when important ESSENTIAL information is still missing.

OPTIONAL missing information must NEVER by itself cause
INCOMPLETE.

When enough essential information exists:

- completeness = COMPLETE
- clarification_questions = []

Do not continue asking questions simply to make the specification
perfect.

CodeForge AI should generate a useful first SRS and allow later
refinement.

========================================================
STRICT CLASSIFICATION RULES
========================================================

- Never convert an inference into an explicit requirement.
- Never invent requirements.
- Never assume roles, permissions, workflows, technologies,
  platforms, integrations, regulations, or constraints.
- Previous user answers become EXPLICIT.
- If an answer resolves a missing item, remove it from MISSING.
- Never repeat an already answered question.
- Prefer clarification over guessing.
- Do not use general domain knowledge as if the user provided it.

========================================================
ITERATIVE QUESTION STRATEGY
========================================================

You MUST NOT ask all possible questions at once.

For each round:

- Maximum 3 questions.
- Ask only about the highest-priority ESSENTIAL missing information.
- Group related questions under a logical round title.
- Do not repeat previous questions.
- Stop asking questions once the essential information is sufficient.

Possible round titles:

- Basic Scope
- Users and Access
- Core Workflows
- Business Rules
- Security and Data
- Other Essential Requirements

========================================================
ANALYSIS
========================================================

A. PROJECT UNDERSTANDING

Explain only what is supported by the user's information.

B. EXPLICIT REQUIREMENTS

List only confirmed requirements.

C. INFERRED INFORMATION

List reasonable but unconfirmed interpretations.

D. ESSENTIAL MISSING INFORMATION

List only unresolved information that is necessary for a useful
first SRS.

E. OPTIONAL MISSING INFORMATION

List unresolved information that can safely be addressed later.

F. NEXT CLARIFICATION ROUND

Select the highest-priority essential topic.

G. CLARIFICATION QUESTIONS

Ask at most 3 questions.

H. COMPLETENESS

Determine whether enough essential information exists for the first SRS.

========================================================
OUTPUT FORMAT
========================================================

Return ONLY valid JSON.

Do not use Markdown.

Do not use ```json fences.

Use exactly this structure:

{{
  "project_understanding": "string",

  "explicit_requirements": [
    "string"
  ],

  "inferred_information": [
    "string"
  ],

  "essential_missing_information": [
    "string"
  ],

  "optional_missing_information": [
    "string"
  ],

  "clarification_round": {{
    "round_number": {round_number},
    "title": "string",
    "reason": "string"
  }},

  "clarification_questions": [
    "string"
  ],

  "completeness": "COMPLETE or INCOMPLETE"
}}

IMPORTANT:

If completeness is COMPLETE:

- clarification_questions MUST be []

If completeness is INCOMPLETE:

- clarification_questions must contain 1 to 3 questions.
- Questions must address ESSENTIAL missing information only.
"""


def create_requirement_analysis_task(
    agent,
    project_idea: str,
    previous_answers: str = "",
    round_number: int = 1,
) -> Task:
    """
    Backward-compatible CrewAI Task version.

    This is kept so existing tests and older code can still
    create a CrewAI Task if needed.
    """

    prompt = create_requirement_analysis_prompt(
        project_idea=project_idea,
        previous_answers=previous_answers,
        round_number=round_number,
    )

    return Task(
        description=prompt,
        expected_output="""
A valid JSON object containing:

project_understanding,
explicit_requirements,
inferred_information,
essential_missing_information,
optional_missing_information,
clarification_round,
clarification_questions,
completeness.

Return JSON only.
""",
        agent=agent,
    )