from fastapi import APIRouter, Request, status, HTTPException
from uuid import UUID
from decimal import Decimal
from psycopg.sql import SQL

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.shared.infrastructure import MiddlewareWrapper
from backend.database import get_database_connection
from backend.bets.schemas.bet_resolve_schema import BetResolveSchema

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.post(
    path="/{group_id}/bets/{bet_id}/resolve",
    summary="Resolve a bet (creator only).",
    description="Creator selects winners among participants and amount is split equally.",
    status_code=status.HTTP_200_OK,
)
async def resolve_bet_in_group(
    request: Request,
    group_id: UUID,
    bet_id: UUID,
    payload: BetResolveSchema,
) -> dict:
    logged_user = request.state.logged_user

    # winners únics (evita duplicats)
    winners = list(dict.fromkeys(payload.winners))
    if not winners:
        raise HTTPException(status_code=400, detail="Winners list cannot be empty")

    with get_database_connection() as connection:
        # 1) Bet existeix i està dins del grup + obtenim creator, amount, status
        bet_row = connection.search_one(
            """
            SELECT b.id, b.user_id, b.amount, b.status
            FROM bet b
            JOIN group_bet gb ON gb.bet_id = b.id
            WHERE b.id = %(bet_id)s AND gb.group_id = %(group_id)s
            """,
            {"bet_id": str(bet_id), "group_id": str(group_id)},
            dict,
        )
        if bet_row is None:
            raise HTTPException(status_code=404, detail="Bet not found in this group")

        creator_username = bet_row["user_id"]
        status_str = bet_row["status"]
        amount = Decimal(str(bet_row["amount"]))

        # 2) Només creator pot resoldre
        if creator_username != logged_user.username:
            raise HTTPException(status_code=403, detail="Only the bet creator can resolve this bet")

        # 3) No permetre resoldre dues vegades
        if status_str != "open":
            raise HTTPException(status_code=409, detail=f"Bet is not open (current status: {status_str})")

        if amount <= 0:
            raise HTTPException(status_code=400, detail="Bet amount is 0, nothing to distribute")

        # 4) Validar winners ⟂ participants
        participant_rows = connection.search_all(
            """
            SELECT username
            FROM bet_participant
            WHERE bet_id = %(bet_id)s
            """,
            {"bet_id": str(bet_id)},
            dict,
        )
        participants = {r["username"] for r in participant_rows}

        not_participants = [u for u in winners if u not in participants]
        if not_participants:
            raise HTTPException(status_code=400, detail=f"These winners are not participants: {not_participants}")

        # 5) payout
        payout = amount / Decimal(len(winners))

        # 6) pagar guanyadors
        for w in winners:
            connection.execute(
                query=SQL("""
                    UPDATE "user"
                    SET coins = coins + %(payout)s
                    WHERE username = %(username)s
                """),
                parameters={"payout": payout, "username": w},
            )

        # 7) marcar bet com resolved (i opcionalment deixar amount a 0)
        connection.execute(
            query=SQL("""
                UPDATE bet
                SET status = 'resolved',
                    amount = 0,
                    update_date = NOW()
                WHERE id = %(bet_id)s
            """),
            parameters={"bet_id": str(bet_id)},
        )

    return {
        "ok": True,
        "group_id": str(group_id),
        "bet_id": str(bet_id),
        "resolved_by": logged_user.username,
        "winners": winners,
        "payout_per_winner": float(payout),
    }
