"""
Bet min_bet value object.
"""

from backend.shared.models import ValueObject


class BetMinBet(ValueObject[int]):
    """
    Bet min_bet value object (renamed from BetCost).
    Minimum amount of coins required to join the bet.
    """

    def _validate(self, value: int) -> None:
        if value < 0:
            raise ValueError("Minimum bet cannot be negative")
