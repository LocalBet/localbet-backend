"""
Schema for the user login data.
"""

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class LoginSchema(BaseRequestSchema):
    """
    Schema for the user login data.
    """

    identifier: str = Field(
        default=...,
        description="Username or email.",
        examples=["johndoesmith", "john@example.com"],
    )

    password: str = Field(
        default=...,
        description="The user's password in plain text.",
        examples=["P#ssW0rd@23!"],
    )
