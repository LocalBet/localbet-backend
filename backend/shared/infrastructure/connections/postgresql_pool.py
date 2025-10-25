"""
PostgreSQL pool module.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from types import TracebackType
from typing import Self

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from .postgresql_connection import PostgreSqlConnection


class PostgresSqlPool:
    """
    PostgreSQL pool module.
    """

    __uri: str
    __minimum_connections: int
    __maximum_connections: int
    __pool: ConnectionPool

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        minimum_connections: int,
        maximum_connections: int,
    ) -> None:
        """
        PostgreSQL pool constructor.

        Args:
            host (str): PostgreSQL database host.
            port (int): PostgreSQL database port.
            username (str): PostgreSQL database username.
            password (str): PostgreSQL database password.
            database (str): PostgreSQL database name.
            minimum_connections (int): Minimum number of connections that must be kept in the pool.
            maximum_connections (int): Maximum number of connections that can be kept in the pool.
        """
        self.__uri = self.__create_uri(username=username, password=password, host=host, port=port, database=database)
        self.__minimum_connections = minimum_connections
        self.__maximum_connections = maximum_connections

    def open(self) -> None:
        """
        Open the pool.
        """
        self.__pool = ConnectionPool(
            conninfo=self.__uri,
            min_size=self.__minimum_connections,
            max_size=self.__maximum_connections,
        )

        self.__pool.wait()  # Waits for the pool to be ready

    def close(self) -> None:
        """
        Close the pool.
        """
        self.__pool.close()

    def __enter__(self) -> Self:
        """
        Enter the postgresql pool context.

        Returns:
            Self: The postgresql pool instance.
        """
        self.__pool.__enter__()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Exit the postgresql pool context.

        Args:
            exc_type (type[BaseException] | None): Exception type.
            exc_value (BaseException | None): Exception value.
            traceback (TracebackType | None): Traceback.
        """
        self.__pool.__exit__(exc_type, exc_value, traceback)

    @staticmethod
    def __create_uri(username: str, password: str, host: str, port: int, database: str) -> str:
        """
        Create the Database URI.

        Args:
            username (str): PostgreSQL database username.
            password (str): PostgreSQL database password.
            host (str): PostgreSQL database host.
            port (int): PostgreSQL database port.
            database (str): PostgreSQL database name.

        Returns:
            str: Database connection URI.
        """
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"

    @contextmanager
    def get_connection(self) -> Iterator[PostgreSqlConnection]:
        """
        Get an available connection from the pool.

        Returns:
            PostgreSqlConnection: PostgreSqlConnection instance.
        """
        connection = self.__pool.getconn()
        connection.row_factory = dict_row  # type: ignore[assignment]

        try:
            yield PostgreSqlConnection(connection=connection)
            connection.commit()

        except Exception as exception:
            connection.rollback()

            raise exception

        finally:
            self.__pool.putconn(conn=connection)
