from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class GroupGetSchema(BaseModel):
    id: UUID
    name: str
    description: str
    creator_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
