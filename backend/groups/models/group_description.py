"""
Group description value object.
"""

from backend.shared.models import ValueObject


class GroupDescription(ValueObject[str | None]):
    """
    Group description value object.
    Optional field.
    """

    def _validate(self, value: str | None) -> None:
        # Optional field, no validation needed
        pass
