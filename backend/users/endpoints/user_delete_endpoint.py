"""
User delete controller module.
"""

from fastapi import APIRouter, Request, status

from backend.auth.errors import PasswordVerificationError
from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.database import get_database_connection
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.errors import UserNotFoundError
from backend.users.schemas import UserDeleteSchema
from backend.users.services import UserDeleterService

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.delete(
    path="/",
    summary="User delete.",
    description="It allows to delete the logged user account.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "title": "Unauthorized",
                            "message": "The provided access token is invalid.",
                        },
                    }
                }
            },
        },
    },
)
async def user_delete(request: Request, delete_data: UserDeleteSchema) -> None:
    """
    It allows to delete the logged user account.

    Args:
        request (Request): The request that the user is making.
        delete_data (UserDeleteSchema): The user delete data.
    """
    try:
        with get_database_connection() as database_connection:
            psql_user_actions = PostgreSQLUserActions(connection=database_connection)
            deleter_service = UserDeleterService(action=psql_user_actions)

            logged_user = request.state.logged_user
            deleter_service.delete(user=logged_user, password=delete_data.password)

    except (UserNotFoundError, PasswordVerificationError) as exception:
        raise HTTPError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            title="Unauthorized",
            message="Invalid email or password.",
        ) from exception
