"""
Schema for the user login data.
"""

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class LoginSchema(BaseRequestSchema):
    """
    Schema for the user login data.
    """

    email: str = Field(
        default=...,
        description="The user's email address.",
        examples=["joedoesmith@example.com"],
    )

    password: str = Field(
        default=...,
        description="The user's password in plain text.",
        examples=["P#ssW0rd@23!"],
    )
