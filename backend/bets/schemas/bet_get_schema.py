from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class BetGetSchema(BaseModel):
    id: UUID
    group_id: UUID
    title: str
    description: str
    image_url: str | None
    min_bet: int
    deadline: datetime
    status: str
    winning_option: UUID | None = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime
