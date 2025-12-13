"""
Schema for updating an user.
"""

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class UserUpdateSchema(BaseRequestSchema):
    """
    Schema for updating an user.
    """

    username: str | None = Field(
        default=None,
        description="User username.",
        examples=["johndoesmith"],
    )

    email: str | None = Field(
        default=None,
        description="User email.",
        examples=["joedoesmith@example.com"],
    )

    old_password: str | None = Field(
        default=None,
        serialization_alias="oldPassword",
        description="Old user password.",
        examples=["P#ssW0rd@23!"],
    )

    new_password: str | None = Field(
        default=None,
        serialization_alias="newPassword",
        description="New user password.",
        examples=["P#ssW0rd@23!"],
    )

    new_password_verification: str | None = Field(
        default=None,
        serialization_alias="newPasswordVerification",
        description="New user password verification.",
        examples=["P#ssW0rd@23!"],
    )
