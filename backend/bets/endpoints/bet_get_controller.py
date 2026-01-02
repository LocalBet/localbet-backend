"""
Get a bet by ID.
"""

from fastapi import APIRouter, Request, status, HTTPException
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
    description="Fetch a bet by ID.",
    responses={status.HTTP_200_OK: {"model": BetGetSchema}},
)
async def get_bet(request: Request, bet_id: str) -> BetGetSchema:
    with get_database_connection() as connection:
        bet_finder = BetFinderService(PostgreSQLBetActions(connection))
        bets = bet_finder.find([Condition("id", SQLOperation.EQUAL, bet_id)])

        if not bets:
            raise HTTPException(status_code=404, detail="Bet not found")

        bet = bets[0]

        data = bet.to_dict()

        # ✅ per no petar amb el nou schema
        data.setdefault("participants", [])
        # si encara no tens cost al model/to_dict, evita error (millor que el model ja el retorni)
        data.setdefault("cost", 0)

        return BetGetSchema(**data)
