"""
List all bets for the logged user.
"""

from fastapi import APIRouter, Request, status
from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.shared.infrastructure import MiddlewareWrapper
from backend.bets.schemas import BetGetSchema
from backend.bets.services import BetFinderService
from backend.bets.actions.postgres_bet_actions import PostgreSQLBetActions
from backend.database import get_database_connection
from backend.shared.models import Condition, SQLOperation

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))

@route.get(
    path="/",
    summary="List all bets.",
    description="Fetch all bets in the system.",
    response_model=list[BetGetSchema],
    status_code=status.HTTP_200_OK,
)
async def list_bets(request: Request) -> list[BetGetSchema]:
    with get_database_connection() as connection:
        bet_finder = BetFinderService(PostgreSQLBetActions(connection))
        bets = bet_finder.find([])
        return [BetGetSchema(**bet.to_dict()) for bet in bets]

