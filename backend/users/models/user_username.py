"""
UserUsername value object.
"""

from typing_extensions import override

from backend.shared.models import ValueObject
from backend.users.errors import (
    UserUsernameContainsInvalidCharactersError,
    UserUsernameMaxLengthError,
    UserUsernameMinLengthError,
    UserUsernameTypeError,
    UserUsernameUppercaseError,
)


class UserUsername(ValueObject[str]):
    """
    UserUsername value object.
    """

    __USER_USERNAME_MIN_LENGTH = 3
    __USER_USERNAME_MAX_LENGTH = 32

    @override
    def _validate(self, value: str) -> None:
        """
        This method validates that the value follows the domain rules.

        Args:
            value (str): User username.

        Raises:
            UserUsernameTypeError: If the value is not a string.
            UserUsernameMinLengthError: If the value length is less than the minimum allowed.
            UserUsernameMaxLengthError: If the value length is greater than the maximum allowed.
            UserUsernameContainsInvalidCharactersError: If the value contains invalid characters.
            UserUsernameUppercaseError: If the value is not in lowercase.
        """
        if type(value) is not str:
            raise UserUsernameTypeError(username=value)

        if len(value) < self.__USER_USERNAME_MIN_LENGTH:
            raise UserUsernameMinLengthError(username=value, min_length=self.__USER_USERNAME_MIN_LENGTH)

        if len(value) > self.__USER_USERNAME_MAX_LENGTH:
            raise UserUsernameMaxLengthError(username=value, max_length=self.__USER_USERNAME_MAX_LENGTH)

        if not value.isalnum() and "_" not in value:
            raise UserUsernameContainsInvalidCharactersError(username=value)

        if not value.islower():
            raise UserUsernameUppercaseError(username=value)
