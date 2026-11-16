from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class Verdict(str, Enum):
    TRUE = "True"
    FALSE = "False"
    PARTIALLY_TRUE = "Partially True"
    MISLEADING = "Misleading"
    INSUFFICIENT_EVIDENCE = "Insufficient Evidence"

class FactCheckResult(BaseModel):
    model_config = ConfigDict(extra = "forbid")
    verdict: Verdict = Field(description = "Overall fact-check verdict")
    confidence: float = Field(ge = 0, le = 1, description = "Estimated confidence between 0 and 1")
    explanation: str = Field(description = "Explanation of the verdict")
    supporting_evidence: list[str] = Field(description = "Evidence supporting the claim")
    contradicting_evidence: list[str] = Field(description = "Evidence contradicting the claim")
    limitations: list[str] = Field(description = "Limitations and missing information")