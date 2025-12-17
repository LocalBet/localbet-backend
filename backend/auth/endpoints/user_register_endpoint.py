"""
User registration endpoint.
"""

from fastapi import APIRouter, status

from backend.auth.middlewares import UserMustNotBeLoggedMiddleware
from backend.auth.schemas import AccessTokenSchema, CreateUserSchema
from backend.auth.services import UserRegisterService
from backend.database import get_database_connection
from backend.shared.errors import ValidationError
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.errors import UserAlreadyExistsError

from backend.services.redis import redis_client
import time

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustNotBeLoggedMiddleware]))


@route.post(
    path="/signup",
    summary="User registration endpoint.",
    description="Register new user with profile and legal data, returns tokens for auto-login.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": AccessTokenSchema},
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "examples": {
                        "ValidationError": {
                            "summary": "Validation Error",
                            "value": {
                                "error": {
                                    "title": "ValidationError",
                                    "message": "Must be at least 18 years old",
                                }
                            },
                        },
                        "UserAlreadyExists": {
                            "summary": "User Already Exists",
                            "value": {
                                "error": {
                                    "title": "UserAlreadyExistsError",
                                    "message": "User with username/email already exists",
                                }
                            },
                        },
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
                            "message": "Cannot be authenticated to access this resource",
                        }
                    }
                }
            }
        },
    },
)
async def user_registration(registration_data: CreateUserSchema) -> AccessTokenSchema:
    """
    Register a new user with profile and legal compliance data.

    Args:
        registration_data (CreateUserSchema): Registration data.

    Returns:
        AccessTokenSchema: Access and refresh tokens for auto-login.
    """
    try:
        with get_database_connection() as database_connection:
            user_action = PostgreSQLUserActions(connection=database_connection)
            user_register_service = UserRegisterService(actions=user_action)

            access_token, refresh_token = user_register_service.register(
                username=registration_data.username,
                email=registration_data.email,
                password=registration_data.password,
                password_verification=registration_data.password_verification,
                full_name=registration_data.full_name,
                phone_number=registration_data.phone_number,
                birth_date=registration_data.birth_date,
                country=registration_data.country,
                accepted_terms=registration_data.accepted_terms,
                accepted_privacy_policy=registration_data.accepted_privacy_policy,
            )

    except (ValidationError, ValueError) as exception:
        raise HTTPError(
            status_code=status.HTTP_400_BAD_REQUEST,
            title=exception.__class__.__name__,
            message=str(exception) if isinstance(exception, ValueError) else exception.message,
        ) from exception

    except UserAlreadyExistsError as exception:
        raise HTTPError(
            status_code=status.HTTP_400_BAD_REQUEST,
            title=exception.__class__.__name__,
            message=exception.message,
        ) from exception

    now = int(time.time())
    await redis_client.zadd("new_users", {registration_data.username: now})

    return AccessTokenSchema(access_token=access_token, refresh_token=refresh_token)
