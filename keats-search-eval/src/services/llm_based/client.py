from openai import OpenAI
from dotenv import load_dotenv

import os


def load_openai_client() -> OpenAI:
    """Loads OpenAI client from environment variable."""
    load_dotenv()
    api_key = os.getenv("PROJ_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing OPENAI_API_KEY or PROJ_OPENAI_API_KEY.")
    return OpenAI(api_key=api_key)
