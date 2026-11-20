
import sqlite3
from pathlib import Path
from datetime import datetime

# Database path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "speechflow.db"


def get_connection():
    return sqlite3.connect(str(DB_PATH))


def init_db():
    """Initialize the database."""

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                transcription TEXT,
                language TEXT,
                duration REAL,
                created_at TEXT
            )
        """)

        conn.commit()

    return True


def save_session(
    filename,
    transcription,
    language="Unknown",
    duration=0.0
):
    """Save an audio transcription session."""

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sessions (
                filename,
                transcription,
                language,
                duration,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            filename,
            transcription,
            language,
            duration,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        return cursor.lastrowid


def list_sessions(limit=10):
    """Get recent analysis sessions."""

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                filename,
                transcription,
                language,
                duration,
                created_at
            FROM sessions
            ORDER BY id DESC
            LIMIT ?
        """, (max(1, int(limit)),))

        return cursor.fetchall()
