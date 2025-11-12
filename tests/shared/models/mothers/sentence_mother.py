"""
SentenceMother module.
"""

from random import randint
from typing import Any

from .base_mother import BaseMother


class SentenceMother(BaseMother):
    """
    SentenceMother class.
    """

    @classmethod
    def random(cls, min_length: int = 1, max_length: int = 10, final_punctuation: bool = False) -> str:
        """
        Create a random sentence.

        Args:
            min_length (int, optional): Minimum word length. Defaults to 1.
            max_length (int, optional): Maximum word length. Defaults to 10.
            final_punctuation (bool, optional): Whether to add a final punctuation. Defaults to False.

        Returns:
            str: Random sentence.
        """
        word_length = randint(a=min_length, b=max_length)  # noqa: S311  # nosec
        sentence = cls._faker().sentence(nb_words=word_length)

        return sentence if final_punctuation else sentence[:-1]

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid sentence type.

        Returns:
            Any: Invalid sentence type.
        """
        return cls._invalid_type(remove_types={str})
