"""
UserEmailTypeError module.
"""

from typing import Any

from backend.shared.errors import ValidationError


class UserEmailTypeError(ValidationError):
    """
    UserEmailTypeError class.
    """

    __email: Any

    def __init__(self, *, email: Any) -> None:
        """
        UserEmailTypeError constructor.

        Args:
            email (Any): The value that caused the error.
        """
        self.__email = email

        message = f"UserEmail value <<<{email}>>> must be a string. Got <<<{type(email).__name__}>>> type."
        super().__init__(message=message)

    @property
    def email(self) -> Any:
        """
        Returns the value that caused the error.

        Returns:
            Any: The value that caused the error.
        """
        return self.__email
