from fastapi import APIRouter, status
from backend.stats.schemas.system_stats_schema import SystemStatsSchema
from backend.stats.services.system_stats_service import SystemStatsService
from backend.stats.actions.system_stats_actions import SystemStatsActions

route = APIRouter()

@route.get(
    path="/",
    summary="Get system statistics",
    description="Returns CPU, RAM, disk usage, and temperatures.",
    response_model=SystemStatsSchema,
    status_code=status.HTTP_200_OK,
)
async def get_system_stats() -> SystemStatsSchema:
    service = SystemStatsService(SystemStatsActions())
    stats = await service.get_system_stats()
    return SystemStatsSchema(**stats)
