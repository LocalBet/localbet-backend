"""
Get the current logged user account.
"""

from fastapi import APIRouter, Request, status

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.shared.infrastructure import MiddlewareWrapper
from backend.users.schemas import UserGetSchema

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.get(
    path="/",
    summary="Get the current logged user account.",
    description="It allows to get the current logged user account.",
    responses={
        status.HTTP_200_OK: {
            "model": UserGetSchema,
        },
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
async def get_user(request: Request) -> UserGetSchema:
    """
    It allows to get the current logged user account.

    Args:
        request (Request): The request that the user is making.

    Returns:
        UserGetSchema: The current logged user account.
    """
    logged_user = request.state.logged_user
    return UserGetSchema(**logged_user.to_dict())
