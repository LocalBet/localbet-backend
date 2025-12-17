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
    description="Retrieve a list of all groups in the system with member and bet counts.",
    response_model=list[GroupGetSchema],
    status_code=status.HTTP_200_OK,
)
async def list_groups(request: Request) -> list[GroupGetSchema]:
    with get_database_connection() as connection:
        # FIX: Create actions repository first, then pass to service
        actions = PostgreSQLGroupActions(connection)
        group_service = GroupService(actions)
        groups = group_service.get_all()

        result: list[GroupGetSchema] = []
        for group in groups:
            # Get domain model data
            data = group.to_dict()
            
            # Map field names: Domain model -> API Schema
            schema_data = {
                "id": data.get("id"),
                "name": data.get("name"),
                "description": data.get("description"),
                "is_active": data.get("is_active", True),
                "create_date": data.get("created_at"),  # Schema expects create_date
                "update_date": data.get("updated_at"),  # Schema expects update_date
                "member_count": len(group.members),
                "active_bets_count": len([b for b in group.bets if getattr(b, 'status', 'active') == 'active']),
                "members": data.get("members", []),
                "admin_username": str(data.get("creator_id", "")),  # Map creator_id to admin_username
                "bets": data.get("bets", []),
            }
            
            result.append(GroupGetSchema(**schema_data))

        return result
