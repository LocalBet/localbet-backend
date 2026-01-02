"""
Get a list of all groups.
"""

from fastapi import APIRouter, Request, status
from backend.groups.services import GroupService
from backend.groups.actions.postgres_group_actions import PostgreSQLGroupActions
from backend.groups.schemas import GroupGetSchema
from backend.database import get_database_connection

route = APIRouter()


@route.get(
    path="/",
    summary="Get a list of all groups.",
    description="Retrieve a list of all groups in the system.",
    response_model=list[GroupGetSchema],
    status_code=status.HTTP_200_OK,
)
async def list_groups(request: Request) -> list[GroupGetSchema]:
    with get_database_connection() as connection:
        actions = PostgreSQLGroupActions(connection)
        group_service = GroupService(actions)
        groups = group_service.get_all()

        result: list[GroupGetSchema] = []
        for group in groups:
            data = group.to_dict()
            result.append(GroupGetSchema(**data))

        return result
