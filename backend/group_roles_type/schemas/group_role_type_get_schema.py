"""
Schemas for getting Group role type
"""

from uuid import UUID
from pydantic import BaseModel, Field

class GroupRoleTypeGetSchema(BaseModel):
    """
    Schema for getting an Group Role type
    """

    id: str = Field(
        default=...,
        description="Group Role type id.",
        examples=["d71a63eb-3d8d-4259-a026-49bb2c3d9fa3"],
    )

    name: str = Field(
        default=...,
        description="Group role type name",
        examples=["Founde", "Moderator", "Guest", "Banned"]
    )

    description: str | None = Field(
        default=None,
        description="Group role type description",
        examples=["Only moderators role type"]
    )

    group_id: str | UUID = Field(
        default=...,
        description="Group role type group id",
        examples=["Group role name"]
    )