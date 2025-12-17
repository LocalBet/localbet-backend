"""
Wallet transactions response schema.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class WalletTransactionSchema(BaseModel):
    """
    Schema for a single wallet transaction.
    """

    id: str = Field(
        default=...,
        description="Transaction ID.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    amount: int = Field(
        default=...,
        description="Transaction amount (positive=credit, negative=debit).",
        examples=[500, -100],
    )

    transaction_type: str = Field(
        default=...,
        description="Type of transaction.",
        examples=["bet_won", "bet_placed", "purchase", "initial_balance"],
    )

    description: str | None = Field(
        default=None,
        description="Human-readable description.",
        examples=["Ganaste 500 monedas - Grupo: Liga MX"],
    )

    created_at: datetime = Field(
        default=...,
        description="Transaction timestamp.",
    )


class WalletTransactionsListSchema(BaseModel):
    """
    Schema for list of wallet transactions.
    """

    transactions: list[WalletTransactionSchema] = Field(
        default=...,
        description="List of transactions.",
    )

    total: int = Field(
        default=...,
        description="Total number of transactions (for pagination).",
        examples=[25],
    )
