from fastapi import APIRouter, Request, status, HTTPException
from uuid import UUID

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.shared.infrastructure import MiddlewareWrapper
from backend.groups.schemas import GroupGetSchema
from backend.groups.actions.postgres_group_actions import PostgreSQLGroupActions
from backend.database import get_database_connection

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.post(
    path="/{group_id}/join",
    summary="Join an existing group.",
    description="Adds the logged-in user as a member of the group.",
    response_model=GroupGetSchema,
    status_code=status.HTTP_200_OK,
)
async def join_group(request: Request, group_id: UUID) -> GroupGetSchema:
    logged_user = request.state.logged_user

    with get_database_connection() as connection:
        actions = PostgreSQLGroupActions(connection)

        group = actions.get_by_id(group_id)
        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        actions.add_member(group_id=group_id, username=logged_user.username)

        # Tornem a carregar el group per veure members actualitzat
        updated = actions.get_by_id(group_id)
        data = updated.to_dict()
        data.setdefault("bets", [])
        return GroupGetSchema(**data)
