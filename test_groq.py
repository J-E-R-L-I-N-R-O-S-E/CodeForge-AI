from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL


def main():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    print("Groq model:", GROQ_MODEL)

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Groq test successful",
            }
        ],
    )

    text = response.choices[0].message.content

    print("Response:", text)

    if not text:
        raise RuntimeError("Groq returned an empty response.")

    print("✅ GROQ TEST PASSED")


if __name__ == "__main__":
    main()