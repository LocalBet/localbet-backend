"""
UserCreatedSchema module.
"""

from pydantic import BaseModel, Field


class UserCreatedSchema(BaseModel):
    """
    UserCreatedSchema class.
    """

    message: str = Field(
        default=...,
        description='Message that indicates that the user was created successfully.',
        examples=['A verification link has been sent to the provided email address.'],
    )

    def __init__(self) -> None:
        """
        UserCreatedSchema constructor.
        """
        super().__init__(message='A verification link has been sent to the provided email address.')
