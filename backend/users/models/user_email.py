"""
UserEmail value object.
"""

from typing_extensions import override

from backend.shared.models import ValueObject
from backend.users.errors import UserEmailMaxLengthError, UserEmailMinLengthError, UserEmailTypeError


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
            raise UserEmailMinLengthError(email=value, min_length=self.__USER_EMAIL_MIN_LENGTH)

        if len(value) > self.__USER_EMAIL_MAX_LENGTH:
            raise UserEmailMaxLengthError(max_length=self.__USER_EMAIL_MAX_LENGTH)

