"""
UserUsernameMaxLengthError module.
"""

from backend.shared.errors import ValidationError


class UserUsernameMaxLengthError(ValidationError):
    """
    UserUsernameMaxLengthError class.
    """

    __username: str
    __max_length: int

    def __init__(self, *, username: str, max_length: int) -> None:
        """
        UserUsernameMaxLengthError constructor.

        Args:
            username (str): The value that caused the error.
            max_length (int): The maximum allowed length.
        """
        self.__username = username
        self.__max_length = max_length

        message = f'UserUsername value <<<{username}>>> must be at most <<<{max_length}>>> characters long. Got <<<{len(username)}>>> characters.'  # noqa: E501 # fmt: skip
        super().__init__(message=message)

    @property
    def username(self) -> str:
        """
        Returns the value that caused the error.

        Returns:
            str: The value that caused the error.
        """
        return self.__username

    @property
    def max_length(self) -> int:
        """
        Returns the maximum allowed length.

        Returns:
            int: The maximum allowed length.
        """
        return self.__max_length
