"""
InvalidRefreshTokenError module.
"""

from .invalid_credentials_error import InvalidCredentialsError


class InvalidRefreshTokenError(InvalidCredentialsError):
    """
    InvalidRefreshTokenError class.
    """

    def __init__(self) -> None:
        """
        InvalidRefreshTokenError constructor.
        """
        super().__init__(message="The provided refresh token is invalid.")
