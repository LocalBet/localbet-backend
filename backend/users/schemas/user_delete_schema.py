"""
Schema for deleting an user.
"""

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class UserDeleteSchema(BaseRequestSchema):
    """
    Schema for deleting an user.
    """

    password: str = Field(
        default=...,
        description='Unhashed user password.',
        examples=['P#ssW0rd@23!'],
    )
