
"""
User update controller module.
"""

from fastapi import APIRouter, Request, status

from backend.auth.errors import PasswordVerificationError
from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.database import get_database_connection
from backend.shared.errors import ValidationError
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.errors import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserPasswordMismatchError,
    UserUpdatePasswordError,
)
from backend.users.schemas import UserUpdateSchema
from backend.users.services import UserUpdateService

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.put(
    path='/',
    summary='User update.',
    description='It allows to update the logged user account.',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'content': {
                'application/json': {
                    'example': {
                        'error': {
                            'title': 'UserUsernameContainsInvalidCharactersError',
                            'message': 'UserUsername value <<<johndoe#>>> contains invalid characters. Only alphanumeric characters and underscores are allowed.',  # noqa: E501
                        }
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            'content': {
                'application/json': {
                    'example': {
                        'error': {
                            'title': 'Unauthorized',
                            'message': 'The provided access token is invalid.',
                        },
                    }
                }
            },
        },
    },
)
async def user_update(request: Request, update_data: UserUpdateSchema) -> None:
    """
    It allows to update the logged user account.

    Args:
        request (Request): The request that the user is making.
        update_data (UserUpdateSchema): The user update data.
    """
    try:
        with get_database_connection() as database_connection:
            user_action = PostgreSQLUserActions(connection=database_connection)
            updater_service = UserUpdateService(action=user_action)

            logged_user = request.state.logged_user
            updater_service.update(
                user=logged_user,
                name=update_data.name,
                username=update_data.username,
                email=update_data.email,
                role_id=update_data.role_id,
                old_password=update_data.old_password,
                new_password=update_data.new_password,
                new_password_confirmation=update_data.new_password_verification,
            )

    except (ValidationError, UserAlreadyExistsError, UserPasswordMismatchError, UserUpdatePasswordError) as exception:
        raise HTTPError(
            status_code=status.HTTP_400_BAD_REQUEST,
            title=exception.__class__.__name__,
            message=exception.message,
        ) from exception

    except (UserNotFoundError, PasswordVerificationError) as exception:
        raise HTTPError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            title='Unauthorized',
            message='Invalid email or password.',
        ) from exception
