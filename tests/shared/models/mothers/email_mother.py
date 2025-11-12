"""
EmailMother module.
"""

from typing import Any

from .base_mother import BaseMother


class EmailMother(BaseMother):
    """
    EmailMother class.
    """

    @classmethod
    def random(cls, domain: str | None = None) -> str:
        """
        Create a random email. If the domain is not provided, it will be randomly generated.

        Args:
            domain (str, optional): Email domain. Defaults to None.

        Returns:
            int: Random email.
        """
        return cls._faker().email(safe=False, domain=domain)

    @classmethod
    def invalid_type(cls) -> Any:
        """
        Create an invalid email type.

        Returns:
            Any: Invalid email type.
        """
        return cls._invalid_type(remove_types={str})
