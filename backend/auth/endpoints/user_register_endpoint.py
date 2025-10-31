"""
User registration endpoint.
"""

from fastapi import APIRouter, status

from backend.auth.middlewares import UserMustNotBeLoggedMiddleware
from backend.auth.schemas import CreateUserSchema, UserCreatedSchema
from backend.auth.services import UserRegisterService
from backend.database import get_database_connection
from backend.shared.errors import ValidationError
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.errors import UserAlreadyExistsError

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustNotBeLoggedMiddleware]))


@route.post(
    path='/signup',
    summary='User registration endpoint.',
    description='It allows the registration of new users.',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'model': UserCreatedSchema,
        },
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
                            'message': 'Cannot be authenticated to access this resource',
                        },
                    }
                }
            },
        },
    },
)
async def user_registration(registration_data: CreateUserSchema) -> UserCreatedSchema:
    """
    It allows to register a new user.

    Args:
        registration_data (CreateUserSchema): Registration data.

    Returns:
        UserCreatedSchema: If the user is registered successfully.
    """
    try:
        with get_database_connection() as database_connection:
            user_action = PostgreSQLUserActions(connection=database_connection)
            user_register_service = UserRegisterService(actions=user_action)

            user_register_service.register(
                id=registration_data.id,
                name=registration_data.name,
                username=registration_data.username,
                role_id=registration_data.role_id,
                email=registration_data.email,
                password=registration_data.password,
                password_verification=registration_data.password_verification,
            )

    except ValidationError as exception:
        raise HTTPError(
            status_code=status.HTTP_400_BAD_REQUEST,
            title=exception.__class__.__name__,
            message=exception.message,
        ) from exception

    except UserAlreadyExistsError:
        pass

    return UserCreatedSchema()
