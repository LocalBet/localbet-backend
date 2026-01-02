"""
Bet title value object.
"""

from backend.shared.models import ValueObject


class BetTitle(ValueObject[str]):
    """
    Bet title value object (renamed from BetName).
    """

    def _validate(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Bet title cannot be empty")
        if len(value) > 255:
            raise ValueError("Bet title cannot exceed 255 characters")
