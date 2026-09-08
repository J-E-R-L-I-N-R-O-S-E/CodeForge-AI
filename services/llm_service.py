from __future__ import annotations

from typing import Optional

from google import genai
from groq import Groq
from openai import OpenAI

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
)


class LLMService:
    """
    Central LLM provider service for CodeForge AI.

    Provider priority:
        1. Gemini
        2. OpenRouter
        3. Groq

    A failed provider does not immediately terminate the workflow.
    The service attempts the next configured provider.
    """

    def __init__(self) -> None:

        self.gemini_client: Optional[genai.Client] = None
        self.openrouter_client: Optional[OpenAI] = None
        self.groq_client: Optional[Groq] = None

        # -------------------------------------------------
        # Gemini
        # -------------------------------------------------

        if GEMINI_API_KEY:
            self.gemini_client = genai.Client(
                api_key=GEMINI_API_KEY
            )

        # -------------------------------------------------
        # OpenRouter
        # -------------------------------------------------

        if OPENROUTER_API_KEY:
            self.openrouter_client = OpenAI(
                api_key=OPENROUTER_API_KEY,
                base_url=OPENROUTER_BASE_URL,
            )

        # -------------------------------------------------
        # Groq
        # -------------------------------------------------

        if GROQ_API_KEY:
            self.groq_client = Groq(
                api_key=GROQ_API_KEY
            )

    # =====================================================
    # Gemini
    # =====================================================

    def _generate_gemini(self, prompt: str) -> str:

        if not self.gemini_client:
            raise RuntimeError(
                "Gemini provider is not configured."
            )

        response = self.gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        text = response.text

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    # =====================================================
    # OpenRouter
    # =====================================================

    def _generate_openrouter(self, prompt: str) -> str:

        if not self.openrouter_client:
            raise RuntimeError(
                "OpenRouter provider is not configured."
            )

        response = self.openrouter_client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        text = response.choices[0].message.content

        if not text:
            raise RuntimeError(
                "OpenRouter returned an empty response."
            )

        return text.strip()

    # =====================================================
    # Groq
    # =====================================================

    def _generate_groq(self, prompt: str) -> str:

        if not self.groq_client:
            raise RuntimeError(
                "Groq provider is not configured."
            )

        response = self.groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        text = response.choices[0].message.content

        if not text:
            raise RuntimeError(
                "Groq returned an empty response."
            )

        return text.strip()

    # =====================================================
    # Public generation method
    # =====================================================

    def generate(
        self,
        prompt: str,
        preferred_provider: Optional[str] = None,
    ) -> str:
        """
        Generate a response using the configured providers.

        Default fallback order:
            Gemini → OpenRouter → Groq

        preferred_provider can be:
            "gemini"
            "openrouter"
            "groq"
        """

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        providers = [
            ("gemini", self._generate_gemini),
            ("openrouter", self._generate_openrouter),
            ("groq", self._generate_groq),
        ]

        # -------------------------------------------------
        # Preferred provider goes first
        # -------------------------------------------------

        if preferred_provider:

            preferred_provider = preferred_provider.lower()

            providers.sort(
                key=lambda item: (
                    0
                    if item[0] == preferred_provider
                    else 1
                )
            )

        errors: list[str] = []

        # -------------------------------------------------
        # Try providers sequentially
        # -------------------------------------------------

        for provider_name, provider_function in providers:

            try:

                print(
                    f"\n[LLM SERVICE] Trying provider: "
                    f"{provider_name}"
                )

                response = provider_function(prompt)

                print(
                    f"[LLM SERVICE] Success: "
                    f"{provider_name}"
                )

                return response

            except Exception as exc:

                error_message = (
                    f"{provider_name}: "
                    f"{type(exc).__name__}: {exc}"
                )

                errors.append(error_message)

                print(
                    f"[LLM SERVICE] Failed: "
                    f"{error_message}"
                )

        # -------------------------------------------------
        # Nothing worked
        # -------------------------------------------------

        raise RuntimeError(
            "All configured LLM providers failed.\n\n"
            + "\n".join(errors)
        )


if __name__ == "__main__":

    service = LLMService()

    result = service.generate(
        "Reply only with: "
        "CodeForge AI multi-LLM service is working."
    )

    print("\n" + "=" * 60)
    print("LLM SERVICE RESULT")
    print("=" * 60)
    print(result)