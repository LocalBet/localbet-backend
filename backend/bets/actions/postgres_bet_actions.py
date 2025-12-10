from typing import Any
from typing_extensions import override
from psycopg.sql import SQL, Composed, Identifier, Placeholder

from backend.bets.actions.bet_actions import BetActions
from backend.shared.infrastructure.connections import PostgreSqlConnection
from backend.shared.models import Condition, DataModel, SQLOperation
from backend.bets.models import Bet


class PostgreSQLBetActions(BetActions):
    __connection: PostgreSqlConnection

    def __init__(self, connection: PostgreSqlConnection) -> None:
        self.__connection = connection

    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[Bet]:
        query: str = """
            SELECT id, user_id, coin_id, amount, status, name, create_date, update_date
            FROM bet
            WHERE 1=1
        """
        parameters: dict[str, Any] = {}
        for index, condition in enumerate(conditions):
            query += f" AND {condition.field} {condition.operator} %(param_{index})s"
            parameters[f"param_{index}"] = condition.value

        return self.__connection.search_all(query, parameters, Bet)

    @override
    def save(self, bet: Bet) -> None:
        query: Composed = SQL("""
            INSERT INTO bet (id, user_id, coin_id, amount, status, name, create_date, update_date)
            VALUES (%(id)s, %(user_id)s, %(coin_id)s, %(amount)s, %(status)s, %(name)s, %(create_date)s, %(update_date)s)
        """)
        self.__connection.execute(query=query, parameters=bet.to_dict())

    @override
    def update(self, bet: Bet) -> None:
        set_fragments: list[Composed] = []
        for key, value in bet.to_dict().items():
            if value is not None and key != "id":
                set_fragments.append(SQL("{} = {}").format(Identifier(key), Placeholder(key)))

        query: Composed = SQL("""
            UPDATE bet
            SET {set_clause}
            WHERE id = {id_placeholder}
        """).format(set_clause=SQL(", ").join(set_fragments), id_placeholder=Placeholder("id"))

        self.__connection.execute(query=query, parameters=bet.to_dict())

    @override
    def delete(self, bet: Bet) -> None:
        query: Composed = SQL("DELETE FROM bet WHERE id = %(id)s")
        self.__connection.execute(query=query, parameters=bet.to_dict())
