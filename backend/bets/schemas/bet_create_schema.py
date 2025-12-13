from pydantic import BaseModel, Field

class BetCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, description="Bet name")
    cost: float = Field(..., ge=0, description="Coins required to join this bet")
