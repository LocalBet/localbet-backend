"""
Get a bet by ID.
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
    path="/{bet_id}",
    summary="Get a bet by ID.",
    description="Fetch a bet belonging to the logged user.",
    responses={status.HTTP_200_OK: {"model": BetGetSchema}},
)
async def get_bet(request: Request, bet_id: str) -> BetGetSchema:
    with get_database_connection() as connection:
        bet_finder = BetFinderService(PostgreSQLBetActions(connection))
        bets = bet_finder.find([Condition("id", SQLOperation.EQUAL, bet_id)])
        bet = bets[0]
        return BetGetSchema(**bet.to_dict())
