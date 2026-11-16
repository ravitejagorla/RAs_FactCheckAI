
from pydantic import BaseModel, Field, ConfigDict

class ClaimList(BaseModel):
    model_config = ConfigDict(extra="forbid")
    claims: list[str] = Field( default_factory = list, description = "Individual factual claims extracted from the input. Return an empty list if there are no factual claims.")
