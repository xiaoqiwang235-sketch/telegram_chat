"""Async database connection pool management supporting MySQL and SQLite."""

from contextlib import asynccontextmanager
from typing import AsyncContextManager, Awaitable, Literal

from src.database.config import DatabaseConfig, get_database_config

# Global connection pool instance (singleton)
_pool_instance: "ConnectionPool | None" = None


class ConnectionPool:
    """Async database connection manager supporting MySQL and SQLite.

    Attributes:
        config: Database configuration
        _pool: Internal pool/connection instance
    """

    def __init__(self, config: DatabaseConfig) -> None:
        """Initialize connection pool.

        Args:
            config: Database configuration
        """
        self.config = config
        self._pool: "aiomysql.Pool | aiosqlite.Connection | None" = None

    async def initialize(self) -> None:
        """Initialize the database connection/pool.

        Creates the appropriate connection based on db_type.
        """
        if self._pool is None:
            if self.config.db_type == "mysql":
                import aiomysql

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
            else:  # sqlite
                import aiosqlite

                self._pool = await aiosqlite.connect(self.config.db_path)
                # Enable foreign keys
                await self._pool.execute("PRAGMA foreign_keys = ON")
                # Enable WAL mode for better concurrent access
                await self._pool.execute("PRAGMA journal_mode = WAL")
                await self._pool.commit()

    async def acquire(self):
        """Acquire a connection from the pool.

        Returns:
            Database connection (aiomysql.Connection or aiosqlite.Connection)

        Raises:
            RuntimeError: If pool is not initialized
        """
        if self._pool is None:
            await self.initialize()

        assert self._pool is not None  # For type checker
        if self.config.db_type == "mysql":
            return await self._pool.acquire()
        else:
            return self._pool

    async def release(self, connection) -> None:
        """Release a connection back to the pool.

        Args:
            connection: Connection to release

        Raises:
            RuntimeError: If pool is not initialized
        """
        if self._pool is None:
            raise RuntimeError("Connection pool is not initialized")

        if self.config.db_type == "mysql":
            self._pool.release(connection)
        # For SQLite, no need to release

    async def close(self) -> None:
        """Close the database connection/pool."""
        if self._pool is not None:
            if self.config.db_type == "mysql":
                self._pool.close()
                await self._pool.wait_closed()
            else:
                await self._pool.close()
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
