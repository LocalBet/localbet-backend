"""
UsernameMother module.
"""

from random import choice
from typing import Any

from .base_mother import BaseMother


class UsernameMother(BaseMother):
    """
    UsernameMother class.
    """

    @classmethod
    def random(cls) -> str:
        """
        Create a random username.

        Returns:
            int: Random username.
        """
        username = cls._faker().user_name()
        username = username.replace('-', '_')

        return username

    @classmethod
    def of_length(cls, length: int) -> str:
        """
        Create a person username of the given length.

        Args:
            length (int): Username length.

        Returns:
            str: Person username of the given length.
        """
        return 'a' * length

    @classmethod
    def some_uppercase(cls) -> str:
        """
        Create a username with some uppercase characters. (e.g., 'Username', 'UsErnAme', 'USERNAME').

        Returns:
            str: Username with some uppercase characters.
        """
        username = cls.random()

        options = [
            username.title(),
            'A'.join(choice(seq=[word.lower(), word.upper()]) for word in username),  # noqa: S311  # nosec
            username.upper(),
        ]

        return choice(seq=options)  # noqa: S311  # nosec

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid username type.

        Returns:
            Any: Invalid username type.
        """
        return cls._invalid_type(remove_types={str})

    @classmethod
    def invalid_value(cls) -> str:
        """
        Create an invalid username value. Includes non-printable characters.
        Included space, dot, at symbol, hyphen, and other special characters are
        tested in other methods.

        Returns:
            str: Invalid username value.
        """
        non_printable_chars = ''.join(chr(i) for i in range(33))

        return ''.join(choice(seq=non_printable_chars) for _ in range(10))  # noqa: S311  # nosec


