"""
UserUsernameMinLengthError module.
"""

from backend.shared.errors import ValidationError


class UserUsernameMinLengthError(ValidationError):
    """
    UserUsernameMinLengthError class.
    """

    __username: str
    __min_length: int

    def __init__(self, *, username: str, min_length: int) -> None:
        """
        UserUsernameMinLengthError constructor.

        Args:
            username (str): The value that caused the error.
            min_length (int): The minimum allowed length.
        """
        self.__username = username
        self.__min_length = min_length

        message = f'UserUsername value <<<{username}>>> must be at least <<<{min_length}>>> characters long. Got <<<{len(username)}>>> characters.'  # noqa: E501 # fmt: skip
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
    def min_length(self) -> int:
        """
        Returns the minimum allowed length.

        Returns:
            int: The minimum allowed length.
        """
        return self.__min_length
