"""
Schema for updating an user.
"""

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class UserUpdateSchema(BaseRequestSchema):
    """
    Schema for updating a user (safe fields only).
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

    full_name: str | None = Field(
        default=None,
        description="User full name.",
        examples=["John Doe Smith"],
    )

    phone_number: str | None = Field(
        default=None,
        description="User phone number.",
        examples=["+34612345678"],
    )

    country: str | None = Field(
        default=None,
        description="User country.",
        examples=["ES"],
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
