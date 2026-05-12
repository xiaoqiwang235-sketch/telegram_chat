"""Unit tests for Conversation Repository module."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.models.conversation import Conversation
from src.repositories.conversation_repository import ConversationRepository


class TestConversationRepository:
    """Test suite for ConversationRepository class."""

    @pytest.mark.asyncio
    async def test_conversation_repository_create(self):
        """Test creating a new conversation."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="user",
            content="Hello",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        created_conversation = await repo.create(conversation)

        assert created_conversation.conversation_id == 1
        assert created_conversation.user_id == 123456789
        assert created_conversation.content == "Hello"

    @pytest.mark.asyncio
    async def test_conversation_repository_get_by_id(self):
        """Test getting conversation by ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(
                1,
                123456789,
                None,
                "user",
                "Hello",
                "2024-01-01 12:00:00",
                1001,
                1,
            )
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        conversation = await repo.get_by_id(1)

        assert conversation is not None
        assert conversation.conversation_id == 1
        assert conversation.user_id == 123456789
        assert conversation.content == "Hello"

    @pytest.mark.asyncio
    async def test_conversation_repository_get_by_user_id(self):
        """Test getting conversations by user ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (
                    1,
                    123456789,
                    None,
                    "user",
                    "Hello",
                    "2024-01-01 12:00:00",
                    1001,
                    1,
                ),
                (
                    2,
                    123456789,
                    None,
                    "assistant",
                    "Hi there",
                    "2024-01-01 12:00:01",
                    1002,
                    1,
                ),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        conversations = await repo.get_by_user_id(123456789, limit=10)

        assert len(conversations) == 2
        assert conversations[0].user_id == 123456789
        assert conversations[1].role == "assistant"

    @pytest.mark.asyncio
    async def test_conversation_repository_get_by_group_id(self):
        """Test getting conversations by group ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (
                    1,
                    123456789,
                    987654321,
                    "user",
                    "Hello group",
                    "2024-01-01 12:00:00",
                    1001,
                    1,
                ),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        conversations = await repo.get_by_group_id(987654321, limit=10)

        assert len(conversations) == 1
        assert conversations[0].group_id == 987654321
        assert conversations[0].content == "Hello group"

    @pytest.mark.asyncio
    async def test_conversation_repository_get_recent_by_user(self):
        """Test getting recent conversations by user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (
                    1,
                    123456789,
                    None,
                    "user",
                    "Latest message",
                    "2024-01-01 12:00:00",
                    1001,
                    1,
                ),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        conversations = await repo.get_recent_by_user(123456789, limit=5)

        assert len(conversations) == 1
        assert conversations[0].content == "Latest message"

    @pytest.mark.asyncio
    async def test_conversation_repository_delete(self):
        """Test deleting a conversation."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        result = await repo.delete(1)

        assert result is True

    @pytest.mark.asyncio
    async def test_conversation_repository_delete_by_user(self):
        """Test deleting all conversations for a user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 5
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        count = await repo.delete_by_user(123456789)

        assert count == 5

    @pytest.mark.asyncio
    async def test_conversation_repository_count_by_user(self):
        """Test counting conversations for a user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(10,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        count = await repo.count_by_user(123456789)

        assert count == 10

    @pytest.mark.asyncio
    async def test_conversation_repository_exists(self):
        """Test checking if conversation exists."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(1,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        exists = await repo.exists(1)

        assert exists is True

    @pytest.mark.asyncio
    async def test_conversation_repository_get_conversation_history(self):
        """Test getting conversation history for user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (
                    1,
                    123456789,
                    None,
                    "user",
                    "Hello",
                    "2024-01-01 12:00:00",
                    1001,
                    1,
                ),
                (
                    2,
                    123456789,
                    None,
                    "assistant",
                    "Hi",
                    "2024-01-01 12:00:01",
                    1002,
                    1,
                ),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        history = await repo.get_conversation_history(123456789, limit=10)

        assert len(history) == 2
        assert history[0].role == "user"
        assert history[1].role == "assistant"

    @pytest.mark.asyncio
    async def test_conversation_repository_get_by_group_id_empty(self):
        """Test getting conversations for group with no results."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        conversations = await repo.get_by_group_id(999999999, limit=10)

        assert len(conversations) == 0

    @pytest.mark.asyncio
    async def test_conversation_repository_delete_not_found(self):
        """Test deleting non-existent conversation."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 0
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = ConversationRepository(mock_pool)

        result = await repo.delete(999999)

        assert result is False
