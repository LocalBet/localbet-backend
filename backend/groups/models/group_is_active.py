"""
Group is_active value object.
"""

from backend.shared.models import ValueObject


class GroupIsActive(ValueObject[bool]):
    """
    Group is_active value object.
    """

    def _validate(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean")
