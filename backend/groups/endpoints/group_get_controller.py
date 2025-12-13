"""
Get a group by its ID.
"""

from fastapi import APIRouter, Request, status
from backend.groups.services import GroupService
from backend.groups.schemas import GroupGetSchema
from backend.database import get_database_connection

route = APIRouter()


@route.get(
    path="/{group_id}",
    summary="Get a specific group by its ID.",
    description="Retrieve a group by its unique ID.",
    response_model=GroupGetSchema,
    status_code=status.HTTP_200_OK,
)
async def get_group(request: Request, group_id: str) -> GroupGetSchema:
    with get_database_connection() as connection:
        group_service = GroupService(connection)
        group = group_service.get_by_id(group_id)

        data = group.to_dict()
        data.setdefault("bets", [])
        return GroupGetSchema(**data)
