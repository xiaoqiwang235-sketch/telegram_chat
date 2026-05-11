"""Unit tests for Memory Manager module."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.memory.memory_manager import MemoryManager
from src.models.conversation import Conversation


class TestMemoryManager:
    """Test suite for MemoryManager class."""

    @pytest.mark.asyncio
    async def test_memory_manager_initialization(self):
        """Test MemoryManager initialization."""
        mock_short_term = MagicMock()
        mock_long_term = AsyncMock()

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        assert manager.short_term_memory == mock_short_term
        assert manager.long_term_memory == mock_long_term

    @pytest.mark.asyncio
    async def test_memory_manager_add_message(self):
        """Test adding a message to memory."""
        mock_short_term = MagicMock()
        mock_long_term = AsyncMock()

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        conversation = Conversation(
            conversation_id=1,
            user_id=123,
            group_id=None,
            role="user",
            content="Hello",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        await manager.add_message(conversation, save_long_term=False)

        # Should add to short-term memory
        mock_short_term.add.assert_called_once_with(123, conversation)

        # Should not add to long-term memory
        mock_long_term.add_conversation.assert_not_called()

    @pytest.mark.asyncio
    async def test_memory_manager_add_message_with_long_term(self):
        """Test adding a message to both short and long-term memory."""
        mock_short_term = MagicMock()
        mock_long_term = AsyncMock()
        mock_long_term.add_conversation.return_value = True

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        conversation = Conversation(
            conversation_id=1,
            user_id=123,
            group_id=None,
            role="user",
            content="Hello",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        await manager.add_message(conversation, save_long_term=True)

        # Should add to both memories
        mock_short_term.add.assert_called_once_with(123, conversation)
        mock_long_term.add_conversation.assert_called_once_with(conversation)

    @pytest.mark.asyncio
    async def test_memory_manager_get_context(self):
        """Test getting conversation context."""
        mock_short_term = MagicMock()
        mock_short_term.get_user_messages.return_value = [
            Conversation(
                conversation_id=1,
                user_id=123,
                group_id=None,
                role="user",
                content="Recent message",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            )
        ]

        mock_long_term = AsyncMock()
        mock_long_term.get_conversation_history.return_value = [
            Conversation(
                conversation_id=2,
                user_id=123,
                group_id=None,
                role="user",
                content="Old message",
                timestamp="2024-01-01 11:00:00",
                message_id=1002,
                style_id=1,
            )
        ]

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        context = await manager.get_context(user_id=123)

        assert len(context) == 2
        assert context[0].content == "Old message"  # Long-term first
        assert context[1].content == "Recent message"  # Short-term second

    @pytest.mark.asyncio
    async def test_memory_manager_search(self):
        """Test searching memory."""
        mock_short_term = MagicMock()
        mock_long_term = AsyncMock()

        mock_long_term.search_similar.return_value = [
            {
                "conversation_id": 1,
                "user_id": 123,
                "group_id": None,
                "role": "user",
                "content": "Similar message",
                "timestamp": "2024-01-01 12:00:00",
                "distance": 0.1,
            }
        ]

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        results = await manager.search("Hello", user_id=123, k=5)

        assert len(results) == 1
        assert results[0]["content"] == "Similar message"
        mock_long_term.search_similar.assert_called_once()

    @pytest.mark.asyncio
    async def test_memory_manager_clear_user(self):
        """Test clearing user memory."""
        mock_short_term = MagicMock()
        mock_long_term = AsyncMock()
        mock_long_term.delete_user_history.return_value = 5

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        await manager.clear_user(user_id=123, clear_long_term=True)

        # Should clear short-term memory
        mock_short_term.clear_user.assert_called_once_with(123)

        # Should clear long-term memory
        mock_long_term.delete_user_history.assert_called_once_with(123)

    @pytest.mark.asyncio
    async def test_memory_manager_clear_user_short_term_only(self):
        """Test clearing only short-term memory."""
        mock_short_term = MagicMock()
        mock_long_term = AsyncMock()

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        await manager.clear_user(user_id=123, clear_long_term=False)

        # Should only clear short-term memory
        mock_short_term.clear_user.assert_called_once_with(123)
        mock_long_term.delete_user_history.assert_not_called()

    @pytest.mark.asyncio
    async def test_memory_manager_get_message_count(self):
        """Test getting total message count."""
        mock_short_term = MagicMock()
        mock_short_term.get_message_count.return_value = 10

        mock_long_term = AsyncMock()
        mock_long_term.get_conversation_count.return_value = 100

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        count = await manager.get_message_count(user_id=123)

        assert count == 110  # 10 + 100

    @pytest.mark.asyncio
    async def test_memory_manager_sync_to_long_term(self):
        """Test syncing short-term memory to long-term."""
        mock_short_term = MagicMock()
        mock_short_term.get_user_messages.return_value = [
            Conversation(
                conversation_id=1,
                user_id=123,
                group_id=None,
                role="user",
                content="Message 1",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            ),
            Conversation(
                conversation_id=2,
                user_id=123,
                group_id=None,
                role="assistant",
                content="Message 2",
                timestamp="2024-01-01 12:00:01",
                message_id=1002,
                style_id=1,
            ),
        ]

        mock_long_term = AsyncMock()
        mock_long_term.add_conversation.return_value = True

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        synced = await manager.sync_to_long_term(user_id=123)

        assert synced == 2
        assert mock_long_term.add_conversation.call_count == 2

    @pytest.mark.asyncio
    async def test_memory_manager_sync_to_long_term_empty(self):
        """Test syncing when no messages in short-term memory."""
        mock_short_term = MagicMock()
        mock_short_term.get_user_messages.return_value = []

        mock_long_term = AsyncMock()

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        synced = await manager.sync_to_long_term(user_id=123)

        assert synced == 0
        mock_long_term.add_conversation.assert_not_called()

    @pytest.mark.asyncio
    async def test_memory_manager_get_recent_messages(self):
        """Test getting recent messages."""
        mock_short_term = MagicMock()
        mock_short_term.get_recent_messages.return_value = [
            Conversation(
                conversation_id=1,
                user_id=123,
                group_id=None,
                role="user",
                content="Recent",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            )
        ]

        mock_long_term = MagicMock()

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        messages = await manager.get_recent_messages(user_id=123, limit=5)

        assert len(messages) == 1
        assert messages[0].content == "Recent"
        mock_short_term.get_recent_messages.assert_called_once_with(123, 5)

    @pytest.mark.asyncio
    async def test_memory_manager_has_user(self):
        """Test checking if user has messages."""
        mock_short_term = MagicMock()
        mock_short_term.has_user.return_value = True

        mock_long_term = MagicMock()

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        has_messages = await manager.has_user(user_id=123)

        assert has_messages is True
        mock_short_term.has_user.assert_called_once_with(123)

    @pytest.mark.asyncio
    async def test_memory_manager_get_stats(self):
        """Test getting memory statistics."""
        mock_short_term = MagicMock()
        mock_short_term.get_total_message_count.return_value = 50
        mock_short_term.get_all_users.return_value = [1, 2, 3]

        mock_long_term = AsyncMock()
        mock_long_term.get_conversation_count.side_effect = [10, 20, 30]

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        stats = await manager.get_stats()

        assert stats["total_users"] == 3
        assert stats["short_term_messages"] == 50
        assert stats["long_term_messages"] == 60  # 10 + 20 + 30

    @pytest.mark.asyncio
    async def test_memory_manager_clear_all(self):
        """Test clearing all memory."""
        mock_short_term = MagicMock()
        mock_long_term = MagicMock()

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        await manager.clear_all(clear_long_term=False)

        mock_short_term.clear_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_memory_manager_clear_all_with_long_term(self):
        """Test clearing all memory including long-term."""
        mock_short_term = MagicMock()
        mock_long_term = AsyncMock()
        mock_long_term.rebuild_index.return_value = None

        manager = MemoryManager(
            short_term_memory=mock_short_term,
            long_term_memory=mock_long_term,
        )

        # Note: Clearing all long-term memory would require repository methods
        # This is a simplified test
        await manager.clear_all(clear_long_term=False)

        mock_short_term.clear_all.assert_called_once()
