"""
Refresh user access token controller.
"""

from fastapi import APIRouter, status

from backend.auth.errors import InvalidRefreshTokenError
from backend.auth.middlewares import UserMustNotBeLoggedMiddleware
from backend.auth.schemas import AccessTokenSchema, RefreshTokenSchema
from backend.auth.services import RefreshAccessTokenService
from backend.database import get_database_connection
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.services import UserFinderService

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustNotBeLoggedMiddleware]))


@route.post(
    path="/refresh",
    summary="Refresh user access token.",
    description="It allows to refresh the user access token with the refresh token.",
    responses={
        status.HTTP_200_OK: {
            "model": AccessTokenSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "title": "Unauthorized",
                            "message": "The provided refresh token is invalid.",
                        },
                    }
                }
            },
        },
    },
)
async def user_login(refresh_data: RefreshTokenSchema) -> AccessTokenSchema:
    """
    It allows to refresh the user access token with the refresh token.

    Args:
        refresh_data (RefreshTokenSchema): The refresh token data.

    Returns:
        AccessTokenSchema: New access token and the old refresh token.
    """
    try:
        with get_database_connection() as database_connection:
            user_action = PostgreSQLUserActions(connection=database_connection)
            user_finder_service = UserFinderService(action=user_action)
            refresh_token_service = RefreshAccessTokenService(
                action=user_action,
                user_finder=user_finder_service,
            )

            new_access_token, old_refresh_token = refresh_token_service.refresh(
                refresh_token=refresh_data.refresh_token
            )

    except InvalidRefreshTokenError as exception:
        raise HTTPError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            title="Unauthorized",
            message=exception.message,
        ) from exception

    return AccessTokenSchema(access_token=new_access_token, refresh_token=old_refresh_token)
