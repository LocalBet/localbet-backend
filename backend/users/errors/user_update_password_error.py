"""
UserUpdatePasswordError module.
"""

from backend.shared.errors import ValidationError


class UserUpdatePasswordError(ValidationError):
    """
    UserUpdatePasswordError class.
    """

    def __init__(self) -> None:
        """
        UserUpdatePasswordError constructor.
        """
        message = 'You must provide the old password, the new password and the new password verification to update the password.'  # noqa: E501 # fmt: skip
        super().__init__(message=message)
