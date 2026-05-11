"""Unit tests for Connection Pool module."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.database.connection_pool import ConnectionPool, get_connection_pool


class TestConnectionPool:
    """Test suite for ConnectionPool class."""

    @pytest.mark.asyncio
    async def test_connection_pool_initialization(self):
        """Test ConnectionPool initialization."""
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 3306
        mock_config.database = "test_db"
        mock_config.user = "test_user"
        mock_config.password = "test_pass"
        mock_config.pool_size = 5
        mock_config.max_overflow = 10

        with patch("src.database.connection_pool.aiomysql.create_pool"):
            pool = ConnectionPool(mock_config)

            assert pool.config == mock_config
            assert pool._pool is None

    @pytest.mark.asyncio
    async def test_connection_pool_initialize(self):
        """Test ConnectionPool initialize method."""
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 3306
        mock_config.database = "test_db"
        mock_config.user = "test_user"
        mock_config.password = "test_pass"
        mock_config.pool_size = 5
        mock_config.max_overflow = 10

        mock_pool = AsyncMock()
        mock_pool.acquire = AsyncMock()
        mock_pool.release = MagicMock()
        mock_pool.close = AsyncMock()
        mock_pool.wait_closed = AsyncMock()

        with patch("src.database.connection_pool.aiomysql.create_pool", return_value=mock_pool):
            pool = ConnectionPool(mock_config)
            await pool.initialize()

            assert pool._pool is not None
            assert pool._pool == mock_pool

    @pytest.mark.asyncio
    async def test_connection_pool_acquire(self):
        """Test acquiring connection from pool."""
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 3306
        mock_config.database = "test_db"
        mock_config.user = "test_user"
        mock_config.password = "test_pass"
        mock_config.pool_size = 5
        mock_config.max_overflow = 10

        mock_connection = AsyncMock()
        mock_pool = AsyncMock()
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()
        mock_pool.close = AsyncMock()
        mock_pool.wait_closed = AsyncMock()

        with patch("src.database.connection_pool.aiomysql.create_pool", return_value=mock_pool):
            pool = ConnectionPool(mock_config)
            await pool.initialize()

            connection = await pool.acquire()

            assert connection == mock_connection
            mock_pool.acquire.assert_called_once()

    @pytest.mark.asyncio
    async def test_connection_pool_release(self):
        """Test releasing connection back to pool."""
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 3306
        mock_config.database = "test_db"
        mock_config.user = "test_user"
        mock_config.password = "test_pass"
        mock_config.pool_size = 5
        mock_config.max_overflow = 10

        mock_connection = AsyncMock()
        mock_pool = AsyncMock()
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()
        mock_pool.close = AsyncMock()
        mock_pool.wait_closed = AsyncMock()

        with patch("src.database.connection_pool.aiomysql.create_pool", return_value=mock_pool):
            pool = ConnectionPool(mock_config)
            await pool.initialize()

            await pool.release(mock_connection)

            mock_pool.release.assert_called_once_with(mock_connection)

    @pytest.mark.asyncio
    async def test_connection_pool_close(self):
        """Test closing connection pool."""
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 3306
        mock_config.database = "test_db"
        mock_config.user = "test_user"
        mock_config.password = "test_pass"
        mock_config.pool_size = 5
        mock_config.max_overflow = 10

        mock_pool = AsyncMock()
        mock_pool.acquire = AsyncMock()
        mock_pool.release = MagicMock()
        mock_pool.close = AsyncMock()
        mock_pool.wait_closed = AsyncMock()

        with patch("src.database.connection_pool.aiomysql.create_pool", return_value=mock_pool):
            pool = ConnectionPool(mock_config)
            await pool.initialize()

            await pool.close()

            mock_pool.close.assert_called_once()
            mock_pool.wait_closed.assert_called_once()
            assert pool._pool is None

    @pytest.mark.asyncio
    async def test_connection_pool_context_manager(self):
        """Test ConnectionPool as async context manager."""
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 3306
        mock_config.database = "test_db"
        mock_config.user = "test_user"
        mock_config.password = "test_pass"
        mock_config.pool_size = 5
        mock_config.max_overflow = 10

        mock_pool = AsyncMock()
        mock_pool.acquire = AsyncMock()
        mock_pool.release = MagicMock()
        mock_pool.close = AsyncMock()
        mock_pool.wait_closed = AsyncMock()

        with patch("src.database.connection_pool.aiomysql.create_pool", return_value=mock_pool):
            async with ConnectionPool(mock_config) as pool:
                assert pool._pool is not None
                assert isinstance(pool, ConnectionPool)

            # Verify close was called when exiting context
            mock_pool.close.assert_called_once()
            mock_pool.wait_closed.assert_called_once()

    @pytest.mark.asyncio
    async def test_connection_pool_acquire_without_initialize(self):
        """Test acquiring connection without initializing pool first."""
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 3306
        mock_config.database = "test_db"
        mock_config.user = "test_user"
        mock_config.password = "test_pass"
        mock_config.pool_size = 5
        mock_config.max_overflow = 10

        mock_pool = AsyncMock()
        mock_pool.acquire = AsyncMock()
        mock_pool.release = MagicMock()
        mock_pool.close = AsyncMock()
        mock_pool.wait_closed = AsyncMock()

        with patch("src.database.connection_pool.aiomysql.create_pool", return_value=mock_pool):
            pool = ConnectionPool(mock_config)

            # Should auto-initialize if not initialized
            connection = await pool.acquire()

            assert pool._pool is not None
            mock_pool.acquire.assert_called_once()

    @pytest.mark.asyncio
    async def test_connection_pool_double_initialize(self):
        """Test initializing connection pool twice."""
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 3306
        mock_config.database = "test_db"
        mock_config.user = "test_user"
        mock_config.password = "test_pass"
        mock_config.pool_size = 5
        mock_config.max_overflow = 10

        mock_pool = AsyncMock()
        mock_pool.acquire = AsyncMock()
        mock_pool.release = MagicMock()
        mock_pool.close = AsyncMock()
        mock_pool.wait_closed = AsyncMock()

        with patch("src.database.connection_pool.aiomysql.create_pool", return_value=mock_pool):
            pool = ConnectionPool(mock_config)
            await pool.initialize()
            await pool.initialize()  # Second initialize should be no-op

            # Should only create pool once
            assert mock_pool.close.call_count == 0


class TestGetConnectionPool:
    """Test suite for get_connection_pool function."""

    @pytest.mark.asyncio
    async def test_get_connection_pool_singleton(self, mock_env_vars):
        """Test that get_connection_pool returns singleton instance."""
        with patch("src.database.connection_pool.get_database_config"):
            pool1 = await get_connection_pool()
            pool2 = await get_connection_pool()

            assert pool1 is pool2
            assert id(pool1) == id(pool2)

    @pytest.mark.asyncio
    async def test_get_connection_pool_creates_once(self, mock_env_vars):
        """Test that get_connection_pool creates instance only once."""
        with patch("src.database.connection_pool.get_database_config"):
            pool = await get_connection_pool()

            # Verify it's a ConnectionPool instance
            assert isinstance(pool, ConnectionPool)
            assert pool._pool is not None
