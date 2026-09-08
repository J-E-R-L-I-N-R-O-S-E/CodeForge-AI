from openai import OpenAI

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
)


def main():
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
    )

    prompt = """
Return ONLY valid JSON.

Use exactly this structure:

{
  "status": "success",
  "message": "OpenRouter structured output works"
}
"""

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    print("=" * 60)
    print("OPENROUTER MODEL TEST")
    print("=" * 60)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()