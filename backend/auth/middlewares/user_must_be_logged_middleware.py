"""
This module contains the middleware that checks if the user is logged in.
"""

from typing_extensions import override

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from backend.auth.errors import InvalidAccessTokenError, UserMustBeLoggedError
from backend.auth.models import AccessToken
from backend.database import get_database_connection
from backend.shared.models import Condition, DataModel, SQLOperation
from backend.users.actions import PostgreSQLUserActions
from backend.users.models import User
from backend.users.services import UserFinderService


class UserMustBeLoggedMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks if the user is logged in.
    """

    __finder: UserFinderService

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app=app)

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        with get_database_connection() as database_connection:
            action = PostgreSQLUserActions(connection=database_connection)
            self.__finder = UserFinderService(action=action)

            access_token = request.headers.get("Authorization")
            if access_token is not None:
                access_token = access_token.replace("Bearer ", "")

            logged_user = self.__retrieve_user(access_token=access_token)
            if logged_user is None:
                raise UserMustBeLoggedError()

            request.state.logged_user = logged_user
            return await call_next(request)

    def __retrieve_user(self, access_token: str | None) -> User | None:
        if access_token is None:
            return None

        try:
            # ✅ Ara subject = username (text)
            username = AccessToken().decode(token=access_token).subject
        except Exception as exception:
            raise InvalidAccessTokenError() from exception

        # ✅ Abans buscava per id; ara per username
        conditions: list[Condition[DataModel]] = [
            Condition[DataModel](field="username", operator=SQLOperation.EQUAL, value=username)
        ]

        users = self.__finder.find(conditions=conditions)

        if users and len(users) > 1:
            raise UserMustBeLoggedError()
        elif users:
            return users[0]
        else:
            return None
