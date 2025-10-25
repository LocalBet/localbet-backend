"""
Database module for the app.
"""

from collections.abc import Generator
from contextlib import contextmanager

from backend.settings import Settings
from backend.shared.infrastructure.connections import PostgreSqlConnection, PostgresSqlPool

pool = PostgresSqlPool(
    host=Settings.DATABASE_HOST,
    port=Settings.DATABASE_PORT,
    username=Settings.DATABASE_USERNAME,
    password=Settings.DATABASE_PASSWORD,
    database=Settings.DATABASE_NAME,
    minimum_connections=Settings.DATABASE_MINIMUM_CONNECTIONS,
    maximum_connections=Settings.DATABASE_MAXIMUM_CONNECTIONS,
)


@contextmanager
def get_database_connection() -> Generator[PostgreSqlConnection]:
    """
    Get a database connection context manager.

    Returns:
        Generator[PostgreSqlConnection]: A generator that yields a PostgreSqlConnection instance.
    """
    with pool.get_connection() as connection:
        try:
            yield connection

        except Exception as exception:
            raise exception
