"""
UserPasswordMother module.
"""

from backend.users.models import UserPassword
from tests.shared.models.mothers import PasswordMother


class UserPasswordMother(PasswordMother):
    """
    UserPasswordMother class.
    """

    @classmethod
    def create(
        cls,
        value: str | None = None,
        length: int | None = None,
        include_lower_case: bool = True,
        include_upper_case: bool = True,
        include_digits: bool = True,
        include_special_chars: bool = True,
    ) -> UserPassword:
        """
        Create a user password. If the value is not provided, it will be randomly generated.

        Args:
            value (str, optional): User password value. Defaults to None.
            length (int, optional): Password length. Defaults to None.
            include_lower_case (bool, optional): Whether to include lower case characters. Defaults to True.
            include_upper_case (bool, optional): Whether to include upper case characters. Defaults to True.
            include_digits (bool, optional): Whether to include digits. Defaults to True.
            include_special_chars (bool, optional): Whether to include special characters. Defaults to True.

        Returns:
            UserPassword: User password.
        """
        if value is None:
            value = cls.random(
                length=length,
                include_lower_case=include_lower_case,
                include_upper_case=include_upper_case,
                include_digits=include_digits,
                include_special_chars=include_special_chars,
            )

        return UserPassword(value=value)

    @classmethod
    def unhashed(
        cls,
        value: str | None = None,
        length: int | None = None,
        include_lower_case: bool = True,
        include_upper_case: bool = True,
        include_digits: bool = True,
        include_special_chars: bool = True,
    ) -> str:
        """
        Create an unhashed user password. If the value is not provided, it will be randomly generated.

        Args:
            value (str, optional): User password value. Defaults to None.
            length (int, optional): Password length. Defaults to None.
            include_lower_case (bool, optional): Whether to include lower case characters. Defaults to True.
            include_upper_case (bool, optional): Whether to include upper case characters. Defaults to True.
            include_digits (bool, optional): Whether to include digits. Defaults to True.
            include_special_chars (bool, optional): Whether to include special characters. Defaults to True.

        Returns:
            str: Unhashed user password.
        """
        if value is None:
            value = cls.random(
                length=length,
                include_lower_case=include_lower_case,
                include_upper_case=include_upper_case,
                include_digits=include_digits,
                include_special_chars=include_special_chars,
            )

        UserPassword(value=value)

        return value
