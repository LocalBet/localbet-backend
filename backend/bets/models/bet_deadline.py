"""
Bet deadline value object.
"""

from datetime import datetime

from backend.shared.models import ValueObject


class BetDeadline(ValueObject[datetime]):
    """
    Bet deadline value object (timestamp when bet closes).
    """

    def _validate(self, value: datetime) -> None:
        # datetime validation - just check it's the right type
        if not isinstance(value, datetime):
            raise ValueError("Deadline must be a datetime object")
