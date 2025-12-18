from fastapi import APIRouter, status
from backend.stats.schemas.new_bets_response_schema import NewBetsResponseSchema
from backend.stats.services.new_bets_service import NewBetsService

route = APIRouter()

@route.get(
    path="/",
    summary="Get bets created in the last 24 hours",
    description="Returns bets added to Redis within the last 24 hours.",
    response_model=NewBetsResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_new_bets_last_24h() -> NewBetsResponseSchema:
    service = NewBetsService()
    bet_ids = await service.get_new_bets()
    return NewBetsResponseSchema(new_bets=bet_ids, count=len(bet_ids))
