"""
Schema for updating an user.
"""

from uuid import UUID

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class UserUpdateSchema(BaseRequestSchema):
    """
    Schema for updating an user.
    """

    name: str | None = Field(
        default=...,
        description="User full name.",
        examples=["John Doe Smith"],
    )

    username: str | None = Field(
        default=...,
        description="User username.",
        examples=["johndoesmith"],
    )

    email: str | None = Field(
        default=...,
        description="User email",
        examples=["joedoesmith@example.com"],
    )

    role_id: str | UUID | None = Field(
        default=...,
        description="User role identifier",
        examples=["3fa85f64-5717-4562-b3fc-29601a5f462"],
    )

    old_password: str | None = Field(
        default=...,
        serialization_alias="oldPassword",
        description="Old user password",
        examples=["P#ssW0rd@23!"],
    )

    new_password: str | None = Field(
        default=...,
        serialization_alias="newPassword",
        description="New user password",
        examples=["P#ssW0rd@23!"],
    )

    new_password_verification: str | None = Field(
        default=...,
        serialization_alias="newPasswordVerification",
        description="Unhashed user new password verification",
        examples=["P#ssW0rd@23!"],
    )
