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
                        "members": [
                            "d71a63eb-3d8d-4259-a026-49bb2c3d9fa3",
                            "a76b63cb-3d8d-4259-a026-49bb2c3d9fa3"
                        ],
                        "admin_id": "d71a63eb-3d8d-4259-a026-49bb2c3d9fa3",
                    },
                    {
                        "id": "b87414fc-33e7-4d3d-94ea-d7c9d7d25661",
                        "name": "Basketball Enthusiasts",
                        "create_date": "2025-12-12T09:00:00Z",
                        "update_date": "2025-12-12T09:30:00Z",
                        "members": [
                            "d81a63eb-3d8d-4259-a026-49bb2c3d9fa4",
                            "a76b63cb-3d8d-4259-a026-49bb2c3d9fa5"
                        ],
                        "admin_id": "d81a63eb-3d8d-4259-a026-49bb2c3d9fa4",
                    },
                ]
            }
        }
