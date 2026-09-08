from __future__ import annotations

from typing import Callable, Optional

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

    Provider order:
        Gemini -> OpenRouter -> Groq

    A preferred provider can be supplied for specialized tasks.

    All HTTP-based providers use a bounded timeout so a stalled
    provider cannot block the entire application indefinitely.
    """

    PROVIDER_TIMEOUT = 30.0
    MAX_RETRIES_PER_PROVIDER = 1

    def __init__(self) -> None:
        self.gemini_client: Optional[genai.Client] = None
        self.openrouter_client: Optional[OpenAI] = None
        self.groq_client: Optional[Groq] = None

        if GEMINI_API_KEY:
            self.gemini_client = genai.Client(
                api_key=GEMINI_API_KEY
            )

        if OPENROUTER_API_KEY:
            self.openrouter_client = OpenAI(
                api_key=OPENROUTER_API_KEY,
                base_url=OPENROUTER_BASE_URL,
                timeout=self.PROVIDER_TIMEOUT,
                max_retries=0,
            )

        if GROQ_API_KEY:
            self.groq_client = Groq(
                api_key=GROQ_API_KEY,
                timeout=self.PROVIDER_TIMEOUT,
                max_retries=0,
            )

    # ============================================================
    # Gemini
    # ============================================================

    def _generate_gemini(self, prompt: str) -> str:
        """Generate a response using Gemini."""

        if not self.gemini_client:
            raise RuntimeError(
                "Gemini provider is not configured."
            )

        response = self.gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        text = getattr(response, "text", None)

        if not text or not text.strip():
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    # ============================================================
    # OpenRouter
    # ============================================================

    def _generate_openrouter(self, prompt: str) -> str:
        """Generate a response using OpenRouter."""

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

        if not response.choices:
            raise RuntimeError(
                "OpenRouter returned no choices."
            )

        message = response.choices[0].message
        text = getattr(message, "content", None)

        if not text or not text.strip():
            raise RuntimeError(
                "OpenRouter returned a response without usable text content."
            )

        return text.strip()

    # ============================================================
    # Groq
    # ============================================================

    def _generate_groq(self, prompt: str) -> str:
        """Generate a response using Groq."""

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

        if not response.choices:
            raise RuntimeError(
                "Groq returned no choices."
            )

        message = response.choices[0].message
        text = getattr(message, "content", None)

        if not text or not text.strip():
            raise RuntimeError(
                "Groq returned a response without usable text content."
            )

        return text.strip()

    # ============================================================
    # Response validation
    # ============================================================

    @staticmethod
    def _is_usable_response(response: str) -> bool:
        """Check whether an LLM response contains useful content."""

        if not response or not response.strip():
            return False

        normalized = " ".join(
            response.strip().split()
        ).lower()

        unusable_responses = {
            "user safety: safe",
            "safe",
            "ok",
            "okay",
        }

        if normalized in unusable_responses:
            return False

        return len(normalized) >= 20

    # ============================================================
    # Provider ordering
    # ============================================================

    @staticmethod
    def _provider_priority(
        preferred_provider: Optional[str],
    ) -> list[str]:
        """Return provider order."""

        providers = [
            "gemini",
            "openrouter",
            "groq",
        ]

        if not preferred_provider:
            return providers

        preferred = preferred_provider.lower().strip()

        if preferred not in providers:
            return providers

        return [
            preferred,
            *[
                provider
                for provider in providers
                if provider != preferred
            ],
        ]

    def _get_provider_function(
        self,
        provider_name: str,
    ) -> Callable[[str], str]:
        """Return the generation function for a provider."""

        return {
            "gemini": self._generate_gemini,
            "openrouter": self._generate_openrouter,
            "groq": self._generate_groq,
        }[provider_name]

    # ============================================================
    # Main generation
    # ============================================================

    def generate(
        self,
        prompt: str,
        preferred_provider: Optional[str] = None,
    ) -> str:
        """
        Generate a response using bounded provider fallback.

        Each provider is attempted only once. This prevents a stalled
        or exhausted provider from causing a long blocking loop.
        """

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        providers = self._provider_priority(
            preferred_provider
        )

        errors: list[str] = []

        for provider_name in providers:
            provider_function = self._get_provider_function(
                provider_name
            )

            for attempt in range(
                1,
                self.MAX_RETRIES_PER_PROVIDER + 1,
            ):
                try:
                    print(
                        f"\n[LLM SERVICE] Trying provider: "
                        f"{provider_name} "
                        f"(attempt {attempt}/"
                        f"{self.MAX_RETRIES_PER_PROVIDER})"
                    )

                    response = provider_function(prompt)

                    if not self._is_usable_response(
                        response
                    ):
                        raise RuntimeError(
                            f"{provider_name} returned "
                            f"an unusable response."
                        )

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

        raise RuntimeError(
            "All configured LLM providers failed.\n\n"
            + "\n".join(errors)
        )