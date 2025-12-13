"""
Login controller.
"""

from fastapi import APIRouter, status

from backend.auth.errors import PasswordVerificationError
from backend.auth.middlewares import UserMustNotBeLoggedMiddleware
from backend.auth.schemas import AccessTokenSchema, LoginSchema
from backend.auth.services import UserLoginService
from backend.database import get_database_connection
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.errors import UserNotFoundError
from backend.users.services import UserFinderService

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustNotBeLoggedMiddleware]))


@route.post(
    path="/login",
    summary="User login endpoint.",
    description=(
        "Authenticate an user by verifying their email and password. If the credentials are valid, the API returns an"
        "access and a refresh token for further authentication."
    ),
    responses={
        status.HTTP_200_OK: {
            "model": AccessTokenSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "examples": {
                        "InvalidCredentials": {
                            "summary": "Invalid Credentials",
                            "description": "Unauthorized access due to invalid credentials.",
                            "value": {
                                "error": {
                                    "title": "Unauthorized",
                                    "message": "Invalid email or password.",
                                },
                            },
                        },
                        "AlreadyAuthenticated": {
                            "summary": "Already Authenticated",
                            "description": "Unauthorized access due to the user is already authenticated.",
                            "value": {
                                "error": {
                                    "title": "Unauthorized",
                                    "message": "Cannot be authenticated to access this resource.",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def user_login(login_data: LoginSchema) -> AccessTokenSchema:
    """
    Authenticate a user by verifying their email and password. If the credentials are valid, the API returns an access
    token and a refresh token for further authentication.

    Args:
        login_data (LoginSchema): The login data.

    Returns:
        AccessTokenSchema: Access token and refresh token.
    """
    try:
        with get_database_connection() as database_connection:
            user_action = PostgreSQLUserActions(connection=database_connection)
            user_searcher_service = UserFinderService(action=user_action)
            login_service = UserLoginService(actions=user_action, finder=user_searcher_service)

            access_token, refresh_token = login_service.login(username=login_data.username,
                                                              password=login_data.password)

    except (UserNotFoundError, PasswordVerificationError) as exception:
        raise HTTPError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            title="Unauthorized",
            message="Invalid email or password.",
        ) from exception

    return AccessTokenSchema(access_token=access_token, refresh_token=refresh_token)
