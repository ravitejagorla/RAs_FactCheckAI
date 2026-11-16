from langchain_groq import ChatGroq

from config import GROQ_API_KEY, GROQ_MODEL
from schemas.claim_schema import ClaimList


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0
)

structured_llm = llm.with_structured_output(
    ClaimList,
    method="json_mode"
)


def split_claims(text: str) -> list[str]:

    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    prompt = f"""
        You are an expert claim extraction assistant.

        Extract individual factual claims from the following input.

        RULES:
        - Split multiple independent factual statements into separate claims.
        - Preserve the original meaning.
        - Do not add new facts or assumptions.
        - Do not turn questions or opinions into factual claims.
        - Do not unnecessarily split a single factual statement.
        - Remove duplicate claims.
        - If the input contains only one factual claim, return one claim.
        - Return valid JSON with exactly one field named "claims".
        - Every item in claims must be a string.

        INPUT:
        {text}
    """

    result = structured_llm.invoke(prompt)

    return [
        claim.strip()
        for claim in result.claims
        if claim.strip()
    ]