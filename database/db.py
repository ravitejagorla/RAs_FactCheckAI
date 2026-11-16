import sqlite3
import json
from pathlib import Path
from contextlib import contextmanager

from schemas.factcheck_schema import FactCheckResult


DB_PATH = Path(__file__).resolve().parent / "factcheck.db"


@contextmanager
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


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


def save_fact_check(
    claim: str,
    result: FactCheckResult,
    search_results: list[dict]
) -> int:

    with get_connection() as connection:

        cursor = connection.execute("""
            INSERT INTO fact_checks (
                claim,
                verdict,
                confidence,
                explanation,
                supporting_evidence,
                contradicting_evidence,
                limitations
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            claim,
            result.verdict.value,
            result.confidence,
            result.explanation,
            json.dumps(result.supporting_evidence),
            json.dumps(result.contradicting_evidence),
            json.dumps(result.limitations)
        ))

        fact_check_id = cursor.lastrowid

        connection.executemany("""
            INSERT INTO sources (
                fact_check_id,
                title,
                url,
                snippet
            )
            VALUES (?, ?, ?, ?)
        """, [
            (
                fact_check_id,
                source.get("title"),
                source.get("link"),
                source.get("snippet")
            )
            for source in search_results
        ])

        return fact_check_id

def get_fact_checks(limit: int = 20) -> list[dict]:

    with get_connection() as connection:

        fact_checks = connection.execute("""
            SELECT *
            FROM fact_checks
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        history = []

        for fact_check in fact_checks:

            sources = connection.execute("""
                SELECT title, url, snippet
                FROM sources
                WHERE fact_check_id = ?
            """, (fact_check["id"],)).fetchall()

            record = dict(fact_check)

            record["supporting_evidence"] = json.loads(
                record["supporting_evidence"] or "[]"
            )

            record["contradicting_evidence"] = json.loads(
                record["contradicting_evidence"] or "[]"
            )

            record["limitations"] = json.loads(
                record["limitations"] or "[]"
            )

            record["sources"] = [dict(source) for source in sources]

            history.append(record)

        return history