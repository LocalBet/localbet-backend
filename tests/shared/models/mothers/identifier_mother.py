"""
IdentifierMother module.
"""

from random import choice, randint
from typing import Any

from .base_mother import BaseMother


class IdentifierMother(BaseMother):
    """
    IdentifierMother class.
    """

    @classmethod
    def random(cls) -> str:
        """
        Create a random identifier.

        Returns:
            str: Random identifier.
        """
        identifier = str(object=cls._faker().uuid4())

        return choice(seq=[identifier.lower(), identifier.upper()])  # noqa: S311  # nosec

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid identifier type.

        Returns:
            Any: Invalid identifier type.
        """
        return cls._invalid_type()

    @classmethod
    def invalid_value(cls) -> str:
        """
        Create an invalid identifier value.

        Returns:
            str: Invalid identifier value.
        """
        values: list[str | int] = [
            randint(a=0, b=100),  # noqa: S311  # nosec
            'a' * randint(a=1, b=100),  # noqa: S311  # nosec
            ' ' * randint(a=1, b=10),  # noqa: S311  # nosec
            cls.random().replace('-', '_'),
            cls.random()[:8],
            cls.random() + 'extra',
        ]

        return str(object=choice(seq=values))  # noqa: S311  # nosec
