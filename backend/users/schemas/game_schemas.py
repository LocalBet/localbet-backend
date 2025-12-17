"""
Mini games request and response schemas.
"""

from pydantic import BaseModel, Field


class RoulettePlaySchema(BaseModel):
    """
    Schema for playing roulette.
    """

    bet_amount: int = Field(
        default=...,
        description="Amount of coins to bet.",
        gt=0,
        examples=[100, 50],
    )

    bet_type: str = Field(
        default="red",
        description="Type of bet: 'red', 'black', or 'number'.",
        examples=["red", "black", "number"],
    )

    number: int | None = Field(
        default=None,
        description="Specific number to bet on (0-36), required if bet_type='number'.",
        ge=0,
        le=36,
        examples=[7, 23],
    )


class CardFlipPlaySchema(BaseModel):
    """
    Schema for playing card flip.
    """

    bet_amount: int = Field(
        default=...,
        description="Amount of coins to bet.",
        gt=0,
        examples=[100, 50],
    )

    guess: str = Field(
        default=...,
        description="Guess: 'heads' or 'tails'.",
        examples=["heads", "tails"],
    )


class GameResultSchema(BaseModel):
    """
    Schema for game result response.
    """

    result: str = Field(
        default=...,
        description="Result: 'won' or 'lost'.",
        examples=["won", "lost"],
    )

    winnings: int = Field(
        default=...,
        description="Amount won (0 if lost, bet_amount * multiplier if won).",
        examples=[0, 200],
    )

    new_balance: int = Field(
        default=...,
        description="New coin balance after game.",
        examples=[1200],
    )

    game_details: dict = Field(
        default=...,
        description="Game-specific details (e.g., roulette number, card result).",
        examples=[{"number": 7, "color": "red"}],
    )

    transaction_id: str = Field(
        default=...,
        description="Wallet transaction ID.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
