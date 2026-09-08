import os

from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------
# Gemini
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.6-flash"


# ---------------------------------------------------------
# OpenRouter
# ---------------------------------------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_MODEL = "openrouter/free"

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


# ---------------------------------------------------------
# Groq
# ---------------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Keep the model configurable so we can change it later
# without modifying the application code.
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")