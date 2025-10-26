"""
UserUsernameUppercaseError module.
"""

from backend.shared.errors import ValidationError


class UserUsernameUppercaseError(ValidationError):
    """
    UserUsernameUppercaseError class.
    """

    __username: str

    def __init__(self, *, username: str) -> None:
        """
        UserUsernameUppercaseError constructor.

        Args:
            username (str): The value that caused the error.
        """
        self.__username = username

        message = f"UserUsername value <<<{username}>>> must be in lowercase."
        super().__init__(message=message)

    @property
    def username(self) -> str:
        """
        Returns the value that caused the error.

        Returns:
            str: The value that caused the error.
        """
        return self.__username
