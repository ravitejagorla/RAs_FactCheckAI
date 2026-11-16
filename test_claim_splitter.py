from services.claim_service import split_claims


test_cases = [
    "India became independent in 1947.",
    "India became independent in 1947. The Earth revolves around the Sun.",
    "Is Hyderabad the capital of Telangana?",
    "India became independent in 1947. India became independent in 1947.",
    "I like Hyderabad."
]


for index, text in enumerate(test_cases, start=1):

    print(f"\nTest {index}")
    print("Input:", text)

    try:
        claims = split_claims(text)

        for claim in claims:
            print("-", claim)

    except Exception as error:
        print("Error:", error)