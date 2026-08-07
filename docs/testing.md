# Testing and evaluation

This document separates verified software behavior from claims that still need
human or dataset-based evaluation.

## Current automated result

Verified locally on **2026-08-05** using Python 3.12:

```text
16 tests passed
```

Run the same checks with:

```powershell
python -m compileall -q app.py utils tests
python -m unittest discover -s tests -v
python -m pip check
```

GitHub Actions runs compilation and the regression suite on Python 3.12 with
the system `ffmpeg` package installed.

## Automated coverage

| Area | What is verified |
| --- | --- |
| Communication analysis | Filler count, word count, and words per minute |
| Question parsing | A numbered five-question response is parsed successfully |
| Question validation | Responses with the wrong question count are rejected |
| Job-description grounding | Job-description text is included in question-generation context |
| Résumé summarization | Résumé and job-description comparison instructions reach the summary prompt |
| TXT extraction | UTF-8 text is normalized and repeated spacing is cleaned |
| DOCX extraction | Paragraph and table-cell content are both extracted |
| Content validation | Documents with too little text produce an actionable error |
| PNG extraction | Image bytes are routed to Gemini with the PNG MIME type |
| JPEG extraction | JPEG uploads use the correct MIME type |
| Missing credentials | Image extraction reports a specific Gemini-configuration error |
| Report aggregation | Answer scores, communication scores, and filler counts are aggregated |
| Database isolation | One session cannot read another session's saved history |
| Speech dependency | ffmpeg is exposed under the executable name Whisper requires |
| Streamlit smoke tests | Initial render plus a complete mocked sample-profile interview through five answers and the final report |

The Gemini calls in unit tests are mocked. This keeps the suite deterministic,
fast, and independent of API quota or model availability.

## Manual integration checklist

Run these checks before a release or public deployment:

- Upload one valid file of each supported format: PDF, DOCX, TXT, PNG, and JPG.
- Paste a job description and confirm that the briefing discusses matches,
  transferable evidence, and gaps without inventing experience.
- Generate questions for at least two different roles and confirm that exactly
  five distinct questions appear.
- Submit a typed answer and verify that feedback contains a 1–10 score,
  strengths, improvements, and a suggested structure.
- Record an answer, transcribe it, and confirm that duration-based speaking
  rate is displayed.
- Complete all five questions and download the Markdown report.
- Enable local score history, evaluate an answer, and confirm the history chart
  appears only for the current interview session.
- Enable accessibility mode and confirm larger controls, stronger contrast,
  reduced animation, and visible keyboard focus.
- Check the Practice, How it works, and About pages at desktop and mobile
  widths.

## What the tests do not prove

The current suite does **not** establish that:

- AI scores agree with expert interviewers.
- Generated questions are equally useful across industries or seniority levels.
- Feedback is free of bias.
- Whisper transcription has an acceptable word-error rate across accents,
  microphones, and background-noise conditions.
- Repeated use improves real interview outcomes.
- The Streamlit prototype is secure for multi-user production use.

These are evaluation questions, not ordinary unit-test claims.

## Recommended evaluation study

A stronger project evaluation would use:

1. A consented set of anonymized résumés, job descriptions, and sample answers.
2. Two independent human reviewers using a fixed scoring rubric.
3. Question-relevance ratings for role fit, résumé grounding, clarity, and
   difficulty.
4. Agreement measurements between AI scores and reviewer scores.
5. Whisper word-error rate measured on a small, diverse audio set.
6. Latency measurements for extraction, generation, transcription, and
   evaluation.
7. A documented failure analysis containing representative weak outputs and
   the mitigations attempted.

Do not publish private résumés, recordings, or identifiable evaluation data.
