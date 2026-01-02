"""
Schema for creating an user.
"""

from datetime import date
from pydantic import Field, field_validator

from backend.shared.schemas import BaseRequestSchema


class CreateUserSchema(BaseRequestSchema):
    """
    Schema for creating a user with legal compliance.
    Identity verification (phone, country) is optional at registration.
    """

    # Account fields (required)
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

    # Profile fields (optional - can be provided later for verification)
    full_name: str | None = Field(
        default=None,
        description="User full name.",
        examples=["John Doe Smith"],
    )

    phone_number: str | None = Field(
        default=None,
        description="User phone number (optional, required for full verification).",
        examples=["+34612345678"],
    )

    birth_date: date = Field(
        default=...,
        description="User birth date (required for age verification, must be 18+).",
        examples=["2000-01-15"],
    )

    country: str | None = Field(
        default=None,
        description="User country (optional, ISO 2-letter code).",
        examples=["ES"],
    )

    # Legal/compliance fields (required)
    accepted_terms: bool = Field(
        default=...,
        description="User has accepted terms and conditions (required).",
    )

    accepted_privacy_policy: bool = Field(
        default=...,
        description="User has accepted privacy policy (required).",
    )

    @field_validator('accepted_terms')
    @classmethod
    def validate_terms(cls, v: bool) -> bool:
        if not v:
            raise ValueError("Must accept terms and conditions")
        return v

    @field_validator('accepted_privacy_policy')
    @classmethod
    def validate_privacy(cls, v: bool) -> bool:
        if not v:
            raise ValueError("Must accept privacy policy")
        return v

    @field_validator('birth_date')
    @classmethod
    def validate_age(cls, v: date) -> date:
        """
        Validate that user is at least 18 years old.
        This is the ONLY place where age is validated.
        """
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError("Must be at least 18 years old")
        return v
