"""Unit tests for Long-Term Memory module."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import numpy as np

from src.memory.long_term_memory import LongTermMemory
from src.models.conversation import Conversation


class TestLongTermMemory:
    """Test suite for LongTermMemory class."""

    @pytest.mark.asyncio
    async def test_long_term_memory_initialization(self):
        """Test LongTermMemory initialization."""
        mock_embedding_client = MagicMock()
        mock_faiss_manager = MagicMock()
        mock_conv_repo = MagicMock()
        mock_vector_repo = MagicMock()

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        assert memory.embedding_client == mock_embedding_client
        assert memory.faiss_manager == mock_faiss_manager
        assert memory.conversation_repo == mock_conv_repo
        assert memory.vector_repo == mock_vector_repo

    @pytest.mark.asyncio
    async def test_long_term_memory_add_conversation(self):
        """Test adding a conversation to long-term memory."""
        mock_embedding_client = AsyncMock()
        mock_faiss_manager = AsyncMock()
        mock_conv_repo = AsyncMock()
        mock_vector_repo = AsyncMock()

        # Setup mocks
        mock_embedding_client.generate_embedding.return_value = np.array([0.1] * 1536)
        mock_conv_repo.create.return_value = True
        mock_vector_repo.create.return_value = True
        mock_faiss_manager.add_vector.return_value = None

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        conversation = Conversation(
            conversation_id=1,
            user_id=123,
            group_id=None,
            role="user",
            content="Hello, world!",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        await memory.add_conversation(conversation)

        # Verify embedding was generated
        mock_embedding_client.generate_embedding.assert_called_once_with("Hello, world!")

        # Verify conversation was saved
        mock_conv_repo.create.assert_called_once()

        # Verify vector was saved
        mock_vector_repo.create.assert_called_once()

        # Verify vector was added to Faiss index
        mock_faiss_manager.add_vector.assert_called_once()

    @pytest.mark.asyncio
    async def test_long_term_memory_search_similar(self):
        """Test searching for similar conversations."""
        mock_embedding_client = AsyncMock()
        mock_faiss_manager = AsyncMock()
        mock_conv_repo = AsyncMock()
        mock_vector_repo = AsyncMock()

        # Setup mocks
        mock_embedding_client.generate_embedding.return_value = np.array([0.1] * 1536)
        mock_faiss_manager.search.return_value = {
            "conversation_ids": [1, 2, 3],
            "distances": [0.1, 0.2, 0.3],
        }
        mock_conv_repo.get_by_id.side_effect = [
            Conversation(
                conversation_id=1,
                user_id=123,
                group_id=None,
                role="user",
                content="Similar 1",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            ),
            Conversation(
                conversation_id=2,
                user_id=123,
                group_id=None,
                role="assistant",
                content="Similar 2",
                timestamp="2024-01-01 12:00:01",
                message_id=1002,
                style_id=1,
            ),
            Conversation(
                conversation_id=3,
                user_id=123,
                group_id=None,
                role="user",
                content="Similar 3",
                timestamp="2024-01-01 12:00:02",
                message_id=1003,
                style_id=1,
            ),
        ]

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        results = await memory.search_similar("Hello", user_id=123, k=3)

        assert len(results) == 3
        assert results[0]["conversation_id"] == 1
        assert results[1]["conversation_id"] == 2
        assert results[2]["conversation_id"] == 3

    @pytest.mark.asyncio
    async def test_long_term_memory_get_conversation_history(self):
        """Test getting conversation history."""
        mock_embedding_client = MagicMock()
        mock_faiss_manager = MagicMock()
        mock_conv_repo = AsyncMock()
        mock_vector_repo = MagicMock()

        # Setup mock
        mock_conv_repo.get_conversation_history.return_value = [
            Conversation(
                conversation_id=1,
                user_id=123,
                group_id=None,
                role="user",
                content="Hello",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            ),
            Conversation(
                conversation_id=2,
                user_id=123,
                group_id=None,
                role="assistant",
                content="Hi there",
                timestamp="2024-01-01 12:00:01",
                message_id=1002,
                style_id=1,
            ),
        ]

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        history = await memory.get_conversation_history(user_id=123, limit=10)

        assert len(history) == 2
        assert history[0].role == "user"
        assert history[1].role == "assistant"

    @pytest.mark.asyncio
    async def test_long_term_memory_delete_conversation(self):
        """Test deleting a conversation."""
        mock_embedding_client = MagicMock()
        mock_faiss_manager = AsyncMock()
        mock_conv_repo = AsyncMock()
        mock_vector_repo = AsyncMock()

        # Setup mocks
        mock_conv_repo.delete.return_value = True
        mock_vector_repo.delete.return_value = True
        mock_faiss_manager.remove_by_conversation_id.return_value = True

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        result = await memory.delete_conversation(conversation_id=1)

        assert result is True
        mock_conv_repo.delete.assert_called_once_with(1)
        mock_vector_repo.delete.assert_called_once_with(1)
        mock_faiss_manager.remove_by_conversation_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_long_term_memory_delete_user_history(self):
        """Test deleting all conversation history for a user."""
        mock_embedding_client = MagicMock()
        mock_faiss_manager = AsyncMock()
        mock_conv_repo = AsyncMock()
        mock_vector_repo = AsyncMock()

        # Setup mocks
        mock_conv_repo.get_conversation_history.return_value = [
            Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp="2024-01-01 12:00:00",
                message_id=1000 + i,
                style_id=1,
            )
            for i in range(5)
        ]
        mock_conv_repo.delete.return_value = True
        mock_vector_repo.delete.return_value = True
        mock_faiss_manager.remove_by_conversation_id.return_value = True

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        count = await memory.delete_user_history(user_id=123)

        assert count == 5

    @pytest.mark.asyncio
    async def test_long_term_memory_get_conversation_count(self):
        """Test getting conversation count for user."""
        mock_embedding_client = MagicMock()
        mock_faiss_manager = MagicMock()
        mock_conv_repo = AsyncMock()
        mock_vector_repo = MagicMock()

        # Setup mock
        mock_conv_repo.count_by_user.return_value = 10

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        count = await memory.get_conversation_count(user_id=123)

        assert count == 10

    @pytest.mark.asyncio
    async def test_long_term_memory_search_with_group_filter(self):
        """Test searching with group filter."""
        mock_embedding_client = AsyncMock()
        mock_faiss_manager = AsyncMock()
        mock_conv_repo = AsyncMock()
        mock_vector_repo = AsyncMock()

        # Setup mocks
        mock_embedding_client.generate_embedding.return_value = np.array([0.1] * 1536)
        mock_faiss_manager.search.return_value = {
            "conversation_ids": [1, 2],
            "distances": [0.1, 0.2],
        }
        mock_conv_repo.get_by_id.side_effect = [
            Conversation(
                conversation_id=1,
                user_id=123,
                group_id=456,
                role="user",
                content="Group message 1",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            ),
            Conversation(
                conversation_id=2,
                user_id=123,
                group_id=456,
                role="assistant",
                content="Group message 2",
                timestamp="2024-01-01 12:00:01",
                message_id=1002,
                style_id=1,
            ),
        ]

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        results = await memory.search_similar(
            "Group query", user_id=123, group_id=456, k=5
        )

        assert len(results) == 2
        assert all(r["group_id"] == 456 for r in results)

    @pytest.mark.asyncio
    async def test_long_term_memory_empty_search(self):
        """Test searching when no results found."""
        mock_embedding_client = AsyncMock()
        mock_faiss_manager = AsyncMock()
        mock_conv_repo = AsyncMock()
        mock_vector_repo = AsyncMock()

        # Setup mocks
        mock_embedding_client.generate_embedding.return_value = np.array([0.1] * 1536)
        mock_faiss_manager.search.return_value = {"conversation_ids": [], "distances": []}

        memory = LongTermMemory(
            embedding_client=mock_embedding_client,
            faiss_manager=mock_faiss_manager,
            conversation_repo=mock_conv_repo,
            vector_repo=mock_vector_repo,
        )

        results = await memory.search_similar("Query", user_id=123, k=5)

        assert results == []
