"""
UserCreatedSchema module.
"""

from pydantic import BaseModel, Field


class UserCreatedSchema(BaseModel):
    """
    UserCreatedSchema class.
    """

    message: str = Field(
        default="User created successfully.",
        description="Message that indicates that the user was created successfully.",
        examples=["User created successfully."],
    )
