"""
Refresh user access token domain service.
"""

from backend.auth.errors import InvalidRefreshTokenError
from backend.auth.models import AccessToken, RefreshToken
from backend.shared.models import Condition, DataModel, SQLOperation
from backend.users.actions import UserActions
from backend.users.errors import UserNotFoundError
from backend.users.models import User
from backend.users.services import UserFinderService


class RefreshAccessTokenService:
    """
    Refresh user access token domain service.
    """

    __action: UserActions
    __user_finder: UserFinderService

    def __init__(self, action: UserActions, user_finder: UserFinderService) -> None:
        """
        RefreshAccessTokenService constructor.

        Args:
            action (UserActions): User action.
            user_finder (UserFinderService): User finder service.
        """
        self.__action = action
        self.__user_finder = user_finder

    def refresh(self, refresh_token: str) -> tuple[str, str]:
        """
        Refresh user access token with the provided refresh token.

        Args:
            refresh_token (str): User valid refresh token.

        Raises:
            InvalidRefreshTokenError: If the refresh token is invalid.

        Returns:
            tuple[str, str]: The new access token and refresh token.
        """
        try:
            username = RefreshToken().decode(token=refresh_token).subject
            user = self.__find_user(username=username)
            if not user:
                raise InvalidRefreshTokenError()

            return AccessToken().encode(user=user), refresh_token

        except Exception as exception:
            raise InvalidRefreshTokenError() from exception

    def __find_user(self, username: str) -> User | None:
        """
        Find user by id.

        Args:
            username (str): username.

        Raises:
            IdentifierError: If the username is invalid.
            UserNotFoundError: If the user is not found.

        Returns:
            User: The user. None if the user is not found.
        """
        conditions: list[Condition[DataModel]] = [
            Condition[DataModel](field="username", operator=SQLOperation.EQUAL, value=username)
        ]

        users: list[User] = self.__user_finder.find(conditions=conditions)
        if users and len(users) > 1:
            raise UserNotFoundError(field="username", value=username)
        elif users:
            return users[0]
        else:
            return None
