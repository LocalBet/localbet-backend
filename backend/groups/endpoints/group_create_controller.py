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
            create_date=datetime.utcnow(),
            update_date=datetime.utcnow(),
            members=[logged_user.username],      # ✅ username
            admin_username=logged_user.username, # ✅ username
            bets=[],                              # ✅ nou camp
        )

        group_creator.create(group)

        data = group.to_dict()
        data.setdefault("bets", [])
        return GroupGetSchema(**data)
