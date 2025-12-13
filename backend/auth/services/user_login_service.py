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
        Login a user.

        Args:
            username (str): User username.
            password (str): User password.

        Raises:
            UserNotFoundError: If the provided username does not correspond to any user.
            PasswordVerificationError: If the provided password does not match with the user's password.

        Returns:
            tuple[str, str]: The access and refresh tokens.
        """
        users: list[User] = self.__user_finder.find(
            conditions=[
                Condition(
                    field="username",
                    operator=SQLOperation.EQUAL,
                    value=username,
                )
            ]
        )

        if not users:
            self.__avoid_timing_attack(password=password)
            raise UserNotFoundError(field="username", value=username)

        if not users[0].check_password(plain_password=password):
            raise PasswordVerificationError()

        # ⚠️ Si els tokens esperen user.id o role_id, això petarà.
        # Si passa, m'envies AccessToken/RefreshToken i ho adapto perquè usi user.username.
        return AccessToken().encode(user=users[0]), RefreshToken().encode(user=users[0])

    def __avoid_timing_attack(self, password: str) -> None:
        """
        Avoid timing attacks by doing a dummy hash even if user doesn't exist.
        """
        password_hashing(data=password)
