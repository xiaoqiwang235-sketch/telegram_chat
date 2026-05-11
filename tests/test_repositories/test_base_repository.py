"""Unit tests for Base Repository module."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.repositories.base_repository import BaseRepository


class MockModel:
    """Mock model for testing."""

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def to_dict(self):
        """Convert to dictionary."""
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        return cls(data["id"], data["name"])

    def __eq__(self, other):
        """Equality check."""
        return self.id == other.id and self.name == other.name


class TestBaseRepository:
    """Test suite for BaseRepository class."""

    @pytest.mark.asyncio
    async def test_base_repository_initialization(self):
        """Test BaseRepository initialization."""
        mock_pool = AsyncMock()

        repo = BaseRepository(mock_pool)

        assert repo.pool == mock_pool

    @pytest.mark.asyncio
    async def test_base_repository_execute_query(self):
        """Test executing SQL query."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[(1, "test")])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        result = await repo._execute_query("SELECT * FROM test")

        mock_cursor.execute.assert_called_once_with("SELECT * FROM test")
        mock_cursor.fetchall.assert_called_once()
        assert result == [(1, "test")]

    @pytest.mark.asyncio
    async def test_base_repository_execute_query_with_params(self):
        """Test executing SQL query with parameters."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[(1, "test")])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        result = await repo._execute_query(
            "SELECT * FROM test WHERE id = %s", (1,)
        )

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM test WHERE id = %s", (1,)
        )
        assert result == [(1, "test")]

    @pytest.mark.asyncio
    async def test_base_repository_execute_write(self):
        """Test executing write operation (INSERT/UPDATE/DELETE)."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock(return_value=1)
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        rows_affected = await repo._execute_write(
            "INSERT INTO test (name) VALUES (%s)", ("test_name",)
        )

        mock_cursor.execute.assert_called_once()
        assert rows_affected == 1

    @pytest.mark.asyncio
    async def test_base_repository_execute_write_many(self):
        """Test executing write operation affecting multiple rows."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock(return_value=3)
        mock_cursor.rowcount = 3
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        rows_affected = await repo._execute_write(
            "UPDATE test SET status = %s", ("active",)
        )

        assert rows_affected == 3

    @pytest.mark.asyncio
    async def test_base_repository_execute_batch(self):
        """Test executing batch operations."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.executemany = AsyncMock(return_value=2)
        mock_cursor.rowcount = 2
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        rows_affected = await repo._execute_batch(
            "INSERT INTO test (name) VALUES (%s)", [("test1",), ("test2",)]
        )

        mock_cursor.executemany.assert_called_once()
        assert rows_affected == 2

    @pytest.mark.asyncio
    async def test_base_repository_get_last_insert_id(self):
        """Test getting last insert ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.lastrowid = 123
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        last_id = await repo._get_last_insert_id()

        assert last_id == 123

    @pytest.mark.asyncio
    async def test_base_repository_transaction_commit(self):
        """Test transaction commit."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_connection.commit = AsyncMock()
        mock_connection.rollback = AsyncMock()
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        async with repo._transaction() as conn:
            assert conn == mock_connection

        mock_connection.commit.assert_called_once()
        mock_connection.rollback.assert_not_called()

    @pytest.mark.asyncio
    async def test_base_repository_transaction_rollback(self):
        """Test transaction rollback on error."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_connection.commit = AsyncMock()
        mock_connection.rollback = AsyncMock()
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        with pytest.raises(ValueError):
            async with repo._transaction() as conn:
                assert conn == mock_connection
                raise ValueError("Test error")

        mock_connection.commit.assert_not_called()
        mock_connection.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_repository_connection_context_manager(self):
        """Test connection acquisition via context manager."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        async with repo._get_connection() as conn:
            assert conn == mock_connection

        mock_pool.acquire.assert_called_once()
        # Note: release is handled by _execute_query and _execute_write

    @pytest.mark.asyncio
    async def test_base_repository_execute_query_empty_result(self):
        """Test executing query that returns no results."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        result = await repo._execute_query("SELECT * FROM test WHERE id = %s", (999,))

        assert result == []

    @pytest.mark.asyncio
    async def test_base_repository_execute_query_one_row(self):
        """Test executing query that returns one row."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(1, "test"))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        result = await repo._execute_query_one(
            "SELECT * FROM test WHERE id = %s", (1,)
        )

        mock_cursor.fetchone.assert_called_once()
        assert result == (1, "test")

    @pytest.mark.asyncio
    async def test_base_repository_execute_query_one_no_result(self):
        """Test executing query that returns no results when expecting one."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        result = await repo._execute_query_one(
            "SELECT * FROM test WHERE id = %s", (999,)
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_base_repository_table_exists(self):
        """Test checking if table exists."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(1,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        exists = await repo._table_exists("test_table")

        assert exists is True

    @pytest.mark.asyncio
    async def test_base_repository_table_not_exists(self):
        """Test checking if non-existent table exists."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = BaseRepository(mock_pool)

        exists = await repo._table_exists("non_existent_table")

        assert exists is False
