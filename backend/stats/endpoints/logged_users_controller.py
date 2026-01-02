from fastapi import APIRouter, status
from backend.stats.schemas.logged_users_response_schema import LoggedUsersResponseSchema
from backend.stats.services.logged_users_service import LoggedUsersService

route = APIRouter()

@route.get(
    path="/",
    summary="Get currently logged users",
    description="Returns users with active tokens in Redis.",
    response_model=LoggedUsersResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_logged_users() -> LoggedUsersResponseSchema:
    service = LoggedUsersService()
    user_ids = await service.get_logged_users()
    return LoggedUsersResponseSchema(logged_users=user_ids, count=len(user_ids))
