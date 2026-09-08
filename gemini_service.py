from typing import Optional

from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiService:
    """Reusable Gemini API wrapper for CodeForge AI."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model or GEMINI_MODEL

        if not self.api_key:
            raise ValueError(
                "Gemini API key is missing."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """Generate a text response from Gemini."""

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        text = response.text

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()