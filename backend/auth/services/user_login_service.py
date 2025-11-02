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
    User login domain service.
    """

    __actions: UserActions
    __finder: UserFinderService

    def __init__(self, actions: UserActions, finder: UserFinderService) -> None:
        """
        UserLogin constructor.

        Args:
            actions (UserActions): User actions.
            finder (UserFinderService): User finder service.
        """
        self.__actions = actions
        self.__finder = finder

    def login(self, email: str, password: str) -> tuple[str, str]:
        """
        Login a user.

        Args:
            email (str): User email.
            password (str): User password.

        Raises:
            UserNotFoundError: If the provided email does not correspond to any user.
            PasswordVerificationError: If the provided password does not match with the user's password.

        Returns:
            tuple[str, str]: The access and refresh tokens.
        """
        users: list[User] = self.__finder.find(
            conditions=[Condition(
                field='email',
                operator=SQLOperation.EQUAL,
                value=email,
            )]
        )

        if not users:
            self.__avoid_timing_attack(password=password)
            raise UserNotFoundError(field='email', value=email)

        if not users[0].check_password(plain_password=password):
            raise PasswordVerificationError()

        return AccessToken().encode(user=users[0]), RefreshToken().encode(user=users[0])

    def __avoid_timing_attack(self, password: str) -> None:
        """
        This method is used to avoid timing attacks. This type of attack is where the attacker attempts to compromise a
        system by analyzing the time taken to execute cryptographic algorithms. In this case, we are using a dummy
        password hashing function, so even the user does not exist, the time taken to execute the hashing function will
        be the same.

        Args:
            password (str): User password.

        References:
            https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#authentication-and-error-messages
        """
        password_hashing(data=password)
