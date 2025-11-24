"""
PostgreSQL Permission action.
"""

from typing import Any
from typing_extensions import override

from backend.shared.infrastructure.connections import PostgreSqlConnection
from backend.shared.models import Condition, DataModel
from backend.permissions.actions.permission_actions import PermissionActions
from backend.permissions.models import Permission


class PostgreSQLPermissionActions(PermissionActions):
    """
    PostgreSQL Permission actions class.
    """

    __connection: PostgreSqlConnection

    def __init__(self, connection: PostgreSqlConnection) -> None:
        """
        PostgreSQL User action constructor.

        Args:
        connection (PostgreSqlConnection): PostgreSQL connection.
        """
        self.__connection = connection

    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[Permission]:
        """
        Search Permissions in the action by conditions.

        Args:
        conditions (list[Condition]): Conditions to search for.

        Returns:
        list[Permission]: List of users.
        """
        # Base query
        query: str = """
        SELECT id, scope, action, resource,create_date, update_date
        FROM "Permission"
        WHERE 1=1
        """

        parameters: dict[str, Any] = {}

        for index, condition in enumerate(conditions):
            query += f" AND {condition.field} {condition.operator} %(param_{index})s"
            parameters[f"param_{index}"] = condition.value

        results = self.__connection.search_all(query, parameters, Permission)

        return results
