"""
PostgreSQL GroupRoleType action.
"""

from typing import Any
from typing_extensions import override

from psycopg.errors import UniqueViolation
from psycopg.sql import SQL, Composed, Identifier, Placeholder

from backend.shared.infrastructure.connections import PostgreSqlConnection
from backend.shared.infrastructure.errors import NoRowAffectedError
from backend.shared.models import Condition, DataModel, SQLOperation
from backend.group_roles_type.actions.role_group_type_actions import GroupRoleTypeActions
from backend.group_roles_type.errors import GroupRoleTypeAlreadyExistsError, GroupRoleTypeNotFoundError
from backend.group_roles_type.models import GroupRoleType


class PostgreSQLGroupRoleTypeActions(GroupRoleTypeActions):
    """
    PostgreSQL GroupRoleType actions class.
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
    def search(self, conditions: list[Condition[DataModel]]) -> list[GroupRoleType]:
        """
        Search GroupRoleType in the action by conditions.

        Args:
        conditions (list[Condition]): Conditions to search for.

        Returns:
        list[User]: List of users.
        """
        # Base query
        query: str = """
        SELECT id, group_id, name, description, create_date, update_date
        FROM "group_role_type"
        WHERE 1=1
        """

        parameters: dict[str, Any] = {}

        for index, condition in enumerate(conditions):
            query += f" AND {condition.field} {condition.operator} %(param_{index})s"
            parameters[f"param_{index}"] = condition.value

        results = self.__connection.search_all(query, parameters, GroupRoleType)

        return results

    @override
    def update(self, group_role_type: GroupRoleType) -> None:
        """
        Update a GroupRoleType in the action using the safe, dynamically built query.

        Args:
        group_role_type (GroupRoleType): User to be updated.

        Raises:
            ValueError: If no valid fields are provided.
            GroupRoleTypeNotFoundError: If no User with the specified ID is found.
        """
        if not group_role_type.id:
            raise ValueError("GroupRoleType ID is mandatory and cannot be None.")

        users = self.search([Condition("id", SQLOperation.EQUAL, group_role_type.id)])
        if not users:
            raise GroupRoleTypeAlreadyExistsError(field="id", value=group_role_type.id)

        set_fragments: list[Composed] = []
        for key, value in group_role_type.to_dict().items():
            if value is not None and key != "id":
                set_fragments.append(SQL("{} = {}").format(Identifier(key), Placeholder(key)))

        if not set_fragments:
            raise ValueError("No valid fields to update were provided.")

        query: Composed = SQL(
            """
            UPDATE "group_role_type"
            SET {set_clause}
            WHERE id = {id_placeholder}
            """
        ).format(set_clause=SQL(", ").join(set_fragments), id_placeholder=Placeholder("id"))

        self.__connection.execute(query=query, parameters=group_role_type.to_dict())

    @override
    def save(self, group_role_type: GroupRoleType) -> None:
        """
        Create a GroupRoleType in the action.

        Args:
            group_role_type (GroupRoleType): GroupRoleType to be created.

        Raises:
            ValueError: If no valid fields are provided.
            GroupRoleTypeAlreadyExistsError: If the GroupRoleType already exists.
        """
        try:
            if not group_role_type.to_dict():
                raise ValueError("No valid fields to insert were provided.")

            query: Composed = SQL(
                    """
                    INSERT INTO "group_role_type" (
                    id, group_id, name, description, create_date, update_date
                    )
                    VALUES (
                    {id_placeholder}, {group_id_placeholder}, {name_placeholder}, {description_placeholder}, {create_date_placeholder},
                    {update_date_placeholder}
                    )
                    """
                ).format(
                    id_placeholder=Placeholder("id"),
                    group_id_placeholder=Placeholder("group_id"),
                    name_placeholder=Placeholder("name"),
                    description_placeholder=Placeholder("description"),
                    create_date_placeholder=Placeholder("create_date"),
                    update_date_placeholder=Placeholder("update_date"),
                )

            self.__connection.execute(query=query, parameters=group_role_type.to_dict())
        except UniqueViolation as exception:
            raise GroupRoleTypeAlreadyExistsError(field="name", value=group_role_type.name) from exception

    @override
    def delete(self, group_role_type: GroupRoleType) -> None:
        """
        Delete a GroupRoleType from the action.

        Args:
            group_role_type (GroupRoleType): User to delete.

        Raises:
            GroupRoleTypeNotFoundError: If the User is not found.
        """
        # TODO: Check if containe any user a role group member
        try:
            query: Composed = SQL(
                """
                DELETE FROM "group_role_type"
                WHERE id = {id_placeholder}
                """
            ).format(id_placeholder=Placeholder("id"))
            self.__connection.execute(query=query, parameters=group_role_type.to_dict())
        except NoRowAffectedError as exception:
            raise GroupRoleTypeNotFoundError(field="id", value=group_role_type.id) from exception
