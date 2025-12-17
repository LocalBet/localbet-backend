"""
Bet updated_at value object.
"""

from datetime import datetime

from backend.shared.models import ValueObject


class BetUpdatedAt(ValueObject[datetime]):
    """
    Bet updated_at value object (renamed from BetUpdatedDate).
    """

    def _validate(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise ValueError("Updated_at must be a datetime object")
