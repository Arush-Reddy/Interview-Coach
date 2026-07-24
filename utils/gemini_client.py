import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv(Path(__file__).resolve().parent.parent / ".env")

TEXT_MODELS = ("gemini-3.1-flash-lite", "gemini-3.1-flash-lite-preview")


def _get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets.get("GEMINI_API_KEY")
    except (FileNotFoundError, KeyError):
        return None


def generate_text(prompt):
    """Generate text with Gemini and retry once with the backup model."""
    api_key = _get_api_key()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from .env or Streamlit secrets."
        )

    client = genai.Client(api_key=api_key)
    last_error = None

    for model in TEXT_MODELS:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            if response.text and response.text.strip():
                return response.text.strip()
        except Exception as error:
            last_error = error

    if last_error:
        raise last_error

    raise RuntimeError("Gemini returned an empty response.")
