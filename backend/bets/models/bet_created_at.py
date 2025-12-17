"""
Bet created_at value object.
"""

from datetime import datetime

from backend.shared.models import ValueObject


class BetCreatedAt(ValueObject[datetime]):
    """
    Bet created_at value object (renamed from BetCreatedDate).
    """

    def _validate(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise ValueError("Created_at must be a datetime object")
