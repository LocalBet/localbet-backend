"""
Group updated_at value object.
"""

from datetime import datetime

from backend.shared.models import ValueObject


class GroupUpdatedAt(ValueObject[datetime]):
    """
    Group updated_at value object.
    """

    def _validate(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise ValueError("Updated_at must be a datetime object")
