from fastapi import APIRouter, Request, status
from uuid import uuid4
from datetime import datetime

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.shared.infrastructure import MiddlewareWrapper

from backend.groups.models import Group
from backend.groups.schemas import GroupCreateSchema, GroupGetSchema
from backend.groups.services import GroupCreatorService
from backend.groups.actions.postgres_group_actions import PostgreSQLGroupActions
from backend.database import get_database_connection

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.post(
    path="/",
    summary="Create a new group.",
    description="Allows a logged user to create a new group.",
    response_model=GroupGetSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(request: Request, group_data: GroupCreateSchema) -> GroupGetSchema:
    logged_user = request.state.logged_user

    with get_database_connection() as connection:
        group_creator = GroupCreatorService(PostgreSQLGroupActions(connection))

        group = Group(
            id=uuid4(),
            name=group_data.name,
            description=group_data.description,
            creator_id=logged_user.id,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        group_creator.create(group)
        return GroupGetSchema(**group.to_dict())