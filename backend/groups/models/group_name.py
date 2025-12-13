"""
Group Name value object.
"""

from backend.shared.models import ValueObject
from backend.groups.errors.errors import GroupNameError  # si encara no existeix, mira sota

class GroupName(ValueObject[str]):
    """
    Group Name value object.
    """

    def _validate(self, value: str) -> None:
        if not value or len(value) < 3:
            raise GroupNameError(name=value)
