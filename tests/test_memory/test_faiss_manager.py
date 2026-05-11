"""Unit tests for Faiss Manager module."""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import numpy as np

from src.memory.faiss_manager import FaissManager


class TestFaissManager:
    """Test suite for FaissManager class."""

    @pytest.mark.asyncio
    async def test_faiss_manager_initialization(self):
        """Test FaissManager initialization."""
        manager = FaissManager(dimension=1536)

        assert manager.dimension == 1536
        assert manager.index is not None
        assert manager._vector_ids == []
        assert manager._conversation_ids == []

    @pytest.mark.asyncio
    async def test_faiss_manager_add_vector(self):
        """Test adding a vector to the index."""
        manager = FaissManager(dimension=128)

        vector = np.random.rand(128).astype(np.float32)
        await manager.add_vector(vector_id="vec_1", conversation_id=1, vector=vector)

        assert len(manager._vector_ids) == 1
        assert len(manager._conversation_ids) == 1
        assert manager._vector_ids[0] == "vec_1"
        assert manager._conversation_ids[0] == 1

    @pytest.mark.asyncio
    async def test_faiss_manager_add_batch_vectors(self):
        """Test adding multiple vectors to the index."""
        manager = FaissManager(dimension=128)

        vectors = [np.random.rand(128).astype(np.float32) for _ in range(5)]
        vector_ids = [f"vec_{i}" for i in range(5)]
        conversation_ids = list(range(5))

        await manager.add_batch_vectors(
            vector_ids=vector_ids,
            conversation_ids=conversation_ids,
            vectors=vectors,
        )

        assert len(manager._vector_ids) == 5
        assert len(manager._conversation_ids) == 5

    @pytest.mark.asyncio
    async def test_faiss_manager_search(self):
        """Test searching for similar vectors."""
        manager = FaissManager(dimension=128)

        # Add some vectors
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(10)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i, vector=vector
            )

        # Search
        query_vector = vectors[0]
        results = await manager.search(query_vector, k=5)

        assert len(results) == 5
        assert "conversation_ids" in results
        assert "distances" in results
        assert len(results["conversation_ids"]) == 5
        assert len(results["distances"]) == 5

    @pytest.mark.asyncio
    async def test_faiss_manager_search_empty_index(self):
        """Test searching in empty index."""
        manager = FaissManager(dimension=128)

        query_vector = np.random.rand(128).astype(np.float32)
        results = await manager.search(query_vector, k=5)

        assert results["conversation_ids"] == []
        assert results["distances"] == []

    @pytest.mark.asyncio
    async def test_faiss_manager_remove_by_conversation_id(self):
        """Test removing vectors by conversation ID."""
        manager = FaissManager(dimension=128)

        # Add vectors
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(5)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i % 2, vector=vector
            )

        # Remove conversation 0
        removed = await manager.remove_by_conversation_id(conversation_id=0)

        assert removed is True
        assert len(manager._conversation_ids) == 3

    @pytest.mark.asyncio
    async def test_faiss_manager_remove_by_conversation_id_not_found(self):
        """Test removing non-existent conversation ID."""
        manager = FaissManager(dimension=128)

        removed = await manager.remove_by_conversation_id(conversation_id=999)

        assert removed is False

    @pytest.mark.asyncio
    async def test_faiss_manager_get_vector_count(self):
        """Test getting vector count."""
        manager = FaissManager(dimension=128)

        assert await manager.get_vector_count() == 0

        # Add vectors
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(5)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i, vector=vector
            )

        assert await manager.get_vector_count() == 5

    @pytest.mark.asyncio
    async def test_faiss_manager_clear(self):
        """Test clearing the index."""
        manager = FaissManager(dimension=128)

        # Add vectors
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(5)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i, vector=vector
            )

        await manager.clear()

        assert len(manager._vector_ids) == 0
        assert len(manager._conversation_ids) == 0
        assert await manager.get_vector_count() == 0

    @pytest.mark.asyncio
    async def test_faiss_manager_rebuild_index(self):
        """Test rebuilding the index."""
        manager = FaissManager(dimension=128)

        # Add vectors
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(5)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i, vector=vector
            )

        # Rebuild
        await manager.rebuild_index()

        # Should still have same number of vectors
        assert len(manager._vector_ids) == 5
        assert len(manager._conversation_ids) == 5

    @pytest.mark.asyncio
    async def test_faiss_manager_search_with_filter(self):
        """Test searching with conversation ID filter."""
        manager = FaissManager(dimension=128)

        # Add vectors with different conversation IDs
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(10)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i // 2, vector=vector
            )

        # Search with filter
        query_vector = vectors[0]
        results = await manager.search(
            query_vector, k=5, conversation_filter=[0, 1]
        )

        # Should only return results from conversations 0 and 1
        assert all(cid in [0, 1] for cid in results["conversation_ids"])

    @pytest.mark.asyncio
    async def test_faiss_manager_invalid_dimension(self):
        """Test initializing with invalid dimension."""
        with pytest.raises(ValueError, match="Dimension must be positive"):
            FaissManager(dimension=0)

    @pytest.mark.asyncio
    async def test_faiss_manager_add_vector_wrong_dimension(self):
        """Test adding vector with wrong dimension."""
        manager = FaissManager(dimension=128)

        wrong_vector = np.random.rand(256).astype(np.float32)

        with pytest.raises(ValueError, match="Vector dimension mismatch"):
            await manager.add_vector(
                vector_id="vec_1", conversation_id=1, vector=wrong_vector
            )

    @pytest.mark.asyncio
    async def test_faiss_manager_search_invalid_k(self):
        """Test searching with invalid k value."""
        manager = FaissManager(dimension=128)

        query_vector = np.random.rand(128).astype(np.float32)

        with pytest.raises(ValueError, match="k must be positive"):
            await manager.search(query_vector, k=0)

    @pytest.mark.asyncio
    async def test_faiss_manager_search_k_larger_than_index(self):
        """Test searching with k larger than index size."""
        manager = FaissManager(dimension=128)

        # Add only 2 vectors
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(2)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i, vector=vector
            )

        # Search with k=10
        query_vector = vectors[0]
        results = await manager.search(query_vector, k=10)

        # Should return at most 2 results
        assert len(results["conversation_ids"]) <= 2

    @pytest.mark.asyncio
    async def test_faiss_manager_get_vectors_by_conversation(self):
        """Test getting vectors by conversation ID."""
        manager = FaissManager(dimension=128)

        # Add vectors
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(10)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i // 3, vector=vector
            )

        # Get vectors for conversation 1
        conv_vectors = await manager.get_vectors_by_conversation(conversation_id=1)

        # Should have 3 vectors (IDs 1, 2, 3)
        assert len(conv_vectors) == 3

    @pytest.mark.asyncio
    async def test_faiss_manager_save_and_load(self, tmp_path):
        """Test saving and loading index."""
        import tempfile

        manager = FaissManager(dimension=128)

        # Add vectors
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(5)]
        for i, vector in enumerate(vectors):
            await manager.add_vector(
                vector_id=f"vec_{i}", conversation_id=i, vector=vector
            )

        # Save index
        with tempfile.NamedTemporaryFile(suffix=".index", delete=False) as f:
            index_path = f.name

        try:
            await manager.save_index(index_path)

            # Create new manager and load
            new_manager = FaissManager(dimension=128)
            await new_manager.load_index(index_path)

            # Should have same number of vectors
            assert len(new_manager._vector_ids) == 5
            assert len(new_manager._conversation_ids) == 5
        finally:
            import os

            if os.path.exists(index_path):
                os.remove(index_path)

    @pytest.mark.asyncio
    async def test_faiss_manager_batch_add_empty(self):
        """Test batch adding empty list."""
        manager = FaissManager(dimension=128)

        with pytest.raises(ValueError, match="Cannot add empty batch"):
            await manager.add_batch_vectors(
                vector_ids=[], conversation_ids=[], vectors=[]
            )

    @pytest.mark.asyncio
    async def test_faiss_manager_batch_add_mismatched_lengths(self):
        """Test batch adding with mismatched lengths."""
        manager = FaissManager(dimension=128)

        vectors = [np.random.rand(128).astype(np.float32) for _ in range(3)]

        with pytest.raises(ValueError, match="Length mismatch"):
            await manager.add_batch_vectors(
                vector_ids=["vec_1", "vec_2"],
                conversation_ids=[1, 2, 3],
                vectors=vectors,
            )
