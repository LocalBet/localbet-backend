"""
Get a list of all groups.
"""

from fastapi import APIRouter, Request, status
from backend.groups.services import GroupService
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
    """
    List all groups.

    Args:
        request (Request): The request object.

    Returns:
        List[GroupGetSchema]: A list of groups.
    """
    with get_database_connection() as connection:
        group_service = GroupService(connection)  # Assuming the GroupService is connected to the database
        groups = group_service.get_all()  # Get all groups (you will need to implement this in the service)
        return [GroupGetSchema(**group.to_dict()) for group in groups]
