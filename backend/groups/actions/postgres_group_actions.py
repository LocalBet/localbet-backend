from typing import Any
from typing_extensions import override
from psycopg.sql import SQL, Composed, Identifier, Placeholder

from backend.groups.actions.group_actions import GroupActions
from backend.shared.infrastructure.connections import PostgreSqlConnection
from backend.shared.models import Condition, DataModel, SQLOperation
from backend.groups.models import Group


class PostgreSQLGroupActions(GroupActions):
    __connection: PostgreSqlConnection

    def __init__(self, connection: PostgreSqlConnection) -> None:
        self.__connection = connection

    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[Group]:
        query: str = """
            SELECT id, name, create_date, update_date, admin_id, members
            FROM groups
            WHERE 1=1
        """
        parameters: dict[str, Any] = {}
        for index, condition in enumerate(conditions):
            query += f" AND {condition.field} {condition.operator} %(param_{index})s"
            parameters[f"param_{index}"] = condition.value

        return self.__connection.search_all(query, parameters, Group)

    @override
    def save(self, group: Group) -> None:
        query: Composed = SQL("""
            INSERT INTO groups (id, name, create_date, update_date, admin_id, members)
            VALUES (%(id)s, %(name)s, %(create_date)s, %(update_date)s, %(admin_id)s, %(members)s)
        """)
        self.__connection.execute(query=query, parameters=group.to_dict())

    @override
    def update(self, group: Group) -> None:
        set_fragments: list[Composed] = []
        for key, value in group.to_dict().items():
            if value is not None and key != "id":
                set_fragments.append(SQL("{} = {}").format(Identifier(key), Placeholder(key)))

        query: Composed = SQL("""
            UPDATE groups
            SET {set_clause}
            WHERE id = {id_placeholder}
        """).format(set_clause=SQL(", ").join(set_fragments), id_placeholder=Placeholder("id"))

        self.__connection.execute(query=query, parameters=group.to_dict())

    @override
    def delete(self, group: Group) -> None:
        query: Composed = SQL("DELETE FROM groups WHERE id = %(id)s")
        self.__connection.execute(query=query, parameters=group.to_dict())
