"""
Schemas for getting Group role type
"""

from uuid import UUID
from pydantic import BaseModel, Field

class GroupRoleTypeUpdateSchema(BaseModel):
    """
    Schema for getting an Group Role type
    """

    name: str | None= Field(
        default=...,
        description="Group role type name",
        examples=["Founde", "Moderator", "Guest", "Banned"]
    )

    description: str | None = Field(
        default=None,
        description="Group role type description",
        examples=["Only moderators role type"]
    )