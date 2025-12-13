"""
Schema for getting an user.
"""

from pydantic import BaseModel, Field


class UserGetSchema(BaseModel):
    """
    Schema for getting an user.
    """

    username: str = Field(
        default=...,
        description="User username.",
        examples=["johndoesmith"],
    )

    email: str = Field(
        default=...,
        description="User email.",
        examples=["joedoesmith@example.com"],
    )


    coins: float = Field(
        default=...,
        description="User coins.",
        examples=[100.0]
    )
