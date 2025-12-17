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
        self.__connection = connection

    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[User]:
        query: str = """
            SELECT 
                id, username, email, password, 
                full_name, phone_number, birth_date, country,
                coins, wins, losses, active_groups_count,
                accepted_terms, accepted_privacy_policy, legal_verified, verified_at,
                created_at, updated_at
            FROM "user"
            WHERE 1=1
        """

        parameters: dict[str, Any] = {}

        for index, condition in enumerate(conditions):
            # Dynamic WHERE clause construction
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
            raise UserNotFoundError(field='id', value=str(user.id))

        set_fragments: list[Composed] = []
        user_dict = user.to_dict()

        valid_update_fields = {
            'username', 'email', 'password', 'full_name', 'phone_number',
            'birth_date', 'country', 'coins', 'wins', 'losses',
            'active_groups_count', 'legal_verified', 'verified_at'
        }

        for key, value in user_dict.items():
            if value is not None and key in valid_update_fields:
                set_fragments.append(SQL('{} = {}').format(Identifier(key), Placeholder(key)))

        set_fragments.append(SQL("updated_at = CURRENT_TIMESTAMP"))

        query: Composed = SQL(
            """
            UPDATE "user"
            SET {set_clause}
            WHERE id = {id_placeholder}
            """
        ).format(set_clause=SQL(', ').join(set_fragments), id_placeholder=Placeholder('id'))

        self.__connection.execute(query=query, parameters=user_dict)

    @override
    def save(self, user: User) -> None:
        """
        Create a User in the DB with all profile and legal fields.
        """
        try:
            if not user.to_dict():
                raise ValueError('No valid fields to insert were provided.')

            # Insert with all new columns
            query: Composed = SQL(
                """
                INSERT INTO "user" (
                    id, username, email, password, 
                    full_name, phone_number, birth_date, country,
                    coins, wins, losses, active_groups_count, 
                    accepted_terms, accepted_privacy_policy, legal_verified, verified_at,
                    created_at, updated_at
                )
                VALUES (
                    {id}, {username}, {email}, {password}, 
                    {full_name}, {phone_number}, {birth_date}, {country},
                    {coins}, {wins}, {losses}, {active_groups_count},
                    {accepted_terms}, {accepted_privacy_policy}, {legal_verified}, {verified_at},
                    {created_at}, {updated_at}
                )
            """).format(
                id=Placeholder("id"),
                username=Placeholder("username"),
                email=Placeholder("email"),
                password=Placeholder("password"),
                full_name=Placeholder("full_name"),
                phone_number=Placeholder("phone_number"),
                birth_date=Placeholder("birth_date"),
                country=Placeholder("country"),
                coins=Placeholder("coins"),
                wins=Placeholder("wins"),
                losses=Placeholder("losses"),
                active_groups_count=Placeholder("active_groups_count"),
                accepted_terms=Placeholder("accepted_terms"),
                accepted_privacy_policy=Placeholder("accepted_privacy_policy"),
                legal_verified=Placeholder("legal_verified"),
                verified_at=Placeholder("verified_at"),
                created_at=Placeholder("created_at"),
                updated_at=Placeholder("updated_at")
            )

            params = user.to_dict()
            self.__connection.execute(query=query, parameters=params)

        except UniqueViolation as exception:
            msg = str(exception)
            field = 'email' if 'email' in msg else 'username'
            value = user.email if field == 'email' else user.username
            raise UserAlreadyExistsError(field=field, value=str(value)) from exception

    @override
    def delete(self, user: User) -> None:
        """
        Delete a User from the DB (by username).
        """
        try:
            query: Composed = SQL(
                """
                DELETE FROM "user"
                WHERE id = {id_placeholder}
            """).format(id_placeholder=Placeholder('id'))

            self.__connection.execute(query=query, parameters={'id': str(user.id)})

        except NoRowAffectedError as exception:
            raise UserNotFoundError(field='id', value=str(user.id)) from exception