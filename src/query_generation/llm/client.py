from openai import OpenAI
from dotenv import load_dotenv

import os

def load_openai_client() -> OpenAI:
    """Loads OpenAI client from environment variable."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing OPENAI_API_KEY in .env file.")
    return OpenAI(api_key=api_key)