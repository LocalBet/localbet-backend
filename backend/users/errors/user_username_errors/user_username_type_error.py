"""
UserUsernameTypeError module.
"""

from typing import Any

from backend.shared.errors import ValidationError


class UserUsernameTypeError(ValidationError):
    """
    UserUsernameTypeError class.
    """

    __username: Any

    def __init__(self, *, username: Any) -> None:
        """
        UserUsernameTypeError constructor.

        Args:
            username (Any): The value that caused the error.
        """
        self.__username = username

        message = f"UserUsername value <<<{username}>>> must be a string. Got <<<{type(username).__name__}>>> type."
        super().__init__(message=message)

    @property
    def username(self) -> Any:
        """
        Returns the value that caused the error.

        Returns:
            Any: The value that caused the error.
        """
        return self.__username
