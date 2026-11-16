
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "factcheck.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS fact_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                claim TEXT NOT NULL,
                verdict TEXT NOT NULL,
                confidence REAL NOT NULL,
                explanation TEXT NOT NULL,
                supporting_evidence TEXT,
                contradicting_evidence TEXT,
                limitations TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_check_id INTEGER NOT NULL,
                title TEXT,
                url TEXT,
                snippet TEXT,
                FOREIGN KEY (fact_check_id)
                    REFERENCES fact_checks(id)
                    ON DELETE CASCADE
            )
        """)
