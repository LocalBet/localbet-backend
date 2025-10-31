"""
PostgreSQL User action.
"""

from typing import Any
from typing_extensions import override

from psycopg.errors import UniqueViolation
from psycopg.sql import SQL, Composed, Identifier, Placeholder

from backend.shared.infrastructure.connections import PostgreSqlConnection
from backend.shared.infrastructure.errors import NoRowAffectedError
from backend.shared.models import Condition, DataModel, SQLOperation
from backend.users.actions.user_actions import UserActions
from backend.users.errors import UserAlreadyExistsError, UserNotFoundError
from backend.users.models import User


class PostgreSQLUserActions(UserActions):
    """
    PostgreSQL User actions class.
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
    def search(self, conditions: list[Condition[DataModel]]) -> list[User]:
        """
        Search Users in the action by conditions.

        Args:
            conditions (list[Condition]): Conditions to search for.

        Returns:
            list[User]: List of users.
        """
        # Base query
        query: str = """
            SELECT id, name, username, email, password, role_id, create_date, update_date
            FROM "user"
            WHERE 1=1
        """

        parameters: dict[str, Any] = {}

        for index, condition in enumerate(conditions):
            query += f' AND {condition.field} {condition.operator} %(param_{index})s'
            parameters[f'param_{index}'] = condition.value

        results = self.__connection.search_all(query, parameters, User)

        return results

    @override
    def update(self, user: User) -> None:
        """
        Update a User in the action using the safe, dynamically built query.

        Args:
            user (User): User to be updated.

        Raises:
            ValueError: If no valid fields are provided.
            UserNotFoundError: If no User with the specified ID is found.
        """
        if not user.id:
            raise ValueError('User ID is mandatory and cannot be None.')

        users = self.search([Condition('id', SQLOperation.EQUAL, user.id)])
        if not users:
            raise UserNotFoundError(field='id', value=user.id)

        set_fragments: list[Composed] = []
        for key, value in user.to_dict().items():
            if value is not None and key != 'id':
                set_fragments.append(SQL('{} = {}').format(Identifier(key), Placeholder(key)))

        if not set_fragments:
            raise ValueError('No valid fields to update were provided.')

        query: Composed = SQL(
            """
            UPDATE "user"
            SET {set_clause}
            WHERE id = {id_placeholder}
            """
        ).format(set_clause=SQL(', ').join(set_fragments), id_placeholder=Placeholder('id'))

        self.__connection.execute(query=query, parameters=user.to_dict())

    @override
    def save(self, user: User) -> None:
        """
        Create a User in the action.

        Args:
            user (User): User to be created.

        Raises:
            ValueError: If no valid fields are provided.
            UserAlreadyExistsError: If the User already exists.
        """
        try:
            if not user.to_dict():
                raise ValueError('No valid fields to insert were provided.')

            query: Composed = SQL("""
                INSERT INTO "user" (
                    id, name, username, email, password, role_id, create_date, update_date
                )
                VALUES (
                    {id_placeholder}, {name_placeholder}, {username_placeholder},
                    {email_placeholder}, {password_placeholder}, {role_id_placeholder}, {create_date_placeholder},
                    {update_date_placeholder}
                )
            """).format(
                id_placeholder=Placeholder('id'),
                name_placeholder=Placeholder('name'),
                username_placeholder=Placeholder('username'),
                email_placeholder=Placeholder('email'),
                password_placeholder=Placeholder('password'),
                role_id_placeholder=Placeholder('role_id'),
                create_date_placeholder=Placeholder('create_date'),
                update_date_placeholder=Placeholder('update_date'),
            )

            self.__connection.execute(query=query, parameters=user.to_dict())
        except UniqueViolation as exception:
            raise UserAlreadyExistsError(field='username', value=user.username) from exception

    @override
    def delete(self, user: User) -> None:
        """
        Delete a User from the action.

        Args:
            user (User): User to delete.

        Raises:
            UserNotFoundError: If the User is not found.
        """
        try:
            query: Composed = SQL("""
                DELETE FROM "user"
                WHERE id = {id_placeholder}
            """).format(id_placeholder=Placeholder('id'))
            self.__connection.execute(query=query, parameters=user.to_dict())
        except NoRowAffectedError as exception:
            raise UserNotFoundError(field='id', value=user.id) from exception
