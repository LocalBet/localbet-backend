"""
DatetimeMother module.
"""

from datetime import UTC, datetime
from typing import Any

from .base_mother import BaseMother


class DatetimeMother(BaseMother):
    """
    DatetimeMother class.
    """

    @classmethod
    def random(cls) -> datetime:
        """
        Create a random datetime.

        Returns:
            datetime: Random datetime.
        """
        return cls._faker().date_time(tzinfo=UTC)

    @classmethod
    def now(cls) -> datetime:
        """
        Create a datetime representing the current moment.

        Returns:
            datetime: Current datetime.
        """
        return datetime.now(UTC)

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid datetime type.

        Returns:
            Any: Invalid datetime type.
        """
        return cls._invalid_type(remove_types={datetime})

    def prepare_now_method(self, now: datetime) -> None:
        """
        Prepare the now method to return the given datetime.

        Args:
            now (datetime): Datetime to return.
        """
        self.__now_datetime = now
