"""
Group Roles type get
"""

from fastapi import APIRouter, status, Request

from backend.auth.middlewares import UserMustNotBeLoggedMiddleware
from backend.auth.schemas import CreateUserSchema, UserCreatedSchema
from backend.auth.services import UserRegisterService
from backend.database import get_database_connection
from backend.shared.errors import ValidationError
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.errors import UserAlreadyExistsError
from backend.group_roles_type.schemas import GroupRoleTypeGetSchema

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustNotBeLoggedMiddleware]))
# TODO: Make endpoints from with ID/name argument.
# Returns number of users of users at complet or something
# Maybe if had the permissions (admin/moderator) to consult it then return the permissions of the group role
@route.get(
    path='/get',
    summary="Get Group roles types",
    description="It allow the get the group roles types",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": GroupRoleTypeGetSchema,
        },
    }
)
async def get_group_roles_types(request: Request) -> GroupRoleTypeGetSchema:
    """
    It allows to get the group role type
    """
    pass