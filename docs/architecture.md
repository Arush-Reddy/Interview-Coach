# System architecture

AI Interview Coach combines generative-AI tasks with deterministic Python
analysis. The language model is used where interpretation is useful; parsing,
validation, communication metrics, persistence, and report aggregation remain
explicit application code.

## End-to-end flow

```mermaid
flowchart TD
    U[Candidate] --> UI[Streamlit interface]

    subgraph Setup
        UI --> R{Résumé source}
        R -->|PDF| PDF[pypdf extraction]
        R -->|DOCX| DOCX[python-docx extraction]
        R -->|TXT| TXT[UTF-8 decoding]
        R -->|PNG or JPEG| IMG[Gemini image transcription]
        PDF --> CLEAN[Text cleanup and validation]
        DOCX --> CLEAN
        TXT --> CLEAN
        IMG --> CLEAN
        JD[Optional job description] --> CLEAN
    end

    CLEAN --> SUMMARY[Gemini candidate and role briefing]
    SUMMARY --> QUESTIONS[Gemini question generation]
    QUESTIONS --> VALIDATE[Exactly-five question validator]
    VALIDATE --> SESSION[Streamlit interview session]

    subgraph Practice
        SESSION --> MODE{Answer mode}
        MODE -->|Text| ANSWER[Candidate answer]
        MODE -->|Voice| WHISPER[Local Whisper transcription]
        WHISPER --> ANSWER
        ANSWER --> GEMINI[Gemini structured feedback]
        ANSWER --> METRICS[Local communication analysis]
        GEMINI --> FEEDBACK[Score, strengths, improvements, structure]
        METRICS --> FEEDBACK
    end

    FEEDBACK --> REPORT[Deterministic report aggregation]
    FEEDBACK -->|Opt-in only| SQLITE[(Local SQLite history)]
    REPORT --> DOWNLOAD[Markdown report download]
```

## Component responsibilities

| Component | Responsibility |
| --- | --- |
| `app.py` | Page composition, session state, interview navigation, and user actions |
| `utils/pdf_reader.py` | File limits, format routing, extraction, cleanup, and actionable errors |
| `utils/gemini_client.py` | Credential lookup, Gemini client calls, and backup-model retry |
| `utils/summarizer.py` | Résumé-to-role briefing and job-description comparison prompt |
| `utils/question_generator.py` | Five-question prompt and strict numbered-list parsing |
| `utils/evaluator.py` | Structured answer-feedback prompt and score validation |
| `utils/speech.py` | ffmpeg discovery, temporary audio handling, and local Whisper transcription |
| `utils/communication.py` | Word count, filler-word count, speaking rate, and communication score |
| `utils/report.py` | Session-level score and feedback aggregation |
| `utils/database.py` | Parameterized, session-scoped optional SQLite history |
| `utils/styles.py` | Shared responsive theme, navigation, progress stepper, and accessibility mode |

## Data lifecycle

```mermaid
sequenceDiagram
    actor Candidate
    participant Browser as Streamlit session
    participant Gemini
    participant Whisper as Local Whisper
    participant DB as Local SQLite

    Candidate->>Browser: Upload résumé and choose a role
    Browser->>Browser: Extract and validate text in memory
    Browser->>Gemini: Send extracted text and role context
    Gemini-->>Browser: Return briefing and questions
    Candidate->>Browser: Type or record an answer
    opt Recorded answer
        Browser->>Whisper: Transcribe a temporary audio file
        Whisper-->>Browser: Return transcript and duration
    end
    Browser->>Gemini: Send question and candidate answer
    Gemini-->>Browser: Return structured feedback
    Browser->>Browser: Calculate transparent communication metrics
    opt Score history enabled
        Browser->>DB: Save session-scoped evaluation
    end
    Browser-->>Candidate: Display feedback and downloadable report
```

Uploaded résumés and job descriptions are processed in memory. Recorded audio
is written only to a temporary file for transcription and is removed when the
temporary context closes. Evaluation history is written to SQLite only when the
user enables local score history.

## Trust boundaries

- **Gemini boundary:** résumé/job-description text and typed or transcribed
  answers are sent to the configured Gemini API for generation and evaluation.
- **Local model boundary:** recorded audio is transcribed by Whisper on the
  application host.
- **Persistence boundary:** SQLite persistence is local, optional, and keyed by
  a randomly generated interview-session identifier.
- **Public deployment boundary:** the prototype has no user accounts,
  encrypted personal storage, retention controls, or deletion workflow. It
  should not be treated as a production hiring platform.

## Design decisions

1. **Keep measurable signals deterministic.** Filler words, word counts,
   speaking rate, and report averages can be inspected and tested.
2. **Validate model output before using it.** Question generation must yield
   exactly five questions, and answer feedback must contain a valid 1–10 score.
3. **Make persistence opt-in.** Practice works without writing answer history
   to the database.
4. **Separate modules by responsibility.** AI access, document extraction,
   speech, analysis, persistence, and presentation can evolve independently.
