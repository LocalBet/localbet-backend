"""
PostgreSQL User action.
"""

from typing import Any
from typing_extensions import override

from psycopg.errors import UniqueViolation
from psycopg.sql import SQL, Composed, Identifier, Placeholder

from backend.shared.infrastructure.connections import PostgreSqlConnection
from backend.shared.infrastructure.errors import NoRowAffectedError
from backend.shared.models import Condition, DataModel
from backend.users.actions.user_actions import UserActions
from backend.users.errors import UserAlreadyExistsError, UserNotFoundError
from backend.users.models import User


class PostgreSQLUserActions(UserActions):
    """
    PostgreSQL User actions class.
    Works with: username, email, password, coins.
    """

    __connection: PostgreSqlConnection

    def __init__(self, connection: PostgreSqlConnection) -> None:
        self.__connection = connection

    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[User]:
        query: str = """
            SELECT username, email, password, coins
            FROM "user"
            WHERE 1=1
        """

        parameters: dict[str, Any] = {}

        for index, condition in enumerate(conditions):
            query += f" AND {condition.field} {condition.operator} %(param_{index})s"
            parameters[f"param_{index}"] = condition.value

        return self.__connection.search_all(query, parameters, User)

    @override
    def save(self, user: User) -> None:
        """
        Create a User in the DB.

        IMPORTANT:
        - We explicitly insert 'coins' to ensure consistency.
        - This allows the application to control the initial value.
        """
        try:
            query: Composed = SQL(
                """
                INSERT INTO "user" (username, email, password, coins)
                VALUES ({username_placeholder}, {email_placeholder}, {password_placeholder}, {coins_placeholder})
                """
            ).format(
                username_placeholder=Placeholder("username"),
                email_placeholder=Placeholder("email"),
                password_placeholder=Placeholder("password"),
                coins_placeholder=Placeholder("coins"),
            )

            self.__connection.execute(query=query, parameters=user.to_dict())

        except UniqueViolation as exception:
            raise UserAlreadyExistsError(field="username/email", value=user.username) from exception

    @override
    def update(self, user: User) -> None:
        """
        Update a User in the DB (by username).

        Note:
        - If user.to_dict() includes 'coins', it can be updated here
          (useful for spending coins when creating bets).
        """
        if not user.username:
            raise ValueError("Username is mandatory and cannot be None.")

        users = self.search([Condition("username", "=", user.username)])
        if not users:
            raise UserNotFoundError(field="username", value=user.username)

        set_fragments: list[Composed] = []
        for key, value in user.to_dict().items():
            if value is not None and key != "username":
                set_fragments.append(SQL("{} = {}").format(Identifier(key), Placeholder(key)))

        if not set_fragments:
            return

        query: Composed = SQL(
            """
            UPDATE "user"
            SET {set_clause}
            WHERE username = {username_placeholder}
            """
        ).format(
            set_clause=SQL(", ").join(set_fragments),
            username_placeholder=Placeholder("username"),
        )

        self.__connection.execute(query=query, parameters=user.to_dict())

    @override
    def delete(self, user: User) -> None:
        """
        Delete a User from the DB (by username).
        """
        try:
            query: Composed = SQL(
                """
                DELETE FROM "user"
                WHERE username = {username_placeholder}
                """
            ).format(username_placeholder=Placeholder("username"))

            self.__connection.execute(query=query, parameters=user.to_dict())

        except NoRowAffectedError as exception:
            raise UserNotFoundError(field="username", value=user.username) from exception
