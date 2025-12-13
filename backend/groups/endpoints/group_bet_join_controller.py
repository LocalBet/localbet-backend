from fastapi import APIRouter, Request, status, HTTPException
from uuid import UUID
from psycopg.sql import SQL

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.shared.infrastructure import MiddlewareWrapper
from backend.database import get_database_connection

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.post(
    path="/{group_id}/bets/{bet_id}/join",
    summary="Join a bet inside a group (pays cost and increases amount).",
    status_code=status.HTTP_200_OK,
)
async def join_bet_in_group(request: Request, group_id: UUID, bet_id: UUID) -> dict:
    logged_user = request.state.logged_user

    with get_database_connection() as connection:
        # 1) comprovar que la bet existeix i pertany a aquest grup + obtenir cost
        bet_rows = connection.search_all(
            """
            SELECT b.id, b.cost
            FROM bet b
            JOIN group_bet gb ON gb.bet_id = b.id
            WHERE b.id = %(bet_id)s AND gb.group_id = %(group_id)s
            """,
            {"bet_id": str(bet_id), "group_id": str(group_id)},
            dict,
        )
        if not bet_rows:
            raise HTTPException(status_code=404, detail="Bet not found in this group")

        cost = float(bet_rows[0]["cost"])

        # 2) evitar doble-join (si ja és participant)
        already = connection.search_all(
            """
            SELECT 1
            FROM bet_participant
            WHERE bet_id = %(bet_id)s AND username = %(username)s
            """,
            {"bet_id": str(bet_id), "username": logged_user.username},
            dict,
        )
        if already:
            raise HTTPException(status_code=409, detail="User already joined this bet")

        # 3) cobrar coins
        res = connection.execute(
            query=SQL("""
                UPDATE "user"
                SET coins = coins - %(cost)s
                WHERE username = %(username)s AND coins >= %(cost)s
            """),
            parameters={"username": logged_user.username, "cost": cost},
        )
        rowcount = getattr(res, "rowcount", None)
        if rowcount == 0:
            raise HTTPException(status_code=400, detail="Not enough coins to join this bet")

        # 4) inserir participant
        connection.execute(
            query=SQL("""
                INSERT INTO bet_participant (bet_id, username)
                VALUES (%(bet_id)s, %(username)s)
            """),
            parameters={"bet_id": str(bet_id), "username": logged_user.username},
        )

        # 5) sumar amount += cost
        connection.execute(
            query=SQL("""
                UPDATE bet
                SET amount = amount + %(cost)s,
                    update_date = NOW()
                WHERE id = %(bet_id)s
            """),
            parameters={"bet_id": str(bet_id), "cost": cost},
        )

    return {
        "ok": True,
        "group_id": str(group_id),
        "bet_id": str(bet_id),
        "username": logged_user.username,
        "charged_cost": cost,
    }
