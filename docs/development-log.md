# Development log

This log records the major engineering milestones visible in the repository
history. It focuses on decisions and lessons rather than listing every UI edit.

## 2026-07-15 — Functional prototype

The initial version established the complete interview-practice loop:

- Streamlit application and session state
- Gemini résumé summary, question generation, and answer evaluation
- PDF extraction
- Typed and recorded answer paths
- Communication metrics
- SQLite answer history
- Downloadable report generation

### Early design choice

Generative feedback and deterministic metrics were separated from the start.
This made filler counts, speaking rate, persistence, and report calculations
testable without calling an AI model.

## 2026-07-24 — Portfolio and deployment readiness

The prototype was prepared for reproducible local and hosted use:

- Environment-variable and Streamlit-secret configuration
- Docker and Streamlit Community Cloud support
- Python 3.12 runtime declaration
- GitHub Actions compilation and regression tests
- MIT license and citation metadata
- Session-scoped database history
- ffmpeg discovery for Whisper
- Initial project README and automated Streamlit smoke test

### Problem solved: local speech dependencies

Whisper expects an executable named `ffmpeg`. The application now discovers
the bundled `imageio-ffmpeg` binary and exposes it under the command name
Whisper expects, while deployment environments also install the system package.

### Problem solved: history privacy

An unscoped local history view could mix separate practice attempts. Database
reads now require the randomly generated session identifier, and a regression
test protects this behavior.

## 2026-08-03 — Résumé-aware MVP

The setup flow became substantially more useful:

- Added DOCX, TXT, PNG, and JPEG résumé support
- Added file-size, minimum-content, encoding, and format validation
- Added Gemini image transcription for résumé screenshots and scans
- Added target role and experience level
- Added optional pasted or uploaded job descriptions
- Grounded summary and question prompts in supplied vacancy requirements
- Required exactly five parsed questions
- Added clearer error messages and a sample candidate profile

### Problem solved: image résumés

Text extractors cannot read résumé screenshots. PNG and JPEG inputs are sent as
image parts to Gemini with explicit transcription instructions and the correct
MIME type. Scanned PDFs still need to be exported as an image before upload.

### Problem solved: unreliable generated structure

The application cannot safely assume every model response has the requested
shape. Question parsing rejects any response that does not contain exactly five
numbered questions. Answer evaluation parses JSON and rejects scores outside
the accepted range.

## 2026-08-04 to 2026-08-05 — Product experience and accessibility

The interface was reorganized into a focused application rather than a default
Streamlit form:

- Full-width responsive landing and workspace layouts
- Dedicated Practice, How it works, and About navigation
- Sample-profile state that replaces the upload control when selected
- Compact connected stage stepper
- Larger labels and simplified visual hierarchy
- Persistent accessibility mode
- Stronger keyboard focus visibility, contrast, and reduced motion
- Accessibility state preserved across page navigation

### Product lesson

Feature density did not make the interface feel more capable. The clearer
result came from prioritizing one primary action, moving explanatory content to
dedicated pages, and showing progress without giving the progress indicator
more visual weight than the interview itself.

## Current engineering priorities

1. Add deterministic fixtures for malformed Gemini feedback payloads.
2. Add end-to-end browser coverage for a complete sample-profile interview.
3. Measure generation and transcription latency.
4. Evaluate question relevance and feedback agreement with human reviewers.
5. Replace local SQLite with authenticated, user-owned persistence before any
   production multi-user use.
6. Add explicit data-retention and deletion controls.
