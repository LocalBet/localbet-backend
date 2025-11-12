"""
PasswordMother module.
"""

from random import choice, randint
from typing import Any

from .base_mother import BaseMother


class PasswordMother(BaseMother):
    """
    PasswordMother class.
    """

    @classmethod
    def random(
        cls,
        length: int | None = None,
        include_lower_case: bool = True,
        include_upper_case: bool = True,
        include_digits: bool = True,
        include_special_chars: bool = True,
    ) -> str:
        """
        Create a random password. If the length is not provided, it will be randomly generated.

        Args:
            length (int, optional): Password length. Defaults to None.
            include_lower_case (bool, optional): Whether to include lower case characters. Defaults to True.
            include_upper_case (bool, optional): Whether to include upper case characters. Defaults to True.
            include_digits (bool, optional): Whether to include digits. Defaults to True.
            include_special_chars (bool, optional): Whether to include special characters. Defaults to True.

        Returns:
            str: Random password.
        """
        if length is None:
            length = randint(a=12, b=128)  # noqa: S311  # nosec

        return cls._faker().password(
            length=length,
            lower_case=include_lower_case,
            upper_case=include_upper_case,
            digits=include_digits,
            special_chars=include_special_chars,
        )

    @classmethod
    def of_length(cls, length: int) -> str:
        """
        Create a person password of the given length.

        Args:
            length (int): Password length.

        Returns:
            str: Person password of the given length.
        """
        return "a" * length

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid password type.

        Returns:
            Any: Invalid password type.
        """
        return cls._invalid_type(remove_types={str})

    @classmethod
    def invalid_value(cls) -> str:
        """
        Create an invalid password value.

        Returns:
            str: Invalid password value.
        """
        non_printable_chars = "".join(chr(i) for i in range(32))

        return "".join(choice(seq=non_printable_chars) for _ in range(12))  # noqa: S311  # nosec
