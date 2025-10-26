"""
DatetimeError module.
"""

from typing import Any

from .validation_error import ValidationError


class DatetimeError(ValidationError):
    """
    DatetimeError class.
    """

    __datetime: Any

    def __init__(self, datetime: Any) -> None:
        """
        DatetimeError constructor.

        Args:
            datetime (Any): The value that caused the error.
        """
        self.__datetime = datetime

        message = f"Datetime value <<<{datetime}>>> must be a valid ISO 8601 datetime."
        super().__init__(message=message)

    @property
    def datetime(self) -> Any:
        """
        Returns the value that caused the error.

        Returns:
            Any: The value that caused the error.
        """
        return self.__datetime
