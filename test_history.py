from database.db import get_fact_checks

history = get_fact_checks()

print(f"Total records retrieved: {len(history)}")

for item in history:

    print("\n" + "=" * 50)

    print("ID:", item["id"])
    print("Claim:", item["claim"])
    print("Verdict:", item["verdict"])
    print("Confidence:", item["confidence"])
    print("Explanation:", item["explanation"])

    print("Supporting Evidence:", item["supporting_evidence"])
    print("Sources:", len(item["sources"]))