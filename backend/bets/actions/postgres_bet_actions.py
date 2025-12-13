from typing import Any
from typing_extensions import override

from psycopg.sql import SQL, Composed, Identifier, Placeholder

from backend.bets.actions.bet_actions import BetActions
from backend.shared.infrastructure.connections import PostgreSqlConnection
from backend.shared.models import Condition, DataModel
from backend.bets.models import Bet


class PostgreSQLBetActions(BetActions):
    __connection: PostgreSqlConnection

    def __init__(self, connection: PostgreSqlConnection) -> None:
        self.__connection = connection

    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[Bet]:
        """
        Search bets and include:
        - cost
        - participants (array_agg of usernames)
        """
        query: str = """
            SELECT
                b.id,
                b.user_id,
                b.cost,
                b.status,
                b.name,
                b.create_date,
                b.update_date,
                COALESCE(array_agg(bp.username) FILTER (WHERE bp.username IS NOT NULL), '{}'::text[]) AS participants
            FROM bet b
            LEFT JOIN bet_participant bp ON bp.bet_id = b.id
            WHERE 1=1
        """

        parameters: dict[str, Any] = {}

        for index, condition in enumerate(conditions):
            query += f" AND b.{condition.field} {condition.operator} %(param_{index})s"
            parameters[f"param_{index}"] = condition.value

        query += """
            GROUP BY
                b.id, b.user_id, b.cost, b.status, b.name, b.create_date, b.update_date
        """

        return self.__connection.search_all(query, parameters, Bet)

    @override
    def save(self, bet: Bet) -> None:
        """
        Save bet (name + cost only).
        """
        query: Composed = SQL("""
            INSERT INTO bet (id, user_id, cost, status, name, create_date, update_date)
            VALUES (%(id)s, %(user_id)s, %(cost)s, %(status)s, %(name)s, %(create_date)s, %(update_date)s)
        """)
        self.__connection.execute(query=query, parameters=bet.to_dict())

    @override
    def update(self, bet: Bet) -> None:
        """
        Update bet (does not touch participants table).
        """
        set_fragments: list[Composed] = []
        for key, value in bet.to_dict().items():
            if value is not None and key not in ("id", "participants"):
                set_fragments.append(SQL("{} = {}").format(Identifier(key), Placeholder(key)))

        if not set_fragments:
            return

        query: Composed = SQL("""
            UPDATE bet
            SET {set_clause}
            WHERE id = {id_placeholder}
        """).format(
            set_clause=SQL(", ").join(set_fragments),
            id_placeholder=Placeholder("id"),
        )

        self.__connection.execute(query=query, parameters=bet.to_dict())

    @override
    def delete(self, bet: Bet) -> None:
        query: Composed = SQL("DELETE FROM bet WHERE id = %(id)s")
        self.__connection.execute(query=query, parameters=bet.to_dict())

    @override
    def join_bet(self, bet_id: str, username: str) -> None:
        """
        Join bet:
        - charge user's coins by bet.cost
        - insert bet_participant
        """
        rows = self.__connection.search_all(
            """
            SELECT cost
            FROM bet
            WHERE id = %(bet_id)s
            """,
            {"bet_id": bet_id},
            dict,
        )
        if not rows:
            raise ValueError("Bet not found")

        cost = float(rows[0]["cost"])

        # charge user coins safely
        res = self.__connection.execute(
            query=SQL("""
                UPDATE "user"
                SET coins = coins - %(cost)s
                WHERE username = %(username)s AND coins >= %(cost)s
            """),
            parameters={"username": username, "cost": cost},
        )

        rowcount = getattr(res, "rowcount", None)
        if rowcount == 0:
            raise ValueError("Not enough coins")

        # insert participant
        self.__connection.execute(
            query=SQL("""
                INSERT INTO bet_participant (bet_id, username)
                VALUES (%(bet_id)s, %(username)s)
                ON CONFLICT DO NOTHING
            """),
            parameters={"bet_id": bet_id, "username": username},
        )

    @override
    def leave_bet(self, bet_id: str, username: str) -> None:
        self.__connection.execute(
            query=SQL("""
                DELETE FROM bet_participant
                WHERE bet_id = %(bet_id)s AND username = %(username)s
            """),
            parameters={"bet_id": bet_id, "username": username},
        )
