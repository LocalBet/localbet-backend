"""
Get all groups a user belongs to.
"""

from fastapi import APIRouter, Request, status
from backend.groups.services import GroupService
from backend.groups.schemas import GroupGetSchema
from backend.database import get_database_connection

route = APIRouter()

@route.get(
    path="/user/{user_id}",
    summary="Get all groups a user belongs to.",
    description="Retrieve all the groups that a specific user is part of.",
    response_model=list[GroupGetSchema],
    status_code=status.HTTP_200_OK,
)
async def get_user_groups(request: Request, user_id: str) -> list[GroupGetSchema]:
    """
    Get all groups a user belongs to.

    Args:
        request (Request): The request object.
        user_id (str): The ID of the user.

    Returns:
        List[GroupGetSchema]: A list of groups the user is part of.
    """
    with get_database_connection() as connection:
        group_service = GroupService(connection)  # Assuming the GroupService is connected to the database
        groups = group_service.get_user_groups(user_id)  # Get all groups the user is part of (you will need to implement this)
        return [GroupGetSchema(**group.to_dict()) for group in groups]
