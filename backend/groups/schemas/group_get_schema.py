from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class GroupGetSchema(BaseModel):
    id: UUID = Field(..., description="Group ID")
    name: str = Field(..., description="Group name")
    create_date: datetime = Field(..., description="Date when the group was created")
    update_date: datetime = Field(..., description="Date when the group was last updated")
    members: List[UUID] = Field(..., description="List of user IDs who are members of the group")
    admin_id: UUID = Field(..., description="The user ID of the group admin")

    class Config:
        schema_extra = {
            "example": {
                "id": "b77414fc-33e7-4d3d-94ea-d7c9d7d25660",
                "name": "Football Lovers",
                "create_date": "2025-12-11T10:00:00Z",
                "update_date": "2025-12-11T10:30:00Z",
                "members": [
                    "d71a63eb-3d8d-4259-a026-49bb2c3d9fa3",
                    "a76b63cb-3d8d-4259-a026-49bb2c3d9fa3"
                ],
                "admin_id": "d71a63eb-3d8d-4259-a026-49bb2c3d9fa3",
            }
        }
