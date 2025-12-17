"""
Purchase tokens schema.
"""

from pydantic import BaseModel, Field


class PurchaseTokensSchema(BaseModel):
    """
    Schema for purchasing tokens.
    """

    amount: int = Field(
        default=...,
        description="Amount of tokens to purchase.",
        gt=0,
        examples=[1000, 500],
    )

    payment_method: str = Field(
        default="mock",
        description="Payment method (MVP: always 'mock').",
        examples=["mock"],
    )


class PurchaseTokensResponseSchema(BaseModel):
    """
    Schema for purchase tokens response.
    """

    transaction_id: str = Field(
        default=...,
        description="Transaction ID.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    amount: int = Field(
        default=...,
        description="Amount of tokens purchased.",
        examples=[1000],
    )

    new_balance: int = Field(
        default=...,
        description="New coin balance after purchase.",
        examples=[1500],
    )
