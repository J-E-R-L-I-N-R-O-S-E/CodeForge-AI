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

    If one provider fails, the service automatically attempts
    the next configured provider.
    """

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
            )

        if GROQ_API_KEY:
            self.groq_client = Groq(
                api_key=GROQ_API_KEY
            )

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

        text = response.text

        if not text or not text.strip():
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

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
                "OpenRouter returned a response without "
                "usable text content."
            )

        return text.strip()

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
                "Groq returned a response without "
                "usable text content."
            )

        return text.strip()
    @staticmethod
    def _is_usable_response(response: str) -> bool:
        """
        Check whether an LLM response contains meaningful content.

        Rejects empty responses and known non-answer responses such as
        safety-only messages returned by some routed models.
        """

        if not response or not response.strip():
            return False

        normalized = " ".join(response.strip().split()).lower()

        unusable_responses = {
            "user safety: safe",
            "safe",
            "ok",
            "okay",
        }

        if normalized in unusable_responses:
            return False

        # Very short responses are unlikely to be useful for
        # CodeForge's generation tasks.
        if len(normalized) < 20:
            return False

        return True

    def generate(
        self,
        prompt: str,
        preferred_provider: Optional[str] = None,
    ) -> str:
        """
        Generate text using the configured LLM providers.

        Default priority:
            Gemini → OpenRouter → Groq

        If preferred_provider is supplied, that provider
        is attempted first.
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

        if preferred_provider:
            preferred_provider = preferred_provider.lower()

            providers.sort(
                key=lambda item:
                0 if item[0] == preferred_provider else 1
            )

        errors: list[str] = []

        for provider_name, provider_function in providers:
            try:
                print(
                    f"\n[LLM SERVICE] Trying provider: "
                    f"{provider_name}"
                )

                response = provider_function(prompt)

                if not self._is_usable_response(response):
                    raise RuntimeError(
                        f"{provider_name} returned an unusable response."
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