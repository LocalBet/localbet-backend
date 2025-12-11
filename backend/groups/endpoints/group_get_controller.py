"""
Get a group by its ID.
"""

from fastapi import APIRouter, Request, status
from backend.groups.services import GroupService
from backend.groups.models import Group
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
    """
    Get a group by its ID.

    Args:
        request (Request): The request object.
        group_id (str): The ID of the group to retrieve.

    Returns:
        GroupGetSchema: The group data.
    """
    with get_database_connection() as connection:
        group_service = GroupService(connection)  # Assuming the GroupService is connected to the database
        group = group_service.get_by_id(group_id)  # Get the group by ID (you will need to implement this in the service)
        return GroupGetSchema(**group.to_dict())
