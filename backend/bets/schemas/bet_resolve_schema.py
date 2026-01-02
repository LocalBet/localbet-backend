from pydantic import BaseModel, Field
from typing import List

class BetResolveSchema(BaseModel):
    winners: List[str] = Field(..., min_length=1, description="Usernames of winners (must be participants)")
