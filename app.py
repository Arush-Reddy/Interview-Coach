import hashlib
import uuid

import pandas as pd
import streamlit as st

from utils.communication import analyze_communication
from utils.database import get_history, initialize_database, save_answer
from utils.evaluator import evaluate_answer
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


defaults = {
    "resume_hash": None,
    "resume_summary": None,
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
    uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])
    st.toggle(
        "Save score history on this device",
        key="save_history",
        help=(
            "When disabled, answers remain in the current browser session and "
            "are not added to the local SQLite history."
        ),
    )

    analyze_clicked = False
    if uploaded_file is not None:
        file_hash = hashlib.sha256(uploaded_file.getvalue()).hexdigest()
        if file_hash != st.session_state.resume_hash:
            st.session_state.resume_hash = file_hash
            new_interview_session(keep_summary=False)

        st.caption(uploaded_file.name)
        analyze_clicked = st.button(
            "Analyze resume",
            type="primary",
            icon=":material/analytics:",
            width="stretch",
        )
    else:
        st.info("Upload a text-based PDF resume to begin.")

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


st.title("AI Interview Coach")
st.caption("Analyse your resume, practise interview answers, and track improvement.")

if analyze_clicked:
    with st.spinner("Gemini is analysing your resume..."):
        try:
            resume_text = extract_text(uploaded_file)
            if not resume_text.strip():
                raise ValueError("No readable text was found in the uploaded PDF.")

            st.session_state.resume_summary = summarize_resume(resume_text)
            new_interview_session()
            st.success("Your resume is ready for interview practice.")
        except Exception as error:
            st.error("We could not analyse this resume.")
            st.caption(f"Technical detail: {type(error).__name__}: {error}")

if not st.session_state.resume_summary:
    st.info("Upload a PDF in the sidebar, then select **Analyze resume**.")
    st.stop()

overview_tab, practice_tab, report_tab = st.tabs(
    [
        ":material/description: Resume overview",
        ":material/record_voice_over: Interview practice",
        ":material/monitoring: Report and progress",
    ]
)

with overview_tab:
    st.subheader("Resume Summary")
    st.markdown(st.session_state.resume_summary)

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
                        st.session_state.resume_summary
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
