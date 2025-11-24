"""
Permission action domain model
"""

from backend.shared.models import ValueObject
from .permission_action_type import PermissionActionType
from typing_extensions import override
from backend.shared.errors import ValidationError

class PermissionAction(ValueObject[PermissionActionType]):
    """PermissionAction value object."""

    @override
    def _validate(self, value: str) -> None:
        """
        This method validates that the value follows the domain rules.

        Args:
        value (str): Value to validate.

        Raises:
        ValidationError: If value is not a valid PermissionActionType.
        """
        try:
            PermissionActionType(value=value)
        except Exception as e:
            raise ValidationError(f'Invalid device type: {value}. Error: {e!s}') from e


