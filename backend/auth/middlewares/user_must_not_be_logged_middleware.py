
"""
This module contains the middleware that checks if the user is not logged in.
"""

from typing_extensions import override

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from backend.auth.errors import UserMustNotBeLoggedError
from backend.auth.models import AccessToken
from backend.database import get_database_connection
from backend.shared.models import Condition, DataModel, SQLOperation
from backend.users.actions import PostgreSQLUserActions
from backend.users.models import User
from backend.users.services import UserFinderService


class UserMustNotBeLoggedMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks if the user is not logged in.
    """

    __finder: UserFinderService

    def __init__(self, app: ASGIApp) -> None:
        """
        UserMustNotBeLoggedMiddleware constructor.

        Args:
            app (ASGIApp): The ASGI app to call.
        """
        super().__init__(app=app)

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Middleware that checks if the user is not logged in.

        Args:
            request (Request): The request that the user is making.
            call_next (RequestResponseEndpoint): The endpoint to call.

        Raises:
            UserMustNotBeLoggedError: If the user is logged in.
        """
        with get_database_connection() as database_connection:
            action = PostgreSQLUserActions(connection=database_connection)
            self.__finder = UserFinderService(action=action)

            access_token = request.headers.get('Authorization')
            if access_token is not None:
                access_token = access_token.replace('Bearer ', '')

            logged_user = self.__retrieve_user(access_token=access_token)
            if logged_user is not None:
                raise UserMustNotBeLoggedError()

            return await call_next(request)

    def __retrieve_user(self, access_token: str | None) -> User | None:
        """
        Retrieve the current logged user with the provided access token.

        Args:
            access_token (str | None): The current user access token.

        Returns:
            User | None: User if the token is valid and the user exists, None otherwise.
        """
        if access_token is None:
            return None

        try:
            user_id = AccessToken().decode(token=access_token).subject

        except Exception:
            return None

        conditions: list[Condition[DataModel]] = [Condition[DataModel](
                             field='id',
                            operator=SQLOperation.EQUAL,
                            value=user_id
                         )]

        users =  self.__finder.find(conditions=conditions)

        if users and len(users) > 1:
            raise UserMustNotBeLoggedError()
        elif users:
            return users[0]
        else:
            return None
