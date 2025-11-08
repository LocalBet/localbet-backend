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
