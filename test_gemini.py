from gemini_service import GeminiService


def main() -> None:
    gemini = GeminiService()

    response = gemini.generate(
        "Reply only with: "
        "CodeForge AI Gemini service is working."
    )

    print(response)


if __name__ == "__main__":
    main()