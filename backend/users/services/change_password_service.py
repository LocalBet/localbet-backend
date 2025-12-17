"""
Change user password service.
"""

from backend.users.actions import UserActions
from backend.users.errors import UserPasswordMismatchError
from backend.users.models import User


class ChangePasswordService:
    """
    Service for changing user password.
    """

    __actions: UserActions

    def __init__(self, actions: UserActions) -> None:
        """
        ChangePasswordService constructor.

        Args:
            actions (UserActions): User actions.
        """
        self.__actions = actions

    def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
    ) -> None:
        """
        Change user password after verifying current password.

        Args:
            user (User): The user whose password will be changed.
            current_password (str): Current password for verification.
            new_password (str): New password to set.

        Raises:
            UserPasswordMismatchError: If current password is incorrect.
        """
        # Verify current password
        if not user.check_password(current_password):
            raise UserPasswordMismatchError()

        # Set new password (will be hashed by User model setter)
        user.password = new_password

        # Save updated user
        self.__actions.update(user=user)
