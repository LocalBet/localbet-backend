"""
UserEmail value object.
"""

from typing_extensions import override

from backend.shared.models import ValueObject
from backend.users.errors import UserEmailTypeError


class UserEmail(ValueObject[str]):
    """
    UserEmail value object.
    """

    __USER_EMAIL_MIN_LENGTH: int = 5
    __USER_EMAIL_MAX_LENGTH: int = 150

    @override
    def _validate(self, value: str) -> None:
        """
        This method validates that the value follows the domain rules.

        Args:
            value (str): User email.

        Raises:
            UserEmailTypeError: If the email value is not a string.
        """
        if type(value) is not str:
            raise UserEmailTypeError(email=value)

        if "@" not in value or "." not in value.split("@")[-1]:
            raise UserEmailTypeError(email=value)

        if len(value) < self.__USER_EMAIL_MIN_LENGTH:
            raise UserEmailTypeError(email=value)

        if len(value) > self.__USER_EMAIL_MAX_LENGTH:
            raise UserEmailTypeError(email=value)

    # @override
    # def _validate(self, value: str) -> None:
    #     """
    #     This method validates that the value follows the domain rules.

    #     Args:
    #         value (str): User name.

    #     Raises:
    #         UserNameTypeError: If the value is not a string.
    #         UserNameMinLengthError: If the value length is less than the minimum allowed.
    #         UserNameMaxLengthError: If the value length is greater than the maximum allowed.
    #         UserNameContainsInvalidCharactersError: If the value contains invalid characters.
    #         UserNameContainsInvalidCharactersError: If the value contains leading or trailing whitespaces.
    #     """
    #     if type(value) is not str:
    #         raise UserNameTypeError(name=value)

    #     if len(value) < self.__USER_NAME_MIN_LENGTH:
    #         raise UserNameMinLengthError(name=value, min_length=self.__USER_NAME_MIN_LENGTH)

    #     if len(value) > self.__USER_NAME_MAX_LENGTH:
    #         raise UserNameMaxLengthError(name=value, max_length=self.__USER_NAME_MAX_LENGTH)

    #     if not value.isprintable():
    #         raise UserNameContainsInvalidCharactersError(name=value)

    #     if value != value.strip():
    #         raise UserNameContainsInvalidCharactersError(name=value)
