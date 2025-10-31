"""
UserMustBeLoggedError module.
"""

from .invalid_credentials_error import InvalidCredentialsError


class UserMustBeLoggedError(InvalidCredentialsError):
    """
    UserMustBeLoggedError class.
    """

    def __init__(self) -> None:
        """
        UserMustBeLoggedError constructor.
        """
        super().__init__(message='Authentication is required to access this resource.')
