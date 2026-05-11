"""Base repository class for database operations."""

import aiomysql
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from src.database.connection_pool import ConnectionPool


class BaseRepository:
    """Base repository class providing common database operations.

    Attributes:
        pool: Database connection pool
    """

    def __init__(self, pool: ConnectionPool) -> None:
        """Initialize base repository.

        Args:
            pool: Database connection pool
        """
        self.pool = pool

    @asynccontextmanager
    async def _get_connection(self) -> AsyncGenerator[aiomysql.Connection, None]:
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
            query: SQL query string
            params: Query parameters

        Returns:
            List of result rows
        """
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params or ())
                return await cursor.fetchall()

    async def _execute_query_one(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> tuple[Any, ...] | None:
        """Execute a SELECT query and return one row.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Single result row or None if no results
        """
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params or ())
                return await cursor.fetchone()

    async def _execute_write(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> int:
        """Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Number of rows affected
        """
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params or ())
                await conn.commit()
                return cursor.rowcount

    async def _execute_batch(
        self, query: str, params_list: list[tuple[Any, ...]]
    ) -> int:
        """Execute a batch operation.

        Args:
            query: SQL query string
            params_list: List of parameter tuples

        Returns:
            Number of rows affected
        """
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(query, params_list)
                await conn.commit()
                return cursor.rowcount

    async def _get_last_insert_id(self) -> int:
        """Get the last inserted ID.

        Returns:
            Last insert ID
        """
        result = await self._execute_query_one("SELECT LAST_INSERT_ID()")
        if result:
            return result[0]
        return 0

    @asynccontextmanager
    async def _transaction(self) -> AsyncGenerator[aiomysql.Connection, None]:
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
        query = """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
            AND table_name = %s
        """
        result = await self._execute_query_one(query, (table_name,))
        return result is not None and result[0] > 0
