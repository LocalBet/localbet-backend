"""
Create a new bet.
"""

from fastapi import APIRouter, Request, status
from uuid import uuid4
from datetime import datetime
from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.shared.infrastructure import MiddlewareWrapper
from backend.bets.models import Bet
from backend.bets.schemas import BetCreateSchema, BetGetSchema
from backend.bets.services import BetCreatorService
from backend.bets.actions.postgres_bet_actions import PostgreSQLBetActions
from backend.database import get_database_connection
from backend.services.redis import redis_client   # <-- import Redis client

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))

@route.post(
    path="/",
    summary="Create a new bet.",
    description="Allows a logged user to create a bet.",
    response_model=BetGetSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_bet(request: Request, bet_data: BetCreateSchema) -> BetGetSchema:
    logged_user = request.state.logged_user

    with get_database_connection() as connection:
        bet_service = BetCreatorService(PostgreSQLBetActions(connection))
        now = datetime.utcnow()

        bet = Bet(
            id=uuid4(),
            group_id=bet_data.group_id,
            title=bet_data.title,
            description=bet_data.description,
            image_url=bet_data.image_url,
            min_bet=bet_data.min_bet,
            deadline=bet_data.deadline,
            status="active",
            created_by=logged_user.id,
            created_at=now,
            updated_at=now,
        )

        bet_service.create(bet)

        # Add bet to Redis ZSET for 24h tracking
        # Use created_at timestamp as score, and bet.id or bet.title as member
        timestamp = int(now.timestamp())
        await redis_client.zadd("new_bets", {str(bet.id): timestamp})

        return BetGetSchema(**bet.to_dict())
