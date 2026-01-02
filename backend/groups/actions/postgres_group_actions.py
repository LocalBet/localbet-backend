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
        """
        Load group + members (UUIDs) + bets via JOINs.
        
        CRITICAL: No group_bet table exists in SQL v2.0.
        - Members: JOIN group_member (user_id UUID)
        - Bets: JOIN bet WHERE bet.group_id = group.id
        """
        return """
            SELECT
                g.id,
                g.name,
                g.description,
                g.creator_id,
                g.is_active,
                g.created_at,
                g.updated_at,
                COALESCE(
                    array_agg(DISTINCT gm.user_id) FILTER (WHERE gm.user_id IS NOT NULL),
                    '{}'
                ) AS members,
                COALESCE(
                    array_agg(DISTINCT b.id) FILTER (WHERE b.id IS NOT NULL),
                    '{}'
                ) AS hydrated_bets
            FROM "group" g
            LEFT JOIN group_member gm ON gm.group_id = g.id
            LEFT JOIN bet b ON b.group_id = g.id
            WHERE 1=1
        """

    # -------- Required by GroupActions --------
    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[Group]:
        query = self.__base_select()
        parameters: dict[str, Any] = {}

        # condition.field should be safe like: "id", "name", "creator_id"
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
            ORDER BY g.created_at DESC
        """
        return self.__connection.search_all(query, {}, Group)

    @override
    def get_user_groups(self, user_id: str | UUID) -> list[Group]:
        """
        Get all groups where user is a member.
        
        CRITICAL: Use user_id (UUID) instead of username.
        """
        query = """
            SELECT
                g.id,
                g.name,
                g.description,
                g.creator_id,
                g.is_active,
                g.created_at,
                g.updated_at,
                COALESCE(
                    array_agg(DISTINCT gm2.user_id) FILTER (WHERE gm2.user_id IS NOT NULL),
                    '{}'
                ) AS members,
                COALESCE(
                    array_agg(DISTINCT b.id) FILTER (WHERE b.id IS NOT NULL),
                    '{}'
                ) AS bets
            FROM "group" g
            JOIN group_member gm ON gm.group_id = g.id AND gm.user_id = %(user_id)s
            LEFT JOIN group_member gm2 ON gm2.group_id = g.id
            LEFT JOIN bet b ON b.group_id = g.id
            GROUP BY g.id
            ORDER BY g.created_at DESC
        """
        return self.__connection.search_all(query, {"user_id": str(user_id)}, Group)

    @override
    def save(self, group: Group) -> None:
        """
        Save group to DB.
        
        CRITICAL: Use creator_id (UUID) instead of admin_username.
        Members are NOT stored in group table (use add_member separately).
        """
        query_group: Composed = SQL("""
            INSERT INTO "group" (id, name, description, creator_id, is_active, created_at, updated_at)
            VALUES (%(id)s, %(name)s, %(description)s, %(creator_id)s, %(is_active)s, %(created_at)s, %(updated_at)s)
        """)
        self.__connection.execute(
            query=query_group,
            parameters={
                "id": group.id,
                "name": group.name,
                "description": group.description,
                "creator_id": str(group.creator_id),
                "is_active": group.is_active,
                "created_at": group.created_at,
                "updated_at": group.updated_at,
            },
        )

        # Add members if provided
        if group.members:
            query_member: Composed = SQL("""
                INSERT INTO group_member (group_id, user_id)
                VALUES (%(group_id)s, %(user_id)s)
                ON CONFLICT DO NOTHING
            """)
            for user_id in group.members:
                self.__connection.execute(
                    query=query_member,
                    parameters={"group_id": str(group.id), "user_id": str(user_id)},
                )

    @override
    def update(self, group: Group) -> None:
        """
        Update group fields.
        
        CRITICAL: Use creator_id instead of admin_username.
        Members are managed separately via add_member/remove_member.
        """
        query_update: Composed = SQL("""
            UPDATE "group"
            SET name = %(name)s,
                description = %(description)s,
                creator_id = %(creator_id)s,
                is_active = %(is_active)s,
                updated_at = %(updated_at)s
            WHERE id = %(id)s
        """)
        self.__connection.execute(
            query=query_update,
            parameters={
                "id": str(group.id),
                "name": group.name,
                "description": group.description,
                "creator_id": str(group.creator_id),
                "is_active": group.is_active,
                "updated_at": group.updated_at,
            },
        )

        # Replace members if provided
        if group.members is not None:
            self.__connection.execute(
                query=SQL('DELETE FROM group_member WHERE group_id = %(group_id)s'),
                parameters={"group_id": str(group.id)},
            )

            query_member: Composed = SQL("""
                INSERT INTO group_member (group_id, user_id)
                VALUES (%(group_id)s, %(user_id)s)
                ON CONFLICT DO NOTHING
            """)
            for user_id in group.members:
                self.__connection.execute(
                    query=query_member,
                    parameters={"group_id": str(group.id), "user_id": str(user_id)},
                )

    @override
    def delete(self, group: Group) -> None:
        """
        Delete group (cascades to group_member and bets).
        """
        query: Composed = SQL('DELETE FROM "group" WHERE id = %(id)s')
        self.__connection.execute(query=query, parameters={"id": str(group.id)})

    
    def add_member(self, group_id: str | UUID, user_id: str | UUID) -> None:
        """
        Add member to group.
        
        CRITICAL: Use user_id (UUID) instead of username.
        """
        query = SQL("""
            INSERT INTO group_member (group_id, user_id)
            VALUES (%(group_id)s, %(user_id)s)
            ON CONFLICT DO NOTHING
        """)
        self.__connection.execute(
            query=query,
            parameters={"group_id": str(group_id), "user_id": str(user_id)},
        )