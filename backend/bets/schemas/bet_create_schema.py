from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class BetCreateSchema(BaseModel):
    group_id: UUID
    title: str
    description: str
    image_url: str | None = None
    min_bet: int = 100
    deadline: datetime
