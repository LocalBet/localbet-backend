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
    description="Retrieve a list of all groups in the system with member and bet counts.",
    response_model=list[GroupGetSchema],
    status_code=status.HTTP_200_OK,
)
async def list_groups(request: Request) -> list[GroupGetSchema]:
    with get_database_connection() as connection:
        group_service = GroupService(connection)
        groups = group_service.get_all()

        result: list[GroupGetSchema] = []
        for group in groups:
            data = group.to_dict()
            data.setdefault("bets", [])
            
            # MVP: Compute member_count and active_bets_count
            data["member_count"] = len(group.members)
            data["active_bets_count"] = len([b for b in group.bets if getattr(b, 'status', 'active') == 'active'])
            data.setdefault("description", None)
            data.setdefault("is_active", True)
            
            result.append(GroupGetSchema(**data))

        return result
