"""
Register a new user service.
"""

from datetime import UTC, datetime
from uuid import UUID

from backend.users.actions import UserActions
from backend.users.errors import UserPasswordMismatchError
from backend.users.models import User
from backend.users.services import UserFinderService


class UserRegisterService:
    """
    Register a new user service.
    """

    __actions: UserActions
    __user_finder: UserFinderService

    def __init__(self, actions: UserActions) -> None:
        """
        UserRegistrar constructor.

        Args:
            actions (UserActions): User actions.
        """
        self.__actions = actions

    def register(
        self,
        id: str | UUID,
        name: str,
        username: str,
        email: str,
        role_id: str | UUID,
        password: str,
        password_verification: str,
    ) -> User:
        """
        Register a new user.

        Args:
            id (str | UUID): User id.
            name (str): User name.
            username (str): User username.
            email (str): User email.
            role_id (str | UUID): User role ID.
            password (str): User password.
            password_verification (str): User password verification.

        Raises:
            UserPasswordMismatchError: If the password and the password verification do not match.
            UserAlreadyExistsError: If user already exists.

        Returns:
            User: Created user.
        """
        self.__ensure_passwords_match(password=password, password_verification=password_verification)
        self.__ensure_role_id_exists(
            role_id=role_id
        )  # TODO: Use the finder service of Role when it is implemented and raise RoleNotFoundError if not found

        user = User(
            id=id,
            name=name,
            username=username,
            email=email,
            password=password,
            role_id=role_id,
            create_date=datetime.now(UTC),
            update_date=datetime.now(UTC),
        )
        self.__actions.save(user=user)

        return user

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
