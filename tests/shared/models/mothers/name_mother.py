"""
NameMother module.
"""

from random import choice
from typing import Any

from .base_mother import BaseMother


class NameMother(BaseMother):
    """
    NameMother class.
    """

    @classmethod
    def random(cls) -> str:
        """
        Create a random person full name.

        Returns:
            str: Random person full name.
        """
        name = cls._faker().name()

        return choice(seq=(name.lower(), name.upper(), name.title()))  # noqa: S311  # nosec

    @classmethod
    def of_length(cls, length: int) -> str:
        """
        Create a person name of the given length.

        Args:
            length (int): Name length.

        Returns:
            str: Person name of the given length.
        """
        return "a" * length

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid name type.

        Returns:
            Any: Invalid name type.
        """
        return cls._invalid_type(remove_types={str})

    @classmethod
    def invalid_value(cls) -> str:
        """
        Create an invalid name value.

        Returns:
            str: Invalid name value.
        """
        non_printable_chars = "".join(chr(i) for i in range(32))

        return "".join(choice(seq=non_printable_chars) for _ in range(10))  # noqa: S311  # nosec
