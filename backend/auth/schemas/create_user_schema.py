"""
Schema for creating an user.
"""

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class CreateUserSchema(BaseRequestSchema):
    """
    Schema for creating an user (simplified).
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

    password: str = Field(
        default=...,
        description="Unhashed user password.",
        examples=["P#ssW0rd@23!"],
    )

    password_verification: str = Field(
        default=...,
        description="Unhashed user password verification.",
        examples=["P#ssW0rd@23!"],
    )
