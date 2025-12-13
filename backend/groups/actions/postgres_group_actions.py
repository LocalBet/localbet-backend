from typing import Any
from typing_extensions import override
from uuid import UUID

from psycopg.sql import SQL, Composed

from backend.groups.actions.group_actions import GroupActions
from backend.shared.infrastructure.connections import PostgreSqlConnection
from backend.shared.models import Condition, DataModel
from backend.groups.models import Group


class PostgreSQLGroupActions(GroupActions):
    __connection: PostgreSqlConnection

    def __init__(self, connection: PostgreSqlConnection) -> None:
        self.__connection = connection

    # -------- Helpers --------
    def __base_select(self) -> str:
        # Carrega grup + members + bet_ids en una sola query
        return """
            SELECT
                g.id,
                g.name,
                g.create_date,
                g.update_date,
                g.admin_username,
                COALESCE(
                    array_agg(DISTINCT gm.username) FILTER (WHERE gm.username IS NOT NULL),
                    '{}'
                ) AS members,
                COALESCE(
                    array_agg(DISTINCT gb.bet_id) FILTER (WHERE gb.bet_id IS NOT NULL),
                    '{}'
                ) AS bets
            FROM "group" g
            LEFT JOIN group_member gm ON gm.group_id = g.id
            LEFT JOIN group_bet gb ON gb.group_id = g.id
            WHERE 1=1
        """

    # -------- Required by GroupActions --------
    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[Group]:
        query = self.__base_select()
        parameters: dict[str, Any] = {}

        # IMPORTANT: assumeixo que condition.field ve amb noms segurs com:
        # "id", "name", "admin_username"
        for index, condition in enumerate(conditions):
            query += f' AND g.{condition.field} {condition.operator} %(param_{index})s'
            parameters[f"param_{index}"] = condition.value

        query += " GROUP BY g.id"
        return self.__connection.search_all(query, parameters, Group)

    @override
    def get_by_id(self, group_id: str | UUID) -> Group | None:
        query = self.__base_select() + """
            AND g.id = %(id)s
            GROUP BY g.id
        """
        rows = self.__connection.search_all(query, {"id": str(group_id)}, Group)
        return rows[0] if rows else None

    @override
    def get_all(self) -> list[Group]:
        query = self.__base_select() + """
            GROUP BY g.id
            ORDER BY g.create_date DESC
        """
        return self.__connection.search_all(query, {}, Group)

    @override
    def get_user_groups(self, username: str) -> list[Group]:
        # Filtra per membres: l’usuari ha d’estar a group_member
        query = """
            SELECT
                g.id,
                g.name,
                g.create_date,
                g.update_date,
                g.admin_username,
                COALESCE(
                    array_agg(DISTINCT gm2.username) FILTER (WHERE gm2.username IS NOT NULL),
                    '{}'
                ) AS members,
                COALESCE(
                    array_agg(DISTINCT gb.bet_id) FILTER (WHERE gb.bet_id IS NOT NULL),
                    '{}'
                ) AS bets
            FROM "group" g
            JOIN group_member gm ON gm.group_id = g.id AND gm.username = %(username)s
            LEFT JOIN group_member gm2 ON gm2.group_id = g.id
            LEFT JOIN group_bet gb ON gb.group_id = g.id
            GROUP BY g.id
            ORDER BY g.create_date DESC
        """
        return self.__connection.search_all(query, {"username": username}, Group)

    @override
    def save(self, group: Group) -> None:
        # 1) grup
        query_group: Composed = SQL("""
            INSERT INTO "group" (id, name, admin_username, create_date, update_date)
            VALUES (%(id)s, %(name)s, %(admin_username)s, %(create_date)s, %(update_date)s)
        """)
        self.__connection.execute(
            query=query_group,
            parameters={
                "id": group.id,
                "name": group.name,
                "admin_username": group.admin_username,
                "create_date": group.create_date,
                "update_date": group.update_date,
            },
        )

        # 2) members
        query_member: Composed = SQL("""
            INSERT INTO group_member (group_id, username)
            VALUES (%(group_id)s, %(username)s)
            ON CONFLICT DO NOTHING
        """)
        for username in group.members:
            self.__connection.execute(
                query=query_member,
                parameters={"group_id": group.id, "username": username},
            )

        # 3) bets (ids)
        query_bet: Composed = SQL("""
            INSERT INTO group_bet (group_id, bet_id)
            VALUES (%(group_id)s, %(bet_id)s)
            ON CONFLICT DO NOTHING
        """)
        for bet_id in group.bet_ids:
            self.__connection.execute(
                query=query_bet,
                parameters={"group_id": group.id, "bet_id": bet_id},
            )

    @override
    def update(self, group: Group) -> None:
        # 1) update base group fields
        query_update: Composed = SQL("""
            UPDATE "group"
            SET name = %(name)s,
                admin_username = %(admin_username)s,
                update_date = %(update_date)s
            WHERE id = %(id)s
        """)
        self.__connection.execute(
            query=query_update,
            parameters={
                "id": group.id,
                "name": group.name,
                "admin_username": group.admin_username,
                "update_date": group.update_date,
            },
        )

        # 2) replace members
        self.__connection.execute(
            query=SQL('DELETE FROM group_member WHERE group_id = %(group_id)s'),
            parameters={"group_id": group.id},
        )

        query_member: Composed = SQL("""
            INSERT INTO group_member (group_id, username)
            VALUES (%(group_id)s, %(username)s)
            ON CONFLICT DO NOTHING
        """)
        for username in group.members:
            self.__connection.execute(
                query=query_member,
                parameters={"group_id": group.id, "username": username},
            )

        # 3) replace bets
        self.__connection.execute(
            query=SQL('DELETE FROM group_bet WHERE group_id = %(group_id)s'),
            parameters={"group_id": group.id},
        )

        query_bet: Composed = SQL("""
            INSERT INTO group_bet (group_id, bet_id)
            VALUES (%(group_id)s, %(bet_id)s)
            ON CONFLICT DO NOTHING
        """)
        for bet_id in group.bet_ids:
            self.__connection.execute(
                query=query_bet,
                parameters={"group_id": group.id, "bet_id": bet_id},
            )

    @override
    def delete(self, group: Group) -> None:
        # Cascades eliminen group_member i group_bet
        query: Composed = SQL('DELETE FROM "group" WHERE id = %(id)s')
        self.__connection.execute(query=query, parameters={"id": group.id})

    
    def add_member(self, group_id: str | UUID, username: str) -> None:
        query = SQL("""
            INSERT INTO group_member (group_id, username)
            VALUES (%(group_id)s, %(username)s)
            ON CONFLICT DO NOTHING
        """)
        self.__connection.execute(
            query=query,
            parameters={"group_id": str(group_id), "username": username},
        )