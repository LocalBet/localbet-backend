"""
FloatMother module.
"""

from typing import Any

from .base_mother import BaseMother


class FloatMother(BaseMother):
    """
    FloatMother class.
    """

    @classmethod
    def random(cls, min_value: float = 0.0, max_value: float = 1.0) -> float:
        """
        Create a random float.

        Args:
            min_value (float, optional): Minimum value. Defaults to 0.0.
            max_value (float, optional): Maximum value. Defaults to 1.0.

        Returns:
            float: Random float.
        """
        return cls._faker().pyfloat(min_value=min_value, max_value=max_value)

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid float type.

        Returns:
            Any: Invalid float type.
        """
        return cls._invalid_type(remove_types={float})
