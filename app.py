import hashlib
import uuid

import pandas as pd
import streamlit as st

from utils.communication import analyze_communication
from utils.database import get_history, initialize_database, save_answer
from utils.evaluator import evaluate_answer
from utils.gemini_client import has_api_key
from utils.pdf_reader import extract_text
from utils.question_generator import generate_interview_questions
from utils.report import build_report, report_as_markdown
from utils.speech import transcribe_audio
from utils.summarizer import summarize_resume


st.set_page_config(
    page_title="AI Interview Coach",
    page_icon=":material/record_voice_over:",
    layout="wide",
)
initialize_database()

SAMPLE_RESUME = """
Jordan Lee
Computer Science Student

Skills: Python, SQL, Git, data visualization, REST APIs, teamwork

Experience:
- Coordinated a four-person capstone team and delivered weekly progress updates.
- Built a Python dashboard that reduced manual reporting time for a student club.
- Presented project findings to faculty and incorporated stakeholder feedback.

Projects:
- Interview preparation assistant using Streamlit and a generative AI API.
- Campus event analytics dashboard using Python, pandas, and SQL.

Education:
BSc Computer Science, expected 2027
""".strip()

SAMPLE_JOB_DESCRIPTION = """
Junior Project Coordinator

Support project planning, track milestones, maintain documentation, and communicate
updates to stakeholders. The ideal candidate is organized, comfortable working with
cross-functional teams, and familiar with Agile practices, risk tracking, Jira, and
data-driven reporting. Strong written and verbal communication is required.
""".strip()

st.markdown(
    """
    <style>
    .block-container {
        width: 100%; max-width: 1120px; box-sizing: border-box;
        padding-top: 2.2rem; padding-bottom: 4rem;
    }
    [data-testid="stSidebar"] { border-right: 1px solid #2d3854; }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(124,131,253,.12), rgba(21,28,47,.7));
        border: 1px solid #2d3854;
        border-radius: 18px;
        padding: 1rem;
    }
    [data-testid="stAlert"] { border-radius: 16px; }
    .coach-kicker {
        color: #9da5ff; font-size: .78rem; font-weight: 700;
        letter-spacing: .12em; text-transform: uppercase; margin-bottom: .3rem;
    }
    .workflow {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: .65rem;
        margin: 1.2rem 0 1.8rem;
    }
    .workflow-step {
        border: 1px solid #2d3854; border-radius: 14px; padding: .75rem .9rem;
        color: #aeb6cc; background: rgba(21,28,47,.58); font-size: .88rem;
    }
    .workflow-step strong { color: #f3f4f6; margin-right: .35rem; }
    .workflow-step.active { border-color: #7c83fd; background: rgba(124,131,253,.14); }
    .workflow-step.done { border-color: #48c78e; background: rgba(72,199,142,.09); }
    @media (max-width: 700px) { .workflow { grid-template-columns: 1fr; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def new_interview_session(keep_summary=True):
    """Clear one interview's answers while optionally keeping the resume summary."""
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.interview_questions = []
    st.session_state.question_index = 0
    st.session_state.evaluations = {}
    st.session_state.audio_durations = {}
    st.session_state.answer_sources = {}
    if not keep_summary:
        st.session_state.resume_summary = None
        st.session_state.resume_text = None
        st.session_state.job_description_text = None


def load_sample_profile():
    """Populate a judge-friendly candidate and vacancy without making API calls."""
    st.session_state.demo_resume_text = SAMPLE_RESUME
    st.session_state.target_role = "Junior Project Coordinator"
    st.session_state.experience_level = "Entry level"
    st.session_state.job_description_input = SAMPLE_JOB_DESCRIPTION
    st.session_state.resume_hash = None
    new_interview_session(keep_summary=False)


defaults = {
    "resume_hash": None,
    "resume_summary": None,
    "resume_text": None,
    "job_description_text": None,
    "job_description_input": "",
    "demo_resume_text": None,
    "target_role": "",
    "experience_level": "Student / Intern",
    "interview_questions": [],
    "question_index": 0,
    "evaluations": {},
    "audio_durations": {},
    "answer_sources": {},
    "session_id": str(uuid.uuid4()),
    "save_history": False,
}
for state_key, default_value in defaults.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value


with st.sidebar:
    st.header("Interview setup")
    st.caption("1 · Candidate")
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        help=(
            "Use a PDF, Word document, UTF-8 text file, or clear resume image "
            "(maximum 8 MB). Images are transcribed with Gemini."
        ),
    )
    if st.button(
        "Try a sample candidate",
        icon=":material/auto_awesome:",
        width="stretch",
        on_click=load_sample_profile,
    ):
        pass
    if st.session_state.demo_resume_text and uploaded_file is None:
        st.success("Sample candidate loaded")

    st.caption("2 · Interview target")
    st.text_input(
        "Target role",
        key="target_role",
        placeholder="e.g. Junior Data Analyst",
    )
    st.selectbox(
        "Experience level",
        ("Student / Intern", "Entry level", "Mid level", "Senior"),
        key="experience_level",
    )
    st.caption("3 · Vacancy context")
    with st.expander("Job description (recommended)"):
        st.text_area(
            "Paste the job listing",
            key="job_description_input",
            placeholder=(
                "Paste responsibilities, required skills, and qualifications…"
            ),
            height=150,
        )
        job_description_file = st.file_uploader(
            "Or upload the job listing",
            type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
            key="job_description_file",
            help="Optional. Pasted text takes priority if both are provided.",
        )
    st.toggle(
        "Save score history on this device",
        key="save_history",
        help=(
            "When disabled, answers remain in the current browser session and "
            "are not added to the local SQLite history."
        ),
    )

    analyze_clicked = False
    resume_available = (
        uploaded_file is not None
        or bool(st.session_state.demo_resume_text)
    )
    if resume_available:
        resume_bytes = (
            uploaded_file.getvalue()
            if uploaded_file is not None
            else st.session_state.demo_resume_text.encode("utf-8")
        )
        setup_fingerprint = (
            resume_bytes
            + st.session_state.target_role.strip().lower().encode("utf-8")
            + st.session_state.experience_level.encode("utf-8")
            + st.session_state.job_description_input.strip().encode("utf-8")
            + (
                job_description_file.getvalue()
                if job_description_file is not None
                else b""
            )
        )
        setup_hash = hashlib.sha256(setup_fingerprint).hexdigest()
        if setup_hash != st.session_state.resume_hash:
            st.session_state.resume_hash = setup_hash
            new_interview_session(keep_summary=False)

        if uploaded_file is not None:
            st.caption(uploaded_file.name)
        analyze_clicked = st.button(
            "Build my interview plan",
            type="primary",
            icon=":material/analytics:",
            width="stretch",
            disabled=(
                not st.session_state.target_role.strip()
                or not has_api_key()
            ),
        )
        if not st.session_state.target_role.strip():
            st.caption("Enter a target role to continue.")
        elif not has_api_key():
            st.caption("Gemini is not configured on this server.")
    else:
        st.info("Upload a resume or try the sample candidate to begin.")

    if st.session_state.resume_summary:
        st.divider()
        st.success("Resume analysed")
        st.caption(
            f"Answers evaluated: {len(st.session_state.evaluations)}/"
            f"{len(st.session_state.interview_questions) or 5}"
        )
        if st.button(
            "Start a new interview",
            icon=":material/refresh:",
            width="stretch",
        ):
            new_interview_session()
            st.rerun()


st.markdown('<div class="coach-kicker">Personalized practice studio</div>', unsafe_allow_html=True)
st.title("AI Interview Coach")
st.caption(
    "Upload your resume, choose a target role, practise tailored questions, "
    "and track improvement."
)

plan_ready = bool(st.session_state.resume_summary)
questions_ready = bool(st.session_state.interview_questions)
report_ready = bool(
    questions_ready
    and len(st.session_state.evaluations)
    == len(st.session_state.interview_questions)
)
step_classes = [
    "done" if plan_ready else "active",
    "done" if questions_ready else ("active" if plan_ready else ""),
    "done" if report_ready else ("active" if questions_ready else ""),
]
st.markdown(
    f"""
    <div class="workflow">
      <div class="workflow-step {step_classes[0]}"><strong>01</strong> Build your plan</div>
      <div class="workflow-step {step_classes[1]}"><strong>02</strong> Practice answers</div>
      <div class="workflow-step {step_classes[2]}"><strong>03</strong> Review progress</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if analyze_clicked:
    with st.spinner("Gemini is analysing your resume..."):
        try:
            resume_text = (
                extract_text(uploaded_file)
                if uploaded_file is not None
                else st.session_state.demo_resume_text
            )
            job_description_text = st.session_state.job_description_input.strip()
            if not job_description_text and job_description_file is not None:
                job_description_text = extract_text(
                    job_description_file,
                    document_kind="job description",
                )
            st.session_state.resume_text = resume_text
            st.session_state.job_description_text = job_description_text or None
            st.session_state.resume_summary = summarize_resume(
                resume_text,
                st.session_state.target_role,
                job_description_text,
            )
            new_interview_session()
            st.success("Your resume is ready for interview practice.")
        except Exception as error:
            st.error("We could not analyse this resume.")
            st.caption(f"Technical detail: {type(error).__name__}: {error}")

if not st.session_state.resume_summary:
    feature_columns = st.columns(3)
    with feature_columns[0]:
        with st.container(border=True):
            st.markdown("#### Resume-aware")
            st.caption("Ground every question in your real skills, projects, and experience.")
    with feature_columns[1]:
        with st.container(border=True):
            st.markdown("#### Vacancy-matched")
            st.caption("Prepare against the responsibilities and skills employers actually list.")
    with feature_columns[2]:
        with st.container(border=True):
            st.markdown("#### Voice or text")
            st.caption("Practise naturally, then receive structured feedback and clear next steps.")
    st.info(
        "Start in the sidebar: upload your resume or load the sample profile, "
        "choose a role, then select **Build my interview plan**."
    )
    st.stop()

overview_tab, practice_tab, report_tab = st.tabs(
    [
        ":material/description: Resume overview",
        ":material/record_voice_over: Interview practice",
        ":material/monitoring: Report and progress",
    ]
)

with overview_tab:
    st.subheader("Candidate and Role Briefing")
    st.caption(
        f"Interview target: {st.session_state.target_role} · "
        f"{st.session_state.experience_level}"
    )
    st.markdown(st.session_state.resume_summary)
    if st.session_state.job_description_text:
        with st.expander("Job description used for this interview"):
            st.text_area(
                "Job description",
                st.session_state.job_description_text,
                height=260,
                disabled=True,
            )
    with st.expander("Check extracted resume text"):
        st.text_area(
            "Extracted text",
            st.session_state.resume_text,
            height=320,
            disabled=True,
        )

with practice_tab:
    st.subheader("Practice Interview")
    st.caption(
        "Choose typed or recorded answers. Local score history is optional "
        "and controlled from the sidebar."
    )

    if not st.session_state.interview_questions:
        if st.button(
            "Generate 5 interview questions",
            type="primary",
            icon=":material/auto_awesome:",
        ):
            with st.spinner("Gemini is creating your questions..."):
                try:
                    st.session_state.interview_questions = generate_interview_questions(
                        st.session_state.resume_summary,
                        st.session_state.target_role,
                        st.session_state.experience_level,
                        st.session_state.job_description_text or "",
                    )
                    st.session_state.question_index = 0
                    st.session_state.evaluations = {}
                    st.session_state.audio_durations = {}
                    st.session_state.answer_sources = {}
                    st.session_state.session_id = str(uuid.uuid4())
                    st.rerun()
                except Exception as error:
                    st.error("Gemini could not generate questions. Please try again.")
                    st.caption(f"Technical detail: {type(error).__name__}: {error}")

    if st.session_state.interview_questions:
        questions = st.session_state.interview_questions
        question_index = st.session_state.question_index
        question = questions[question_index]
        answer_key = f"answer_{st.session_state.session_id}_{question_index}"
        mode_key = f"mode_{st.session_state.session_id}_{question_index}"

        st.progress((question_index + 1) / len(questions))
        st.caption(f"Question {question_index + 1} of {len(questions)}")
        st.info(question)

        answer_mode = st.segmented_control(
            "How would you like to answer?",
            ("Type your answer", "Record your answer"),
            default="Type your answer",
            required=True,
            width="stretch",
            key=mode_key,
        )

        if answer_mode == "Record your answer":
            recorded_audio = st.audio_input("Record your answer")
            if recorded_audio:
                st.audio(recorded_audio)
                if st.button(
                    "Transcribe recording",
                    icon=":material/transcribe:",
                    width="stretch",
                ):
                    with st.spinner("Whisper is transcribing your recording..."):
                        try:
                            transcript, duration = transcribe_audio(recorded_audio)
                            st.session_state[answer_key] = transcript
                            st.session_state.audio_durations[question_index] = duration
                            st.session_state.answer_sources[question_index] = "Recorded"
                            st.rerun()
                        except Exception as error:
                            st.error("We could not transcribe this recording.")
                            st.caption(
                                "Whisper downloads its speech model the first time it is used. "
                                f"Technical detail: {type(error).__name__}: {error}"
                            )

        answer = st.text_area(
            "Your answer",
            placeholder="Type your answer, or transcribe a recording above...",
            height=180,
            key=answer_key,
        )

        if st.button(
            "Get AI feedback",
            type="primary",
            icon=":material/psychology:",
            width="stretch",
        ):
            if not answer.strip():
                st.warning("Write or transcribe an answer before requesting feedback.")
            else:
                with st.spinner("Gemini is reviewing your answer..."):
                    try:
                        communication = analyze_communication(
                            answer,
                            st.session_state.audio_durations.get(question_index),
                        )
                        feedback = evaluate_answer(question, answer)
                        record = {
                            "session_id": st.session_state.session_id,
                            "question_index": question_index,
                            "question": question,
                            "answer": answer,
                            "answer_source": st.session_state.answer_sources.get(question_index, "Typed"),
                            "communication": communication,
                            "feedback": feedback,
                        }
                        st.session_state.evaluations[question_index] = record
                        if st.session_state.save_history:
                            save_answer(record)
                        st.rerun()
                    except Exception as error:
                        st.error("Gemini could not evaluate the answer. Please try again.")
                        st.caption(f"Technical detail: {type(error).__name__}: {error}")

        evaluation = st.session_state.evaluations.get(question_index)
        if evaluation:
            feedback = evaluation["feedback"]
            communication = evaluation["communication"]

            score_column, communication_column, fillers_column = st.columns(3)
            score_column.metric("Answer score", f"{feedback['score']}/10")
            communication_column.metric(
                "Communication", f"{communication['communication_score']}/10"
            )
            fillers_column.metric("Filler words", communication["total_fillers"])

            with st.expander("AI Feedback", expanded=True):
                st.markdown("#### What went well")
                st.markdown("\n".join(f"- {item}" for item in feedback["strengths"]))
                st.markdown("#### Improve next time")
                st.markdown("\n".join(f"- {item}" for item in feedback["improvements"]))
                st.markdown("#### Better answer structure")
                st.markdown("\n".join(f"- {item}" for item in feedback["better_structure"]))

            with st.expander("Communication details"):
                st.write(f"Words used: {communication['word_count']}")
                if communication["words_per_minute"]:
                    st.write(f"Speaking speed: {communication['words_per_minute']} words per minute")
                if communication["filler_counts"]:
                    st.write("Filler words found:")
                    st.json(communication["filler_counts"])
                else:
                    st.success("No common filler words were detected.")

        previous_column, next_column, fresh_questions_column = st.columns(3)
        with previous_column:
            if st.button(
                "Previous",
                icon=":material/arrow_back:",
                disabled=question_index == 0,
                width="stretch",
            ):
                st.session_state.question_index -= 1
                st.rerun()
        with next_column:
            if st.button(
                "Next",
                icon=":material/arrow_forward:",
                disabled=question_index == len(questions) - 1,
                width="stretch",
            ):
                st.session_state.question_index += 1
                st.rerun()
        with fresh_questions_column:
            if st.button(
                "New questions",
                icon=":material/refresh:",
                width="stretch",
            ):
                new_interview_session()
                st.rerun()

with report_tab:
    st.subheader("Interview Report")
    evaluations = st.session_state.evaluations

    if st.session_state.interview_questions and len(evaluations) == len(
        st.session_state.interview_questions
    ):
        report = build_report(evaluations)
        score_column, communication_column, fillers_column = st.columns(3)
        score_column.metric("Average answer score", f"{report['average_score']}/10")
        communication_column.metric(
            "Average communication", f"{report['average_communication']}/10"
        )
        fillers_column.metric("Total filler words", report["total_fillers"])

        st.markdown("#### Best answer")
        st.write(report["best_question"])
        st.markdown("#### Main improvement area")
        st.write(report["improvement_question"])
        st.markdown("#### Recommendations")
        st.markdown("\n".join(f"- {item}" for item in report["recommendations"]))
        st.download_button(
            "Download report",
            data=report_as_markdown(report),
            file_name="interview_report.md",
            mime="text/markdown",
            icon=":material/download:",
        )
    else:
        total_questions = len(st.session_state.interview_questions) or 5
        st.info(
            f"Evaluate all {total_questions} questions to unlock your final interview report. "
            f"Completed: {len(evaluations)}/{total_questions}."
        )

    st.divider()
    st.subheader("Current session history")
    history = (
        get_history(st.session_state.session_id)
        if st.session_state.save_history
        else []
    )

    if history:
        history_frame = pd.DataFrame(history)
        st.line_chart(history_frame[["score", "communication_score"]])
        st.dataframe(
            history_frame[["created_at", "score", "communication_score", "filler_count"]],
            hide_index=True,
            width="stretch",
        )
    else:
        if st.session_state.save_history:
            st.caption(
                "Your saved answer scores will appear here after your first evaluation."
            )
        else:
            st.caption(
                "Enable local score history in the sidebar to persist this "
                "session's score trend."
            )
