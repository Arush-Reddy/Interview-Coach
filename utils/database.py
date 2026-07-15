import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "interviews.db"


def _connect():
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS interview_answers (
                session_id TEXT NOT NULL,
                question_index INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                answer_source TEXT NOT NULL,
                score INTEGER NOT NULL,
                communication_score INTEGER NOT NULL,
                filler_count INTEGER NOT NULL,
                PRIMARY KEY (session_id, question_index)
            )
            """
        )


def save_answer(record):
    with _connect() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO interview_answers (
                session_id, question_index, question, answer, answer_source,
                score, communication_score, filler_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["session_id"],
                record["question_index"],
                record["question"],
                record["answer"],
                record["answer_source"],
                record["feedback"]["score"],
                record["communication"]["communication_score"],
                record["communication"]["total_fillers"],
            ),
        )


def get_history():
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT created_at, session_id, question_index, score,
                   communication_score, filler_count
            FROM interview_answers
            ORDER BY created_at
            """
        ).fetchall()

    return [dict(row) for row in rows]
