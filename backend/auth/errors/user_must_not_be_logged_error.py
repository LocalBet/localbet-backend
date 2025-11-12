"""
UserMustNotBeLoggedError module.
"""

from .invalid_credentials_error import InvalidCredentialsError


class UserMustNotBeLoggedError(InvalidCredentialsError):
    """
    UserMustNotBeLoggedError class.
    """

    def __init__(self) -> None:
        """
        UserMustNotBeLoggedError constructor.
        """
        super().__init__(message="Cannot be authenticated to access this resource.")
