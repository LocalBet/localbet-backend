"""
Datetime value object module.
"""

from datetime import datetime

from typing_extensions import override

from backend.shared.errors import DatetimeError

from .value_object import ValueObject


class Datetime(ValueObject[str | datetime]):
    """
    Datetime value object class.
    """

    @override
    def _process(self, value: str | datetime) -> datetime:
        """
        This method processes the datetime value.

        Args:
            value (str | datetime): The datetime value.

        Returns:
            datetime: The processed datetime value.
        """
        if isinstance(value, datetime):
            return value

        return datetime.fromisoformat(value)

    @override
    def _validate(self, value: str | datetime) -> None:
        """
        This method validates that the datetime value follows the domain rules.

        Args:
            value (str | datetime): The datetime value.

        Raises:
            DatetimeError: If the provided value is not a valid datetime.
        """
        if isinstance(value, datetime):
            return None

        try:
            datetime.fromisoformat(value)
        except Exception as exception:
            raise DatetimeError(datetime=value) from exception

    @property
    @override
    def value(self) -> datetime:
        """
        Returns the datetime value object value.

        Returns:
            datetime: The datetime value object value.
        """
        return self._value  # type: ignore[return-value]
