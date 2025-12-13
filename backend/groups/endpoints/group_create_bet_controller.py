from fastapi import APIRouter, Request, status, HTTPException
from uuid import uuid4, UUID
from datetime import datetime
from psycopg.sql import SQL

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.shared.infrastructure import MiddlewareWrapper
from backend.database import get_database_connection

from backend.groups.actions.postgres_group_actions import PostgreSQLGroupActions
from backend.bets.schemas import BetCreateSchema, BetGetSchema

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.post(
    path="/{group_id}/bets",
    summary="Create a bet inside a group (admin only).",
    description="Only the group admin can create bets inside that group.",
    response_model=BetGetSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_bet_in_group(request: Request, group_id: UUID, bet_data: BetCreateSchema) -> BetGetSchema:
    logged_user = request.state.logged_user
    now = datetime.utcnow()
    bet_id = uuid4()

    cost = float(bet_data.cost)

    with get_database_connection() as connection:
        group_actions = PostgreSQLGroupActions(connection)
        group = group_actions.get_by_id(group_id)

        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        if group.admin_username != logged_user.username:
            raise HTTPException(status_code=403, detail="Only the group admin can create bets")

        try:
            # 0) (Opcional però recomanat) comprova que l'admin és membre del grup
            # si no ho vols, pots eliminar aquest bloc
            is_member = connection.search_one(
                """
                SELECT 1
                FROM group_member
                WHERE group_id = %(group_id)s AND username = %(username)s
                """,
                {"group_id": str(group_id), "username": logged_user.username},
                dict,
            )
            if is_member is None:
                raise HTTPException(status_code=403, detail="Admin is not a member of this group")

            # 1) Cobrar coins al creador (SAFE)
            updated = connection.search_one(
                """
                UPDATE "user"
                SET coins = coins - %(cost)s
                WHERE username = %(username)s AND coins >= %(cost)s
                RETURNING coins
                """,
                {"username": logged_user.username, "cost": cost},
                dict,
            )
            if updated is None:
                raise HTTPException(status_code=400, detail="Not enough coins to create this bet")

            # 2) Crear bet amb amount inicial = cost
            connection.execute(
                query=SQL("""
                    INSERT INTO bet (id, user_id, cost, amount, status, name, create_date, update_date)
                    VALUES (%(id)s, %(user_id)s, %(cost)s, %(amount)s, %(status)s, %(name)s, %(create_date)s, %(update_date)s)
                """),
                parameters={
                    "id": str(bet_id),
                    "user_id": logged_user.username,
                    "cost": cost,
                    "amount": cost,        # ✅ amount comença sent el cost
                    "status": "open",
                    "name": bet_data.name,
                    "create_date": now,
                    "update_date": now,
                },
            )

            # 3) Link bet -> group
            connection.execute(
                query=SQL("""
                    INSERT INTO group_bet (group_id, bet_id)
                    VALUES (%(group_id)s, %(bet_id)s)
                    ON CONFLICT DO NOTHING
                """),
                parameters={"group_id": str(group_id), "bet_id": str(bet_id)},
            )

            # 4) Afegir creador com participant (així NO cal que faci join)
            connection.execute(
                query=SQL("""
                    INSERT INTO bet_participant (bet_id, username)
                    VALUES (%(bet_id)s, %(username)s)
                    ON CONFLICT DO NOTHING
                """),
                parameters={"bet_id": str(bet_id), "username": logged_user.username},
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating bet: {e}")

        return BetGetSchema(
            id=bet_id,
            user_id=logged_user.username,
            cost=cost,
            amount=cost,
            status="open",
            name=bet_data.name,
            create_date=now,
            update_date=now,
            participants=[logged_user.username],  # ✅ ara sí
        )
