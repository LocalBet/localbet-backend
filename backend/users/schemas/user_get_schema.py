"""
Schema for getting an user.
"""

from datetime import date, datetime
from pydantic import BaseModel, Field


class UserGetSchema(BaseModel):
    """
    Schema for getting a user with profile data.
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

    coins: int = Field(
        default=...,
        description="User coins (G Tokens).",
        examples=[1000]
    )

    wins: int = Field(
        default=...,
        description="Total bets won.",
        examples=[5]
    )

    losses: int = Field(
        default=...,
        description="Total bets lost.",
        examples=[2]
    )

    active_groups_count: int = Field(
        default=...,
        description="Number of active groups user is member of.",
        examples=[3]
    )

    full_name: str | None = Field(
        default=None,
        description="User full name.",
        examples=["John Doe Smith"],
    )

    phone_number: str | None = Field(
        default=None,
        description="User phone number (None if not provided).",
        examples=["+34612345678"],
    )

    birth_date: date = Field(
        default=...,
        description="User birth date.",
        examples=["2000-01-15"],
    )

    country: str | None = Field(
        default=None,
        description="User country (None if not provided).",
        examples=["ES"],
    )

    verified_at: datetime | None = Field(
        default=None,
        description="Verification timestamp.",
    )

    created_at: datetime = Field(
        default=...,
        description="Account creation timestamp.",
    )

    updated_at: datetime = Field(
        default=...,
        description="Last update timestamp.",
    )
