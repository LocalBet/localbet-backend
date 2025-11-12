"""
IntegerMother module.
"""

from typing import Any

from .base_mother import BaseMother


class IntegerMother(BaseMother):
    """
    IntegerMother class.
    """

    @classmethod
    def random(cls, min_value: int = 0, max_value: int = 100) -> int:
        """
        Create a random integer.

        Args:
            min_value (int, optional): Minimum value. Defaults to 0.
            max_value (int, optional): Maximum value. Defaults to 100.

        Returns:
            int: Random integer.
        """
        return cls._faker().pyint(min_value=min_value, max_value=max_value)

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid integer type.

        Returns:
            Any: Invalid integer type.
        """
        return cls._invalid_type(remove_types={int})
