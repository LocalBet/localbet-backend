from fastapi import APIRouter, status
from backend.stats.schemas.new_users_response_schema import NewUsersResponseSchema
from backend.stats.services.new_users_service import NewUsersService

route = APIRouter()

@route.get(
    path="/",
    summary="Get users registered in the last 24 hours",
    description="Returns users added to Redis within the last 24 hours.",
    response_model=NewUsersResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_new_users_last_24h() -> NewUsersResponseSchema:
    service = NewUsersService()
    user_ids = await service.get_new_users()
    return NewUsersResponseSchema(new_users=user_ids, count=len(user_ids))
