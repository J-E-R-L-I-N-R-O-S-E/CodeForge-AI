from services.llm_service import LLMService


def main():
    print("=" * 60)
    print("CODEFORGE AI - MULTI-LLM SERVICE TEST")
    print("=" * 60)

    service = LLMService()

    prompt = (
        "Reply only with exactly: "
        "CodeForge AI multi-LLM service is working."
    )

    try:
        result = service.generate(prompt)

        print("\nFinal Response:")
        print(result)

    except Exception as exc:
        print("\nLLM SERVICE FAILED")
        print(type(exc).__name__)
        print(exc)


if __name__ == "__main__":
    main()