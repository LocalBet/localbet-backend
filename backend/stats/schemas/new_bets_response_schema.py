from pydantic import BaseModel
from typing import List

class NewBetsResponseSchema(BaseModel):
    new_bets: List[str]
    count: int
