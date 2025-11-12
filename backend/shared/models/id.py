"""
Identifier module.
"""

from typing_extensions import override
from uuid import UUID

from backend.shared.errors import IDError

from .value_object import ValueObject


class ID(ValueObject[str | UUID]):
    """
    Identifier class.
    """

    @override
    def _process(self, value: str | UUID) -> str:
        """
        This method processes the identifier value before storage.

        Args:
            value (str | UUID): The identifier value.

        Returns:
            str: The processed identifier value.
        """
        return str(object=value).lower()

    @override
    def _validate(self, value: str | UUID) -> None:
        """
        This method validates that the identifier value follows the domain rules.

        Args:
            value (str | UUID): The identifier value.

        Raises:
            IDError: If the provided value is not a valid UUID.
        """
        try:
            UUID(hex=str(object=value))
        except Exception as exception:
            raise IDError(id=value) from exception
