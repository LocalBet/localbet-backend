"""
Schema for getting a bet.
"""

from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime


class BetGetSchema(BaseModel):
    id: UUID = Field(..., description="Bet ID")
    user_id: UUID = Field(..., description="User ID")
    coin_id: UUID = Field(..., description="Coin ID")
    amount: float = Field(..., description="Amount betted")
    status: str = Field(..., description="Bet status")
    name: str = Field(..., description="Bet name")
    create_date: datetime = Field(..., description="Creation date")
    update_date: datetime = Field(..., description="Update date")
