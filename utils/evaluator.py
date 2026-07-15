import json
import re

from utils.gemini_client import generate_text


def evaluate_answer(question, answer):
    """Evaluate an answer and return predictable feedback data for the app."""
    prompt = f"""
You are a supportive interview coach. Evaluate the candidate's answer below.
Be honest, specific, and encouraging. Do not claim skills or facts not stated by
the candidate. Return ONLY valid JSON with this exact shape:

{{
  "score": 0,
  "strengths": ["short point", "short point"],
  "improvements": ["short point", "short point"],
  "better_structure": ["step 1", "step 2", "step 3"]
}}

Score must be a whole number from 1 to 10. Give 2 or 3 items in each list.

Interview question:
{question}

Candidate answer:
{answer}
"""

    response_text = generate_text(prompt)
    response_text = re.sub(r"^```json\s*|\s*```$", "", response_text.strip())

    try:
        feedback = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise ValueError("Gemini returned feedback in an unexpected format.") from error

    score = feedback.get("score")
    if not isinstance(score, (int, float)) or not 1 <= score <= 10:
        raise ValueError("Gemini returned an invalid score.")

    return {
        "score": int(round(score)),
        "strengths": feedback.get("strengths", []),
        "improvements": feedback.get("improvements", []),
        "better_structure": feedback.get("better_structure", []),
    }
