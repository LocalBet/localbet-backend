"""
Delete user domain service.
"""

from backend.auth.errors import PasswordVerificationError
from backend.users.actions import UserActions
from backend.users.models import User


class UserDeleterService:
    """
    Delete user domain service.
    """

    __action: UserActions

    def __init__(self, action: UserActions) -> None:
        """
        UserDeleter constructor.
        """
        self.__action = action

    def delete(self, user: User, password: str) -> None:
        """
        Delete a user.

        Args:
            user (User): User to delete.
            password (str): User password.

        Raises:
            PasswordVerificationError: If the user password and the provided password do not match.
            UserNotFoundError: If user was not found.
        """
        self.__ensure_user_password_matches(user=user, password=password)
        self.__action.delete(user=user)

    def __ensure_user_password_matches(self, user: User, password: str) -> None:
        """
        Ensure that the user password and the provided password match.

        Args:
            user (User): User.
            password (str): Password.

        Raises:
            PasswordVerificationError: If the user password and the provided password do not match.
        """
        if not user.check_password(plain_password=password):
            raise PasswordVerificationError()
