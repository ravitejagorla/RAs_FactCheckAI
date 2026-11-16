
from services.search_service import search_web

claim = "The Earth revolves around the Sun"

try:
    results = search_web(claim)

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Title:", result.get("title"))
        print("URL:", result.get("link"))
        print("Snippet:", result.get("snippet"))

except Exception as error:
    print("Error:", error)
