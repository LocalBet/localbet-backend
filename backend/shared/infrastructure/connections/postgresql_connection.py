"""
PostgreSQL connection module.
"""

from __future__ import annotations

from types import TracebackType
from typing import Any, Self, TypeVar

from psycopg import Connection, sql
from psycopg.sql import SQL, Composed

from backend.shared.infrastructure.errors import NoRowAffectedError
from backend.shared.models import DataModel

T = TypeVar("T", bound=DataModel)


class PostgreSqlConnection:
    """
    PostgreSQL connection class.
    """

    __connection: Connection

    def __init__(self, connection: Connection) -> None:
        """
        PostgreSQL connection constructor.

        Args:
            connection (Connection): PostgreSQL connection.
        """
        self.__connection = connection

    def __enter__(self) -> Self:
        """
        Enter the postgresql connection context.

        Returns:
            Self: The postgresql connection instance.
        """
        self.__connection.__enter__()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Exit the postgresql connection context.

        Args:
            exc_type (type[BaseException] | None): Exception type.
            exc_value (BaseException | None): Exception value.
            traceback (TracebackType | None): Traceback.
        """
        self.__connection.__exit__(exc_type, exc_value, traceback)

    def search_one(self, query: str, parameters: dict[str, Any], model: type[T]) -> T | None:
        """
        Execute a query and return the first result.

        Args:
            query (str): SQL query to execute.
            parameters (dict[str, Any]): Parameters to inject into the query (this is to prevent SQL injection).
            model (type[T]): Model to convert the result to.

        Returns:
            T | None: If the query returns a row, it will return the converted model, otherwise None.
        """
        result: dict[str, Any] | None = self.__connection.execute(sql.SQL(query), params=parameters).fetchone()  # type: ignore[assignment]

        if result is None:
            return None

        return model.from_dict(primitives=result)

    def search_all(self, query: str, parameters: dict[str, Any], model: type[T]) -> list[T]:
        """
        Execute a query and return all the results.

        Args:
            query (str): SQL query to execute.
            parameters (dict[str, Any]): Parameters to inject into the query (this is to prevent SQL injection).
            model (type[T]): Model to convert the result to.

        Returns:
            list[T]: List of models converted from the results.
        """
        result: list[dict[str, Any]] = self.__connection.execute(sql.SQL(query), params=parameters).fetchall()  # type: ignore[assignment]

        return [model.from_dict(primitives=primitives) for primitives in result]

    def execute(self, query: SQL | Composed, parameters: dict[str, Any]) -> None:
        """
        Execute a query with the given parameters.

        Args:
            query (SQL | Composed): SQL query to execute. It can be a raw SQL string or a composed SQL statement.
            parameters (dict[str, Any]): Parameters to inject into the query (this is to prevent SQL injection).

        Raises:
            NoRowAffectedError: If the query is an INSERT, UPDATE or DELETE and no row was affected.
        """
        result = self.__connection.execute(query=query, params=parameters)

        query_str = query.as_string(self.__connection)
        if query_str.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")) and result.rowcount == 0:
            raise NoRowAffectedError()
