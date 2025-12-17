"""
Bet created_by value object.
"""

from uuid import UUID

from backend.shared.models import ValueObject


class BetCreatedBy(ValueObject[UUID]):
    """
    Bet created_by value object (creator user UUID).
    Renamed from BetUserId.
    """

    def _validate(self, value: str | UUID) -> None:
        # UUID constructor will raise ValueError if invalid
        if isinstance(value, str):
            UUID(value)
    
    def _process(self, value: str | UUID) -> UUID:
        if isinstance(value, str):
            return UUID(value)
        return value