"""Regression tests for deterministic interview-coach behavior."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from utils.communication import analyze_communication
from utils import database
from utils.question_generator import parse_interview_questions
from utils.report import build_report
from utils.speech import _configure_ffmpeg


def _record(session_id, question_index, score):
    return {
        "session_id": session_id,
        "question_index": question_index,
        "question": f"Question {question_index}",
        "answer": "A concise answer",
        "answer_source": "Typed",
        "communication": {
            "communication_score": 8,
            "total_fillers": 1,
        },
        "feedback": {
            "score": score,
            "strengths": ["Specific"],
            "improvements": ["Add detail"],
            "better_structure": ["Context", "Action", "Result"],
        },
    }


class CommunicationTests(unittest.TestCase):
    def test_filler_words_and_speaking_rate_are_measured(self):
        result = analyze_communication(
            "Um, I actually built the project and tested it.",
            duration_seconds=6,
        )

        self.assertEqual(result["total_fillers"], 2)
        self.assertEqual(result["word_count"], 9)
        self.assertEqual(result["words_per_minute"], 90)


class QuestionParsingTests(unittest.TestCase):
    def test_numbered_questions_are_parsed(self):
        response = "\n".join(
            f"{index}. Question number {index}?"
            for index in range(1, 6)
        )

        questions = parse_interview_questions(response)

        self.assertEqual(len(questions), 5)
        self.assertEqual(questions[0], "Question number 1?")

    def test_wrong_question_count_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_interview_questions("1. Only one question?")


class ReportTests(unittest.TestCase):
    def test_report_aggregates_scores(self):
        report = build_report(
            {
                0: _record("session-a", 0, 9),
                1: _record("session-a", 1, 5),
            }
        )

        self.assertEqual(report["answers_evaluated"], 2)
        self.assertEqual(report["average_score"], 7.0)
        self.assertEqual(report["average_communication"], 8.0)
        self.assertEqual(report["total_fillers"], 2)


class DatabasePrivacyTests(unittest.TestCase):
    def test_history_is_scoped_to_one_session(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "interviews.db"
            with patch.object(database, "DATABASE_PATH", database_path):
                database.initialize_database()
                database.save_answer(_record("session-a", 0, 8))
                database.save_answer(_record("session-b", 0, 4))

                history = database.get_history("session-a")

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["session_id"], "session-a")
        self.assertEqual(history[0]["score"], 8)


class SpeechDependencyTests(unittest.TestCase):
    def test_ffmpeg_is_exposed_under_whispers_command_name(self):
        executable = _configure_ffmpeg()

        self.assertTrue(executable.exists())
        self.assertIsNotNone(shutil.which("ffmpeg"))


if __name__ == "__main__":
    unittest.main()
