
from services.search_service import search_web
from services.factcheck_service import factcheck_claim

claim = "The Earth revolves around the Sun."

try:
    print("Searching for evidence...")
    results = search_web(claim)

    print("Analyzing evidence...")
    result = factcheck_claim(claim, results)

    print("\nVerdict:", result.verdict.value)
    print("Confidence:", result.confidence)
    print("Explanation:", result.explanation)

    print("\nSupporting Evidence:")
    for item in result.supporting_evidence:
        print("-", item)

    print("\nContradicting Evidence:")
    for item in result.contradicting_evidence:
        print("-", item)

    print("\nLimitations:")
    for item in result.limitations:
        print("-", item)

    print("\nJSON:")
    print(result.model_dump_json(indent=4))

except Exception as error:
    print("Fact-checking failed:", error)
