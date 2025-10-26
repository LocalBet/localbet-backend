"""
UserPassword value object.
"""

from typing_extensions import override

from backend.shared.models import ValueObject
from backend.users.errors import (
    UserPasswordContainsInvalidCharactersError,
    UserPasswordMaxLengthError,
    UserPasswordMinLengthError,
    UserPasswordTypeError,
)


class UserPassword(ValueObject[str]):
    """
    UserPassword value object.
    """

    __USER_PASSWORD_MIN_LENGTH: int = 12
    __USER_PASSWORD_MAX_LENGTH: int = 150

    @override
    def __eq__(self, other: object) -> bool:
        """
        Compares self with other UserPassword object.

        Args:
            other (object): UserPassword object.

        Raises:
            NotImplementedError: If the objects are of different types.

        Returns:
            bool: True if the UserPassword objects are equal, False otherwise.
        """
        if not isinstance(other, UserPassword) and not isinstance(other, str):
            raise NotImplementedError

        if isinstance(other, str):
            return self._value == other  # TODO: Verify hashed password

        return self._value == other.value

    @override
    def _process(self, value: str) -> str:
        """
        This method processes the user password before storage.

        Args:
            value (str): User password.

        Returns:
            str: The processed user password.
        """
        if value.startswith("$argon2id$v=19$m"):
            return value

        return value  # TODO: Hash password here

    @override
    def _validate(self, value: str) -> None:
        """
        This method validates that the value follows the domain rules.

        Args:
            value (str): User password.

        Raises:
            UserPasswordTypeError: If the value is not a string.
            UserPasswordMinLengthError: If the value length is less than the minimum allowed.
            UserPasswordMaxLengthError: If the value length is greater than the maximum allowed.
            UserPasswordContainsInvalidCharactersError: If the value contains invalid characters.
            UserPasswordContainsInvalidCharactersError: If the value contains leading or trailing whitespaces.
        """
        if type(value) is not str:
            raise UserPasswordTypeError()

        if len(value) < self.__USER_PASSWORD_MIN_LENGTH:
            raise UserPasswordMinLengthError(min_length=self.__USER_PASSWORD_MIN_LENGTH)

        if len(value) > self.__USER_PASSWORD_MAX_LENGTH:
            raise UserPasswordMaxLengthError(max_length=self.__USER_PASSWORD_MAX_LENGTH)

        if not value.isprintable():
            raise UserPasswordContainsInvalidCharactersError()
