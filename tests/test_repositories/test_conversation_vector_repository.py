"""Unit tests for ConversationVector Repository module."""

import pytest
from unittest.mock import AsyncMock, MagicMock
import numpy as np

from src.repositories.conversation_vector_repository import ConversationVectorRepository


class TestConversationVectorRepository:
    """Test suite for ConversationVectorRepository class."""

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_create(self):
        """Test creating a new conversation vector."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        vector = np.array([0.1, 0.2, 0.3], dtype=np.float32)

        result = await repo.create(
            conversation_id=1,
            vector=vector,
            vector_id="vec_001",
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_get_by_conversation_id(self):
        """Test getting vectors by conversation ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(b"\x00\x00\x80?")  # Binary vector data
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        vector = await repo.get_by_conversation_id(1)

        assert vector is not None
        assert isinstance(vector, np.ndarray)
        assert vector.dtype == np.float32

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_get_by_conversation_id_not_found(self):
        """Test getting vectors for non-existent conversation."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        vector = await repo.get_by_conversation_id(999)

        assert vector is None

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_get_all_vectors(self):
        """Test getting all vectors."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (1, b"\x00\x00\x80?"),
                (2, b"\x00\x00\x80?"),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        vectors = await repo.get_all_vectors(limit=10)

        assert len(vectors) == 2
        assert all(isinstance(v, np.ndarray) for v in vectors)

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_delete(self):
        """Test deleting a conversation vector."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        result = await repo.delete(1)

        assert result is True

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_delete_not_found(self):
        """Test deleting non-existent conversation vector."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 0
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        result = await repo.delete(999)

        assert result is False

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_count(self):
        """Test counting total vectors."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(100,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        count = await repo.count()

        assert count == 100

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_exists(self):
        """Test checking if conversation vector exists."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(1,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        exists = await repo.exists(1)

        assert exists is True

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_not_exists(self):
        """Test checking if non-existent conversation vector exists."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        exists = await repo.exists(999)

        assert exists is False

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_get_by_vector_id(self):
        """Test getting vector by vector ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(1, b"\x00\x00\x80?"))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        conversation_id = await repo.get_by_vector_id("vec_001")

        assert conversation_id == 1

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_get_by_vector_id_not_found(self):
        """Test getting non-existent vector by ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        conversation_id = await repo.get_by_vector_id("nonexistent")

        assert conversation_id is None

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_batch_insert(self):
        """Test batch inserting vectors."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.executemany = AsyncMock()
        mock_cursor.rowcount = 3
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        vectors = [
            (1, np.array([0.1, 0.2, 0.3], dtype=np.float32), "vec_001"),
            (2, np.array([0.4, 0.5, 0.6], dtype=np.float32), "vec_002"),
            (3, np.array([0.7, 0.8, 0.9], dtype=np.float32), "vec_003"),
        ]

        count = await repo.batch_insert(vectors)

        assert count == 3

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_delete_by_conversation_id(self):
        """Test deleting vectors by conversation ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 2
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        count = await repo.delete_by_conversation_id(1)

        assert count == 2

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_get_all_vectors_empty(self):
        """Test getting all vectors when none exist."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        vectors = await repo.get_all_vectors(limit=10)

        assert len(vectors) == 0

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_vector_serialization(self):
        """Test vector serialization to binary format."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        vector = np.array([0.1, 0.2, 0.3, 0.4, 0.5], dtype=np.float32)

        # Should not raise any exceptions
        result = await repo.create(1, vector, "vec_test")

        assert result is True

    @pytest.mark.asyncio
    async def test_conversation_vector_repository_vector_deserialization(self):
        """Test vector deserialization from binary format."""
        # Create a numpy array and convert to bytes
        original_vector = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        vector_bytes = original_vector.tobytes()

        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=vector_bytes)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationVectorRepository(mock_pool)

        vector = await repo.get_by_conversation_id(1)

        assert vector is not None
        np.testing.assert_array_almost_equal(vector, original_vector)
