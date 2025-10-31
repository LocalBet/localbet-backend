"""
InvalidAccessTokenError module.
"""

from .invalid_credentials_error import InvalidCredentialsError


class InvalidAccessTokenError(InvalidCredentialsError):
    """
    InvalidAccessTokenError class.
    """

    def __init__(self) -> None:
        """
        InvalidAccessTokenError constructor.
        """
        super().__init__(message='The provided access token is invalid.')
