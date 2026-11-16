from database.db import init_db, save_fact_check, get_connection
from schemas.factcheck_schema import FactCheckResult, Verdict


# Create tables if they don't exist
init_db()

# Sample AI result — no API calls needed
sample_result = FactCheckResult(
    verdict=Verdict.TRUE,
    confidence=0.98,
    explanation="The Earth revolves around the Sun.",
    supporting_evidence=[
        "NASA confirms Earth's orbital motion."
    ],
    contradicting_evidence=[],
    limitations=[
        "Test data used for database verification."
    ]
)

# Sample search results
sample_sources = [
    {
        "title": "NASA",
        "link": "https://www.nasa.gov/",
        "snippet": "Information about Earth and the Solar System."
    },
    {
        "title": "Britannica",
        "link": "https://www.britannica.com/",
        "snippet": "Information about Earth's orbit."
    }
]

# Save the fact-check
fact_check_id = save_fact_check(
    "The Earth revolves around the Sun.",
    sample_result,
    sample_sources
)

print(f"Saved fact-check ID: {fact_check_id}")

# Verify saved data
with get_connection() as connection:
    fact_check = connection.execute(
        "SELECT * FROM fact_checks WHERE id = ?",
        (fact_check_id,)
    ).fetchone()

    sources = connection.execute(
        "SELECT * FROM sources WHERE fact_check_id = ?",
        (fact_check_id,)
    ).fetchall()

print("Claim:", fact_check["claim"])
print("Verdict:", fact_check["verdict"])
print("Confidence:", fact_check["confidence"])
print("Number of sources:", len(sources))
print("Database save test successful!")