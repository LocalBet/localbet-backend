"""
UserPasswordTypeError module.
"""

from backend.shared.errors import ValidationError


class UserPasswordTypeError(ValidationError):
    """
    UserPasswordTypeError class.
    """

    def __init__(self) -> None:
        """
        UserPasswordTypeError constructor.
        """
        message = "UserPassword value must be a string."
        super().__init__(message=message)
