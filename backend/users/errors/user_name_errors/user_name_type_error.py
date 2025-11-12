"""
UserNameTypeError module.
"""

from typing import Any

from backend.shared.errors import ValidationError


class UserNameTypeError(ValidationError):
    """
    UserNameTypeError class.
    """

    __name: Any

    def __init__(self, *, name: Any) -> None:
        """
        UserNameTypeError constructor.

        Args:
            name (Any): The value that caused the error.
        """
        self.__name = name

        message = f"UserName value <<<{name}>>> must be a string. Got <<<{type(name).__name__}>>> type."
        super().__init__(message=message)

    @property
    def name(self) -> Any:
        """
        Returns the value that caused the error.

        Returns:
            Any: The value that caused the error.
        """
        return self.__name
