"""Async database connection pool management."""

import aiomysql
from typing import AsyncContextManager, Awaitable

from src.database.config import DatabaseConfig, get_database_config

# Global connection pool instance (singleton)
_pool_instance: "ConnectionPool | None" = None


class ConnectionPool:
    """Async database connection pool manager.

    Attributes:
        config: Database configuration
        _pool: Internal aiomysql pool instance
    """

    def __init__(self, config: DatabaseConfig) -> None:
        """Initialize connection pool.

        Args:
            config: Database configuration
        """
        self.config = config
        self._pool: aiomysql.Pool | None = None

    async def initialize(self) -> None:
        """Initialize the connection pool.

        Creates the aiomysql pool with the configured parameters.
        """
        if self._pool is None:
            self._pool = await aiomysql.create_pool(
                host=self.config.host,
                port=self.config.port,
                db=self.config.database,
                user=self.config.user,
                password=self.config.password,
                minsize=1,
                maxsize=self.config.pool_size + self.config.max_overflow,
                autocommit=False,
            )

    async def acquire(self) -> aiomysql.Connection:
        """Acquire a connection from the pool.

        Returns:
            Database connection

        Raises:
            RuntimeError: If pool is not initialized
        """
        if self._pool is None:
            await self.initialize()

        assert self._pool is not None  # For type checker
        return await self._pool.acquire()

    async def release(self, connection: aiomysql.Connection) -> None:
        """Release a connection back to the pool.

        Args:
            connection: Connection to release
        """
        if self._pool is None:
            raise RuntimeError("Connection pool is not initialized")

        self._pool.release(connection)

    async def close(self) -> None:
        """Close the connection pool."""
        if self._pool is not None:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None

    async def __aenter__(self) -> "ConnectionPool":
        """Async context manager entry.

        Returns:
            Initialized connection pool
        """
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        await self.close()


async def get_connection_pool() -> ConnectionPool:
    """Get or create connection pool singleton.

    Returns:
        ConnectionPool instance

    Note:
        Uses get_database_config() to get database configuration.
    """
    global _pool_instance

    if _pool_instance is None:
        config = get_database_config()
        _pool_instance = ConnectionPool(config)
        await _pool_instance.initialize()

    return _pool_instance
