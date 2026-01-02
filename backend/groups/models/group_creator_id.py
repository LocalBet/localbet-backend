"""
Group creator_id value object.
"""

from uuid import UUID

from backend.shared.models import ValueObject


class GroupCreatorId(ValueObject[UUID]):
    """
    Group creator_id value object.
    """

    def _validate(self, value: str | UUID) -> None:
        if isinstance(value, str):
            UUID(value)
    
    def _process(self, value: str | UUID) -> UUID:
        if isinstance(value, str):
            return UUID(value)
        return value
