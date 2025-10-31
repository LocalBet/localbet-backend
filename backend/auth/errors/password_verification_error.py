"""
PasswordVerificationError module.
"""

from .invalid_credentials_error import InvalidCredentialsError


class PasswordVerificationError(InvalidCredentialsError):
    """
    PasswordVerificationError class.
    """

    def __init__(self) -> None:
        """
        PasswordVerificationError constructor.
        """
        super().__init__(message="The provided password does not match the user's password.")
