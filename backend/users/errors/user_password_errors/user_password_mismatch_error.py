"""
UserPasswordMismatchError module.
"""

from backend.shared.errors import ValidationError


class UserPasswordMismatchError(ValidationError):
    """
    UserPasswordMismatchError class.
    """

    def __init__(self) -> None:
        """
        UserPasswordMismatchError constructor.
        """
        message = "The password and the password verification do not match."
        super().__init__(message=message)
