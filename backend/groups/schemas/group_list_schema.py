from typing import List
from pydantic import BaseModel

from backend.groups.schemas.group_get_schema import GroupGetSchema


class GroupListSchema(BaseModel):
    groups: List[GroupGetSchema]

    class Config:
        schema_extra = {
            "example": {
                "groups": [
                    {
                        "id": "b77414fc-33e7-4d3d-94ea-d7c9d7d25660",
                        "name": "Football Lovers",
                        "create_date": "2025-12-11T10:00:00Z",
                        "update_date": "2025-12-11T10:30:00Z",
                        "members": ["marta", "genis"],
                        "admin_username": "marta",
                        "bets": [],
                    }
                ]
            }
        }
