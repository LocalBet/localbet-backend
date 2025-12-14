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
            SELECT 
                username, email, password, coins,
                full_name, phone_number, birth_date, country,
                accepted_terms, accepted_privacy_policy, is_adult, verified_at,
                created_at, updated_at
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
        Create a User in the DB with all profile and legal fields.
        """
        try:
            query: Composed = SQL(
                """
                INSERT INTO "user" (id,
                                    username, email, password, coins,
                                    full_name, phone_number, birth_date, country,
                                    accepted_terms, accepted_privacy_policy, is_adult,
                                    created_at, updated_at)
                VALUES ({id},
                           {username}, {email}, {password}, {coins},
                           {full_name}, {phone_number}, {birth_date}, {country},
                           {accepted_terms}, {accepted_privacy_policy}, {is_adult},
                           {created_at}, {updated_at}
            )
            """
            ).format(
                id=Placeholder("id"),
                username=Placeholder("username"),
                email=Placeholder("email"),
                password=Placeholder("password"),
                coins=Placeholder("coins"),
                full_name=Placeholder("full_name"),
                phone_number=Placeholder("phone_number"),
                birth_date=Placeholder("birth_date"),
                country=Placeholder("country"),
                accepted_terms=Placeholder("accepted_terms"),
                accepted_privacy_policy=Placeholder("accepted_privacy_policy"),
                is_adult=Placeholder("is_adult"),
                created_at=Placeholder("created_at"),
                updated_at=Placeholder("updated_at"),
            )

            self.__connection.execute(query=query, parameters=user.to_dict())

        except UniqueViolation as exception:
            raise UserAlreadyExistsError(field="username/email", value=user.username) from exception

    @override
    def update(self, user: User) -> None:
        """
        Update a User in the DB using the primary key (id).
        """
        if not user.id:
            raise ValueError("User ID is mandatory and cannot be None.")

        users = self.search([Condition("id", SQLOperation.EQUAL, user.id)])
        if not users:
            raise UserNotFoundError(field="id", value=user.id)

        set_fragments: list[Composed] = []
        for key, value in user.to_dict().items():
            if value is not None and key != "id":
                set_fragments.append(
                    SQL("{} = {}").format(Identifier(key), Placeholder(key))
                )

        # Always update updated_at
        set_fragments.append(SQL("updated_at = NOW()"))

        if not set_fragments:
            return

        query: Composed = SQL(
            """
            UPDATE "user"
            SET {set_clause}
            WHERE id = {id_placeholder}
            """
        ).format(
            set_clause=SQL(", ").join(set_fragments),
            id_placeholder=Placeholder("id"),
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
