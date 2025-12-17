"""
Bet description value object.
"""

from backend.shared.models import ValueObject


class BetDescription(ValueObject[str]):
    """
    Bet description value object.
    """

    def _validate(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Bet description cannot be empty")
