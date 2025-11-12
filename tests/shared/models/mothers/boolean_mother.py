"""
BooleanMother module.
"""

from typing import Any

from .base_mother import BaseMother


class BooleanMother(BaseMother):
    """
    BooleanMother class.
    """

    @classmethod
    def random(cls) -> bool:
        """
        Create a random boolean.

        Returns:
            bool: Random boolean.
        """
        return cls._faker().pybool()

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid boolean type.

        Returns:
            Any: Invalid boolean type.
        """
        return cls._invalid_type(remove_types={bool})
