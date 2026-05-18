"""Base repository class for database operations supporting MySQL and SQLite."""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from src.database.config import get_database_config
from src.database.connection_pool import ConnectionPool


class BaseRepository:
    """Base repository class providing common database operations.

    Attributes:
        pool: Database connection pool
        param_placeholder: Parameter placeholder for SQL queries (? or %s)
    """

    def __init__(self, pool: ConnectionPool) -> None:
        """Initialize base repository.

        Args:
            pool: Database connection pool
        """
        self.pool = pool
        # Get parameter placeholder based on database type
        config = get_database_config()
        self.param_placeholder = "??" if config.db_type == "mysql" else "?"
        self.db_type = config.db_type

    def _format_query(self, query: str) -> str:
        """Format query with appropriate parameter placeholders.

        Args:
            query: SQL query with %s placeholders

        Returns:
            Query with appropriate placeholders for the database type
        """
        if self.db_type == "sqlite":
            return query.replace("%s", "?")
        return query

    @asynccontextmanager
    async def _get_connection(self):
        """Acquire a database connection.

        Yields:
            Database connection
        """
        connection = await self.pool.acquire()
        try:
            yield connection
        finally:
            await self.pool.release(connection)

    async def _execute_query(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> list[tuple[Any, ...]]:
        """Execute a SELECT query.

        Args:
            query: SQL query string with %s placeholders
            params: Query parameters

        Returns:
            List of result rows
        """
        formatted_query = self._format_query(query)
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(formatted_query, params or ())
                return await cursor.fetchall()

    async def _execute_query_one(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> tuple[Any, ...] | None:
        """Execute a SELECT query and return one row.

        Args:
            query: SQL query string with %s placeholders
            params: Query parameters

        Returns:
            Single result row or None if no results
        """
        formatted_query = self._format_query(query)
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(formatted_query, params or ())
                return await cursor.fetchone()

    async def _execute_write(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> int:
        """Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query string with %s placeholders
            params: Query parameters

        Returns:
            Number of rows affected
        """
        formatted_query = self._format_query(query)
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(formatted_query, params or ())
                await conn.commit()
                return cursor.rowcount

    async def _execute_batch(
        self, query: str, params_list: list[tuple[Any, ...]]
    ) -> int:
        """Execute a batch operation.

        Args:
            query: SQL query string with %s placeholders
            params_list: List of parameter tuples

        Returns:
            Number of rows affected
        """
        formatted_query = self._format_query(query)
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(formatted_query, params_list)
                await conn.commit()
                return cursor.rowcount

    async def _get_last_insert_id(self) -> int:
        """Get the last inserted ID.

        Returns:
            Last insert ID
        """
        if self.db_type == "mysql":
            result = await self._execute_query_one("SELECT LAST_INSERT_ID()")
        else:  # sqlite
            result = await self._execute_query_one("SELECT last_insert_rowid()")

        if result:
            return result[0]
        return 0

    @asynccontextmanager
    async def _transaction(self):
        """Execute operations in a transaction.

        Yields:
            Database connection within transaction

        Raises:
            Exception: Re-raises any exception after rollback
        """
        async with self._get_connection() as conn:
            try:
                yield conn
                await conn.commit()
            except Exception:
                await conn.rollback()
                raise

    async def _table_exists(self, table_name: str) -> bool:
        """Check if a table exists.

        Args:
            table_name: Name of the table to check

        Returns:
            True if table exists, False otherwise
        """
        if self.db_type == "mysql":
            query = """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = DATABASE()
                AND table_name = %s
            """
            result = await self._execute_query_one(query, (table_name,))
            return result is not None and result[0] > 0
        else:  # sqlite
            query = """
                SELECT COUNT(*)
                FROM sqlite_master
                WHERE type='table'
                AND name = ?
            """
            result = await self._execute_query_one(query, (table_name,))
            return result is not None and result[0] > 0
