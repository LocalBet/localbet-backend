from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

from backend.bets.schemas.bet_get_schema import BetGetSchema


class GroupGetSchema(BaseModel):
    id: UUID = Field(..., description="Group ID")
    name: str = Field(..., description="Group name")
    create_date: datetime = Field(..., description="Date when the group was created")
    update_date: datetime = Field(..., description="Date when the group was last updated")

    # ✅ ara usernames
    members: List[str] = Field(..., description="List of usernames who are members of the group")

    # ✅ ara username (no UUID)
    admin_username: str = Field(..., description="The username of the group admin")

    # ✅ nou
    bets: List[BetGetSchema] = Field(default_factory=list, description="List of bets in the group")

    class Config:
        schema_extra = {
            "example": {
                "id": "b77414fc-33e7-4d3d-94ea-d7c9d7d25660",
                "name": "Football Lovers",
                "create_date": "2025-12-11T10:00:00Z",
                "update_date": "2025-12-11T10:30:00Z",
                "members": ["genis2", "marta"],
                "admin_username": "genis2",
                "bets": [],
            }
        }
