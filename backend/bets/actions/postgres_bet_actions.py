from typing import Any
from typing_extensions import override
from uuid import UUID

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
        Search bets.
        
        CRITICAL: No bet_participant table. Participants are in user_bets table.
        """
        query: str = """
            SELECT
                b.id,
                b.group_id,
                b.title,
                b.description,
                b.image_url,
                b.min_bet,
                b.deadline,
                b.status,
                b.created_by,
                b.created_at,
                b.updated_at
            FROM bet b
            WHERE 1=1
        """

        parameters: dict[str, Any] = {}

        for index, condition in enumerate(conditions):
            query += f" AND b.{condition.field} {condition.operator} %(param_{index})s"
            parameters[f"param_{index}"] = condition.value

        return self.__connection.search_all(query, parameters, Bet)

    @override
    def save(self, bet: Bet) -> None:
        """
        Save bet with new schema fields.
        
        CRITICAL: Include group_id, title, description, min_bet, deadline, created_by.
        """
        query: Composed = SQL("""
            INSERT INTO bet (
                id, group_id, title, description, image_url, 
                min_bet, deadline, status, created_by, 
                created_at, updated_at
            )
            VALUES (
                %(id)s, %(group_id)s, %(title)s, %(description)s, %(image_url)s,
                %(min_bet)s, %(deadline)s, %(status)s, %(created_by)s,
                %(created_at)s, %(updated_at)s
            )
        """)
        self.__connection.execute(query=query, parameters=bet.to_dict())

    @override
    def update(self, bet: Bet) -> None:
        """
        Update bet fields.
        """
        set_fragments: list[Composed] = []
        for key, value in bet.to_dict().items():
            if value is not None and key not in ("id",):
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
    def join_bet(self, bet_id: str | UUID, user_id: str | UUID, option_id: str | UUID) -> None:
        """
        Join bet by placing a user_bet.
        
        CRITICAL: 
        - No bet_participant table exists
        - Must insert into user_bets table
        - user_bets requires: bet_id, user_id, option_id, amount
        - Charge user's coins by bet.min_bet
        """
        # Get bet min_bet
        rows = self.__connection.search_all(
            """
            SELECT min_bet
            FROM bet
            WHERE id = %(bet_id)s
            """,
            {"bet_id": str(bet_id)},
            dict,
        )
        if not rows:
            raise ValueError("Bet not found")

        min_bet = int(rows[0]["min_bet"])

        # Charge user coins safely
        res = self.__connection.execute(
            query=SQL("""
                UPDATE "user"
                SET coins = coins - %(min_bet)s
                WHERE id = %(user_id)s AND coins >= %(min_bet)s
            """),
            parameters={"user_id": str(user_id), "min_bet": min_bet},
        )

        rowcount = getattr(res, "rowcount", None)
        if rowcount == 0:
            raise ValueError("Not enough coins or user not found")

        # Insert into user_bets with option_id
        self.__connection.execute(
            query=SQL("""
                INSERT INTO user_bets (bet_id, user_id, option_id, amount)
                VALUES (%(bet_id)s, %(user_id)s, %(option_id)s, %(amount)s)
                ON CONFLICT (bet_id, user_id) DO NOTHING
            """),
            parameters={
                "bet_id": str(bet_id),
                "user_id": str(user_id),
                "option_id": str(option_id),
                "amount": min_bet,
            },
        )

    @override
    def join_bet_in_group(self, group_id: str, bet_id: str, username: str) -> None:
        """
        Join bet in group (legacy method for compatibility).
        
        NOTE: This method signature uses username for backward compatibility.
        Internally converts username to user_id.
        In SQL v2.0, we should migrate to using user_id directly.
        """
        # First, get user_id from username
        user_rows = self.__connection.search_all(
            """
            SELECT id
            FROM "user"
            WHERE username = %(username)s
            """,
            {"username": username},
            dict,
        )
        if not user_rows:
            raise ValueError(f"User {username} not found")
        
        user_id = user_rows[0]["id"]

        # Verify bet belongs to group
        bet_rows = self.__connection.search_all(
            """
            SELECT id, min_bet
            FROM bet
            WHERE id = %(bet_id)s AND group_id = %(group_id)s
            """,
            {"bet_id": bet_id, "group_id": group_id},
            dict,
        )
        if not bet_rows:
            raise ValueError("Bet not found in this group")

        min_bet = int(bet_rows[0]["min_bet"])

        # Charge user coins safely
        res = self.__connection.execute(
            query=SQL("""
                UPDATE "user"
                SET coins = coins - %(min_bet)s
                WHERE id = %(user_id)s AND coins >= %(min_bet)s
            """),
            parameters={"user_id": str(user_id), "min_bet": min_bet},
        )

        rowcount = getattr(res, "rowcount", None)
        if rowcount == 0:
            raise ValueError("Not enough coins")

        # For this legacy method, we need to handle the case where option_id might not be provided
        # We'll use the first available option for the bet, or raise an error if none exist
        option_rows = self.__connection.search_all(
            """
            SELECT id
            FROM bet_options
            WHERE bet_id = %(bet_id)s
            LIMIT 1
            """,
            {"bet_id": bet_id},
            dict,
        )
        
        if not option_rows:
            raise ValueError("Bet has no options available")
        
        option_id = option_rows[0]["id"]

        # Insert into user_bets
        self.__connection.execute(
            query=SQL("""
                INSERT INTO user_bets (bet_id, user_id, option_id, amount)
                VALUES (%(bet_id)s, %(user_id)s, %(option_id)s, %(amount)s)
                ON CONFLICT (bet_id, user_id) DO NOTHING
            """),
            parameters={
                "bet_id": bet_id,
                "user_id": str(user_id),
                "option_id": str(option_id),
                "amount": min_bet,
            },
        )

    @override
    def leave_bet(self, bet_id: str, username: str) -> None:
        """
        Leave bet by removing user_bet.
        
        CRITICAL: Delete from user_bets table, not bet_participant.
        NOTE: Uses username for backward compatibility.
        """
        # Get user_id from username
        user_rows = self.__connection.search_all(
            """
            SELECT id
            FROM "user"
            WHERE username = %(username)s
            """,
            {"username": username},
            dict,
        )
        if not user_rows:
            raise ValueError(f"User {username} not found")
        
        user_id = user_rows[0]["id"]

        self.__connection.execute(
            query=SQL("""
                DELETE FROM user_bets
                WHERE bet_id = %(bet_id)s AND user_id = %(user_id)s
            """),
            parameters={"bet_id": bet_id, "user_id": str(user_id)},
        )

