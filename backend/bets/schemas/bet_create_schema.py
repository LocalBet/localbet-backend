"""
Schema for creating a bet.
"""

from uuid import UUID
from pydantic import BaseModel, Field


class BetCreateSchema(BaseModel):
    name: str = Field(..., description="Bet name")
    coin_id: UUID = Field(..., description="Coin identifier")
    amount: float = Field(..., gt=0, description="Amount betted")
