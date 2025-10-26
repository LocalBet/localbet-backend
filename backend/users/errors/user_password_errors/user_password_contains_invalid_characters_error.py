"""
UserPasswordContainsInvalidCharactersError module.
"""

from backend.shared.errors import ValidationError


class UserPasswordContainsInvalidCharactersError(ValidationError):
    """
    UserPasswordContainsInvalidCharactersError class.
    """

    def __init__(self) -> None:
        """
        UserPasswordContainsInvalidCharactersError constructor.
        """
        message = "UserPassword value contains invalid characters. Only printable characters are allowed."
        super().__init__(message=message)
