"""
Update user service.
"""

from datetime import UTC, datetime
from uuid import UUID

from backend.auth.errors import PasswordVerificationError
from backend.users.actions import UserActions
from backend.users.errors import UserPasswordMismatchError, UserUpdatePasswordError
from backend.users.models import User


class UserUpdateService:
    """
    Update user domain service.
    """

    __action: UserActions

    def __init__(self, action: UserActions) -> None:
        """
        User update service constructor.

        Args:
            action (UserActions): User action.
        """
        self.__action = action

    def update(
        self,
        user: User,
        username: str | None = None,
        email: str | None = None,
        name: str | None = None,
        role_id: str | UUID | None = None,
        old_password: str | None = None,
        new_password: str | None = None,
        new_password_confirmation: str | None = None,
    ) -> None:
        """
        Update user. The parameters with the same value or None will not be updated.

        Args:
            user (User): User to update.
            username (str | None): New username.
            email (str | None): New email.
            name (str | None): New name.
            role_id (str | UUID | None): New role ID.
            old_password (str | None): Old password.
            new_password (str | None): New password.
            new_password_confirmation (str | None): New password confirmation.

        Raises:
            UserNotFoundError: If user is not found.
        """
        if self.__check_if_user_wants_to_update_password(
            old_password=old_password,
            new_password=new_password,
            new_password_confirmation=new_password_confirmation,
        ):
            self.__ensure_passwords_match(password=new_password, password_verification=new_password_confirmation)  # type: ignore[arg-type]
            self.__ensure_user_password_matches(user=user, password=old_password)  # type: ignore[arg-type]
        server_hash = hash(user)

        if username is not None:
            user.username = username

        if email is not None:
            user.email = email

        if name is not None:
            user.name = name

        if new_password is not None:  # noqa: SIM102
            if not user.check_password(plain_password=new_password):
                user.password = new_password

        if role_id is not None:
            self.__ensure_role_id_exists(
                role_id=role_id
            )  # TODO: Use the finder service of Role when it is implemented and raise RoleNotFoundError if not found
            user.role_id = role_id

        if hash(user) == server_hash:
            return

        user.update_date = datetime.now(UTC)
        self.__action.update(user=user)

    def __check_if_user_wants_to_update_password(
        self,
        old_password: str | None,
        new_password: str | None,
        new_password_confirmation: str | None,
    ) -> bool:
        """
        Check if the user wants to update the password.

        Args:
            old_password (str, optional): Old user password. Defaults to None.
            new_password (str, optional): New user password. Defaults to None.
            new_password_confirmation (str, optional): New user password verification. Defaults to None.

        Raises:
            UserUpdatePasswordError: If some of the password fields are None.

        Returns:
            bool: True if the user wants to update the password, otherwise False.
        """
        if old_password is not None and new_password is not None and new_password_confirmation is not None:
            return True

        if old_password is None and new_password is None and new_password_confirmation is None:
            return False

        raise UserUpdatePasswordError()

    def __ensure_user_password_matches(self, user: User, password: str) -> None:
        """
        Ensure that the user password and the provided password match.

        Args:
            user (User): User.
            password (str): Provided password.

        Raises:
            PasswordVerificationError: If the user password and the provided password do not match.
        """
        if not user.check_password(plain_password=password):
            raise PasswordVerificationError()

    def __ensure_passwords_match(self, password: str, password_verification: str) -> None:
        """
        Ensure that the password and the password verification match.

        Args:
            password (str): Password.
            password_verification (str): Password verification.

        Raises:
            UserPasswordMismatchError: If the password and the password verification do not match.
        """
        if password != password_verification:
            raise UserPasswordMismatchError()

    def __ensure_role_id_exists(self, role_id: str | UUID) -> bool:
        """
        Ensure that the role ID exists.

        Args:
            role_id (str | UUID): Role ID.

        Raises:
            RoleNotFoundError: If the role ID does not exist.
        """
        return True
