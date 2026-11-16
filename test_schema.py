
from schemas.factcheck_schema import FactCheckResult

result = FactCheckResult(
    verdict="True",
    confidence=0.98,
    explanation="Earth revolves around the Sun.",
    supporting_evidence=[
        "NASA confirms Earth's orbit around the Sun."
    ],
    contradicting_evidence=[],
    limitations=[
        "Analysis is based on search-result snippets."
    ]
)

print(result)
print("\nJSON output:")
print(result.model_dump_json(indent=4))
