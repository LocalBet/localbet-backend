"""
Schema for getting an user.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class UserGetSchema(BaseModel):
    """
    Schema for getting an user.
    """

    id: str = Field(
        default=...,
        description="User id.",
        examples=["d71a63eb-3d8d-4259-a026-49bb2c3d9fa3"],
    )

    name: str = Field(
        default=...,
        description="User full name.",
        examples=["John Doe Smith"],
    )

    role_id: str | UUID = Field(
        default=...,
        description="User role identifier",
        examples=["3fa85f64-5717-4562-b3fc-29601a5f462"],
    )

    username: str = Field(
        default=...,
        description="User username.",
        examples=["johndoesmith"],
    )

    email: str = Field(
        default=...,
        description="User email",
        examples=["joedoesmith@example.com"],
    )
