"""
Register a new user service.
"""

from backend.users.actions import UserActions
from backend.users.errors import UserPasswordMismatchError
from backend.users.models import User


class UserRegisterService:
    """
    Register a new user service (simplified).
    """

    __actions: UserActions

    def __init__(self, actions: UserActions) -> None:
        """
        UserRegisterService constructor.

        Args:
            actions (UserActions): User actions.
        """
        self.__actions = actions

    def register(
        self,
        username: str,
        email: str,
        password: str,
        password_verification: str,
    ) -> User:
        """
        Register a new user.

        Args:
            username (str): User username.
            email (str): User email.
            password (str): User password.
            password_verification (str): User password verification.

        Raises:
            UserPasswordMismatchError: If the password and the password verification do not match.
            UserAlreadyExistsError: If user already exists.

        Returns:
            User: Created user.
        """
        self.__ensure_passwords_match(password=password, password_verification=password_verification)

        user = User(
            username=username,
            email=email,
            password=password,
        )

        self.__actions.save(user=user)
        return user

    def __ensure_passwords_match(self, password: str, password_verification: str) -> None:
        """
        Ensure that the password and the password verification match.
        """
        if password != password_verification:
            raise UserPasswordMismatchError()
