from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional

from services.llm_service import LLMService
from tasks.requirement_tasks import create_requirement_analysis_prompt
from tasks.srs_tasks import create_final_srs_prompt


@dataclass
class RequirementState:
    """Stores the current state of a CodeForge AI requirement session."""

    project_idea: str
    round_number: int = 0

    explicit_requirements: list[str] = field(default_factory=list)
    inferred_information: list[str] = field(default_factory=list)

    essential_missing_information: list[str] = field(default_factory=list)
    optional_missing_information: list[str] = field(default_factory=list)

    clarification_questions: list[str] = field(default_factory=list)
    clarification_round_title: str = ""
    clarification_round_reason: str = ""

    completeness: str = "INCOMPLETE"

    user_answers: list[str] = field(default_factory=list)

    final_srs: str = ""


class RequirementService:
    """
    Orchestrates the complete Requirement Agent workflow.

    LLM fallback:

        Gemini
           ↓
        OpenRouter
           ↓
        Groq

    The Requirement workflow itself is provider-independent.
    """

    MAX_ROUNDS = 5

    def __init__(self) -> None:
        self.llm_service = LLMService()

    # =========================================================
    # Utility methods
    # =========================================================

    @staticmethod
    def _clean_json_response(raw_result: str) -> str:
        """Remove accidental Markdown code fences around JSON."""

        cleaned = raw_result.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "", 1)
            cleaned = cleaned.replace("```", "")

        return cleaned.strip()

    @classmethod
    def _parse_analysis_result(
        cls,
        raw_result: str,
    ) -> dict[str, Any]:
        """Parse and validate Requirement Agent JSON output."""

        cleaned = cls._clean_json_response(raw_result)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Requirement Agent returned invalid JSON."
            ) from exc

        if not isinstance(parsed, dict):
            raise ValueError(
                "Requirement Agent response must be a JSON object."
            )

        required_keys = {
            "project_understanding",
            "explicit_requirements",
            "inferred_information",
            "essential_missing_information",
            "optional_missing_information",
            "clarification_round",
            "clarification_questions",
            "completeness",
        }

        missing_keys = required_keys - parsed.keys()

        if missing_keys:
            raise ValueError(
                "Requirement Agent response is missing fields: "
                + ", ".join(sorted(missing_keys))
            )

        if parsed["completeness"] not in {
            "COMPLETE",
            "INCOMPLETE",
        }:
            raise ValueError(
                "Invalid completeness value returned by "
                "Requirement Agent."
            )

        if not isinstance(
            parsed["clarification_questions"],
            list,
        ):
            raise ValueError(
                "clarification_questions must be a list."
            )

        if len(parsed["clarification_questions"]) > 3:
            raise ValueError(
                "Requirement Agent returned more than 3 questions."
            )

        if not isinstance(
            parsed["explicit_requirements"],
            list,
        ):
            raise ValueError(
                "explicit_requirements must be a list."
            )

        if not isinstance(
            parsed["inferred_information"],
            list,
        ):
            raise ValueError(
                "inferred_information must be a list."
            )

        if not isinstance(
            parsed["essential_missing_information"],
            list,
        ):
            raise ValueError(
                "essential_missing_information must be a list."
            )

        if not isinstance(
            parsed["optional_missing_information"],
            list,
        ):
            raise ValueError(
                "optional_missing_information must be a list."
            )

        if not isinstance(
            parsed["clarification_round"],
            dict,
        ):
            raise ValueError(
                "clarification_round must be an object."
            )

        clarification_round = parsed["clarification_round"]

        for key in (
            "round_number",
            "title",
            "reason",
        ):
            if key not in clarification_round:
                raise ValueError(
                    "clarification_round is missing field: "
                    + key
                )

        if parsed["completeness"] == "COMPLETE":

            if parsed["clarification_questions"]:
                raise ValueError(
                    "Complete analysis cannot contain "
                    "clarification questions."
                )

            if parsed["essential_missing_information"]:
                raise ValueError(
                    "Complete analysis cannot contain "
                    "essential missing information."
                )

        if parsed["completeness"] == "INCOMPLETE":

            if not parsed["clarification_questions"]:
                raise ValueError(
                    "Incomplete analysis must contain "
                    "clarification questions."
                )

            if not parsed["essential_missing_information"]:
                raise ValueError(
                    "Incomplete analysis must identify "
                    "at least one essential missing item."
                )

        return parsed

    # =========================================================
    # Requirement analysis
    # =========================================================

    def analyze(
        self,
        project_idea: str,
        previous_answers: Optional[str] = None,
        round_number: int = 1,
    ) -> dict[str, Any]:
        """
        Run one requirement-analysis round through the
        central multi-LLM service.
        """

        if not project_idea or not project_idea.strip():
            raise ValueError(
                "Project idea cannot be empty."
            )

        previous_answers = previous_answers or ""

        prompt = create_requirement_analysis_prompt(
            project_idea=project_idea,
            previous_answers=previous_answers,
            round_number=round_number,
        )

        print("\n" + "=" * 60)
        print(
            f"[REQUIREMENT SERVICE] ANALYSIS ROUND {round_number}"
        )
        print("=" * 60)

        raw_result = self.llm_service.generate(prompt)

        return self._parse_analysis_result(raw_result)

    # =========================================================
    # State update
    # =========================================================

    @staticmethod
    def apply_analysis(
        state: RequirementState,
        analysis: dict[str, Any],
    ) -> RequirementState:
        """Apply an analysis response to the current state."""

        state.round_number = analysis[
            "clarification_round"
        ]["round_number"]

        state.explicit_requirements = analysis[
            "explicit_requirements"
        ]

        state.inferred_information = analysis[
            "inferred_information"
        ]

        state.essential_missing_information = analysis[
            "essential_missing_information"
        ]

        state.optional_missing_information = analysis[
            "optional_missing_information"
        ]

        state.clarification_questions = analysis[
            "clarification_questions"
        ]

        state.clarification_round_title = analysis[
            "clarification_round"
        ]["title"]

        state.clarification_round_reason = analysis[
            "clarification_round"
        ]["reason"]

        state.completeness = analysis[
            "completeness"
        ]

        return state

    # =========================================================
    # Start
    # =========================================================

    def start(
        self,
        project_idea: str,
    ) -> RequirementState:
        """Start a new requirement-analysis session."""

        if not project_idea or not project_idea.strip():
            raise ValueError(
                "Project idea cannot be empty."
            )

        state = RequirementState(
            project_idea=project_idea.strip(),
        )

        analysis = self.analyze(
            project_idea=state.project_idea,
            previous_answers="",
            round_number=1,
        )

        return self.apply_analysis(
            state,
            analysis,
        )

    # =========================================================
    # Continue session
    # =========================================================

    def continue_session(
        self,
        state: RequirementState,
        user_answer: str,
    ) -> RequirementState:
        """
        Add the user's clarification answer and run the
        next requirement-analysis round.
        """

        if not user_answer or not user_answer.strip():
            raise ValueError(
                "User answer cannot be empty."
            )

        if state.completeness == "COMPLETE":
            raise ValueError(
                "Requirement session is already complete."
            )

        if state.round_number >= self.MAX_ROUNDS:
            raise RuntimeError(
                "Maximum clarification rounds reached."
            )

        answer = user_answer.strip()

        state.user_answers.append(answer)

        combined_answers = "\n\n".join(
            (
                f"User clarification round "
                f"{index + 1}:\n{answer_text}"
            )
            for index, answer_text in enumerate(
                state.user_answers
            )
        )

        next_round = state.round_number + 1

        analysis = self.analyze(
            project_idea=state.project_idea,
            previous_answers=combined_answers,
            round_number=next_round,
        )

        return self.apply_analysis(
            state,
            analysis,
        )

    # =========================================================
    # Final SRS
    # =========================================================

    def generate_final_srs(
        self,
        state: RequirementState,
    ) -> str:
        """
        Generate the final SRS using the same multi-LLM service.
        """

        if state.completeness != "COMPLETE":
            raise ValueError(
                "Cannot generate final SRS while requirements "
                "are incomplete."
            )

        confirmed_requirements = "\n".join(
            f"- {item}"
            for item in state.explicit_requirements
        )

        prompt = create_final_srs_prompt(
            project_idea=state.project_idea,
            confirmed_requirements=confirmed_requirements,
        )

        print("\n" + "=" * 60)
        print("[FINAL SRS] GENERATING")
        print("=" * 60)

        state.final_srs = self.llm_service.generate(prompt).strip()

        if not state.final_srs:
            raise RuntimeError(
                "Final SRS response was empty."
            )

        print("\n[FINAL SRS] SUCCESS")

        return state.final_srs