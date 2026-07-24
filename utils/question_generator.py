import re

from utils.gemini_client import generate_text


def parse_interview_questions(response_text):
    """Parse and validate Gemini's numbered interview-question list."""
    questions = [
        question.strip()
        for question in re.split(r"(?m)^\s*\d+[.)]\s*", response_text)
        if question.strip()
    ]

    if len(questions) != 5:
        raise ValueError("Gemini did not return exactly five questions. Please try again.")

    return questions


def generate_interview_questions(resume_summary):
    """Return five personalized questions as a Python list."""
    prompt = f"""
You are a friendly interview coach.

Using this resume summary, create exactly 5 personalized interview questions:
- 2 questions about the candidate's projects or technical skills
- 2 HR or behavioural questions
- 1 question about their goals or learning journey

Return only a numbered list. Put each full question on one line. Do not include answers.

Resume summary:
{resume_summary}
"""

    response_text = generate_text(prompt)
    return parse_interview_questions(response_text)
