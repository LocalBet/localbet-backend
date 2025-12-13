from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class BetGetSchema(BaseModel):
    id: UUID
    user_id: str = Field(..., description="Creator username")
    name: str
    cost: float
    status: str
    create_date: datetime
    update_date: datetime
    participants: List[str] = Field(default_factory=list)
