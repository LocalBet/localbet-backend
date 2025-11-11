"""
WordMother module.
"""

from typing import Any

from .base_mother import BaseMother


class WordMother(BaseMother):
    """
    WordMother class.
    """

    @classmethod
    def random(cls) -> str:
        """
        Create a random word.

        Returns:
            str: Random word.
        """
        return cls._faker().word()

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid word type.

        Returns:
            Any: Invalid word type.
        """
        return cls._invalid_type(remove_types={str})

    @classmethod
    def of_length(cls, length: int) -> str:
        """
        Create a word of the given length.

        Args:
            length (int): Word length.

        Returns:
            str: Word of the given length.
        """
        return "a" * length
