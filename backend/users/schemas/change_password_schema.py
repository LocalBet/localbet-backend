"""
Schema for changing user password.
"""

from pydantic import BaseModel, Field


class ChangePasswordSchema(BaseModel):
    """
    Schema for changing user password.
    """

    current_password: str = Field(
        default=...,
        description="Current password for verification.",
        min_length=6,
        examples=["oldpassword123"],
    )

    new_password: str = Field(
        default=...,
        description="New password.",
        min_length=6,
        examples=["newpassword456"],
    )
