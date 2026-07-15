from utils.gemini_client import generate_text


def summarize_resume(resume_text):
    """Create a concise recruiter-style summary from extracted resume text."""
    resume_text = resume_text[:30000]

    prompt = f"""
You are an experienced technical recruiter helping a student prepare for interviews.

Read the following resume carefully and provide a concise, professional summary.
Use these Markdown headings:

## Candidate Overview
## Skills
## Education
## Experience
## Projects
## Strengths

Keep the summary under 250 words. If a section is absent, write "Not listed".
Do not invent information that is not in the resume.

Resume:
{resume_text}
"""

    return generate_text(prompt)
