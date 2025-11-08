"""
DateMother module.
"""

from datetime import date
from typing import Any

from .base_mother import BaseMother


class DateMother(BaseMother):
    """
    DateMother class.
    """

    @classmethod
    def random(cls) -> date:
        """
        Create a random date.

        Returns:
            date: Random date.
        """
        return date.fromisoformat(cls._faker().date())

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid date type.

        Returns:
            Any: Invalid date type.
        """
        return cls._invalid_type(remove_types={date})
