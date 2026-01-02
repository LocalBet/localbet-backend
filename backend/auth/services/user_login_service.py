"""
User login domain service.
"""

from backend.auth.errors import PasswordVerificationError
from backend.auth.models import AccessToken, RefreshToken
from backend.shared.models import Condition, SQLOperation
from backend.shared.utils import password_hashing
from backend.users.actions import UserActions
from backend.users.errors import UserNotFoundError
from backend.users.models import User
from backend.users.services import UserFinderService


class UserLoginService:
    """
    User login domain service (simplified).
    """

    __actions: UserActions
    __user_finder: UserFinderService

    def __init__(self, actions: UserActions, finder: UserFinderService) -> None:
        self.__actions = actions
        self.__user_finder = finder

    def login(self, username: str, password: str) -> tuple[str, str]:
        """
        Login a user by username or email.

        Args:
            username (str): User username or email.
            password (str): User password.

        Raises:
            UserNotFoundError: If the provided username/email does not correspond to any user.
            PasswordVerificationError: If the provided password does not match with the user's password.

        Returns:
            tuple[str, str]: The access and refresh tokens.
        """
        # Try to find by username first
        try:
            users: list[User] = self.__user_finder.find(
                conditions=[
                    Condition(
                        field="username",
                        operator=SQLOperation.EQUAL,
                        value=username,
                    )
                ]
            )
        except UserNotFoundError:
            # If not found by username, try by email
            try:
                users: list[User] = self.__user_finder.find(
                    conditions=[
                        Condition(
                            field="email",
                            operator=SQLOperation.EQUAL,
                            value=username,
                        )
                    ]
                )
            except UserNotFoundError:
                # User not found by username or email
                self.__avoid_timing_attack(password=password)
                raise UserNotFoundError(field="username/email", value=username)

        if not users[0].check_password(plain_password=password):
            raise PasswordVerificationError()

        return AccessToken().encode(user=users[0]), RefreshToken().encode(user=users[0])

    def __avoid_timing_attack(self, password: str) -> None:
        """
        Avoid timing attacks by doing a dummy hash even if user doesn't exist.
        """
        password_hashing(data=password)
