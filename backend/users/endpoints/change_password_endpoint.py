"""
Change password endpoint.
"""

from fastapi import APIRouter, Request, status

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.database import get_database_connection
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.errors import UserPasswordMismatchError
from backend.users.schemas import ChangePasswordSchema
from backend.users.services import ChangePasswordService

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.put(
    path="/password",
    summary="Change user password.",
    description="Change the password of the currently logged-in user.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Password changed successfully."
        },
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "title": "UserPasswordMismatchError",
                            "message": "Current password is incorrect.",
                        }
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "title": "Unauthorized",
                            "message": "The provided access token is invalid.",
                        }
                    }
                }
            }
        },
    },
)
async def change_password(request: Request, password_data: ChangePasswordSchema) -> None:
    """
    Change the password of the currently logged-in user.

    Args:
        request (Request): The request containing the logged user.
        password_data (ChangePasswordSchema): Current and new password data.

    Raises:
        HTTPError: If current password is incorrect.
    """
    logged_user = request.state.logged_user

    try:
        with get_database_connection() as database_connection:
            user_actions = PostgreSQLUserActions(connection=database_connection)
            change_password_service = ChangePasswordService(actions=user_actions)

            change_password_service.change_password(
                user=logged_user,
                current_password=password_data.current_password,
                new_password=password_data.new_password,
            )

    except UserPasswordMismatchError as exception:
        raise HTTPError(
            status_code=status.HTTP_400_BAD_REQUEST,
            title=exception.__class__.__name__,
            message="Current password is incorrect.",
        ) from exception
