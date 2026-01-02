"""
PostgreSQL connection module.
"""

from __future__ import annotations

from types import TracebackType
from typing import Any, Self, TypeVar, overload, Literal

from psycopg import Connection, sql
from psycopg.sql import SQL, Composed

from backend.shared.infrastructure.errors import NoRowAffectedError
from backend.shared.models.data_model import DataModel

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

    # ---------- SEARCH ONE ----------

    @overload
    def search_one(self, query: str, parameters: dict[str, Any], model: type[T]) -> T | None: ...
    @overload
    def search_one(self, query: str, parameters: dict[str, Any], model: type[dict]) -> dict[str, Any] | None: ...

    def search_one(self, query: str, parameters: dict[str, Any], model: type[Any]) -> Any | None:
        """
        Execute a query and return the first result.

        If model is a DataModel -> returns model instance.
        If model is dict -> returns primitives dict.
        """
        result: dict[str, Any] | None = self.__connection.execute(sql.SQL(query), params=parameters).fetchone()  # type: ignore[assignment]

        if result is None:
            return None

        # ✅ Allow returning raw primitives
        if model is dict:
            return result

        return model.from_dict(primitives=result)

    # ---------- SEARCH ALL ----------

    @overload
    def search_all(self, query: str, parameters: dict[str, Any], model: type[T]) -> list[T]: ...
    @overload
    def search_all(self, query: str, parameters: dict[str, Any], model: type[dict]) -> list[dict[str, Any]]: ...

    def search_all(self, query: str, parameters: dict[str, Any], model: type[Any]) -> list[Any]:
        """
        Execute a query and return all the results.

        If model is a DataModel -> returns list[model].
        If model is dict -> returns list[dict] primitives.
        """
        result: list[dict[str, Any]] = self.__connection.execute(sql.SQL(query), params=parameters).fetchall()  # type: ignore[assignment]

        # ✅ Allow returning raw primitives
        if model is dict:
            return result

        return [model.from_dict(primitives=primitives) for primitives in result]

    def count(self, query: SQL | Composed, parameters: dict[str, Any]) -> int:
     """
     Execute a COUNT query and return the integer result.

     Args:
         query (SQL | Composed): SQL COUNT(*) query expected to return a numeric field.
         parameters (dict[str, Any]): Parameters to inject into the query.

     Returns:
         int: The count returned by the query.
      """
     result = self.__connection.execute(sql.SQL(query), params=parameters).fetchone() # type: ignore[assignment]
     if result is None:
        return 0
     # Extract the first value, expected to be COUNT(*)
     return int(next(iter(result.values())))

    def execute(self, query: SQL | Composed, parameters: dict[str, Any]) -> Any:
        """
        Execute a query with the given parameters.

        Args:
            query (SQL | Composed): SQL query to execute.
            parameters (dict[str, Any]): Parameters to inject into the query.

        Raises:
            NoRowAffectedError: If the query is an INSERT, UPDATE or DELETE and no row was affected.
        """
        result = self.__connection.execute(query=query, params=parameters)

        query_str = query.as_string(self.__connection)
        if query_str.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")) and result.rowcount == 0:
            raise NoRowAffectedError()

        # ✅ Return result so callers can read rowcount if they want
        return result
