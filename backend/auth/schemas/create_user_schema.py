"""
Schema for creating an user.
"""

from uuid import UUID, uuid4

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class CreateUserSchema(BaseRequestSchema):
    """
    Schema for creating an user.
    """

    # Allow client to omit `id`; the server will generate one when missing.
    id: str | UUID = Field(
        default_factory=uuid4,
        description='User id. If omitted, the server will generate one.',
        examples=['d71a63eb-3d8d-4259-a026-49bb2c3d9fa3'],
    )

    name: str = Field(
        default=...,
        description='User full name.',
        examples=['John Doe Smith'],
    )

    username: str = Field(
        default=...,
        description='User username.',
        examples=['johndoesmith'],
    )

    email: str = Field(
        default=...,
        description='User email',
        examples=['joedoesmith@example.com'],
    )

    role_id: str | UUID = Field(
        default=...,
        description='User role identifier',
        examples=['3fa85f64-5717-4562-b3fc-29601a5f462'],
    )

    password: str = Field(
        default=...,
        description='Unhashed user password',
        examples=['P#ssW0rd@23!'],
    )

    password_verification: str = Field(
        default=...,
        description='Unhashed user password verification',
        examples=['P#ssW0rd@23!'],
    )
