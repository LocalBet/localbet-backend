"""
UserUsernameContainsInvalidCharactersError module.
"""

from backend.shared.errors import ValidationError


class UserUsernameContainsInvalidCharactersError(ValidationError):
    """
    UserUsernameContainsInvalidCharactersError class.
    """

    __username: str

    def __init__(self, *, username: str) -> None:
        """
        UserUsernameContainsInvalidCharactersError constructor.

        Args:
            username (str): The value that caused the error.
        """
        self.__username = username

        message = f'UserUsername value <<<{username}>>> contains invalid characters. Only alphanumeric characters and underscores are allowed.'  # noqa: E501 # fmt: skip
        super().__init__(message=message)

    @property
    def username(self) -> str:
        """
        Returns the value that caused the error.

        Returns:
            str: The value that caused the error.
        """
        return self.__username
