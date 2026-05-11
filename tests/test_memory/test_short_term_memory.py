"""Unit tests for Short-Term Memory module."""

import pytest
from datetime import datetime

from src.memory.short_term_memory import ShortTermMemory
from src.models.conversation import Conversation


class TestShortTermMemory:
    """Test suite for ShortTermMemory class."""

    def test_short_term_memory_initialization(self):
        """Test ShortTermMemory initialization."""
        memory = ShortTermMemory(max_messages=50)

        assert memory.max_messages == 50
        assert len(memory._messages) == 0

    def test_short_term_memory_initialization_default(self):
        """Test ShortTermMemory initialization with default values."""
        memory = ShortTermMemory()

        assert memory.max_messages == 50
        assert len(memory._messages) == 0

    def test_short_term_memory_add_message(self):
        """Test adding a message to short-term memory."""
        memory = ShortTermMemory(max_messages=10)
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

        memory.add(123, conversation)

        assert 123 in memory._messages
        assert len(memory._messages[123]) == 1
        assert memory._messages[123][0] == conversation

    def test_short_term_memory_add_multiple_messages(self):
        """Test adding multiple messages for a user."""
        memory = ShortTermMemory(max_messages=10)

        for i in range(3):
            conversation = Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp="2024-01-01 12:00:00",
                message_id=1000 + i,
                style_id=1,
            )
            memory.add(123, conversation)

        assert len(memory._messages[123]) == 3

    def test_short_term_memory_add_multiple_users(self):
        """Test adding messages for multiple users."""
        memory = ShortTermMemory(max_messages=10)

        # User 1
        conv1 = Conversation(
            conversation_id=1,
            user_id=1,
            group_id=None,
            role="user",
            content="Hello",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )
        memory.add(1, conv1)

        # User 2
        conv2 = Conversation(
            conversation_id=2,
            user_id=2,
            group_id=None,
            role="user",
            content="Hi",
            timestamp="2024-01-01 12:00:01",
            message_id=1002,
            style_id=1,
        )
        memory.add(2, conv2)

        assert len(memory._messages[1]) == 1
        assert len(memory._messages[2]) == 1

    def test_short_term_memory_max_messages_limit(self):
        """Test enforcing max messages limit."""
        memory = ShortTermMemory(max_messages=3)

        # Add 5 messages
        for i in range(5):
            conversation = Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp="2024-01-01 12:00:00",
                message_id=1000 + i,
                style_id=1,
            )
            memory.add(123, conversation)

        # Should only keep last 3 messages
        assert len(memory._messages[123]) == 3
        assert memory._messages[123][0].content == "Message 2"
        assert memory._messages[123][1].content == "Message 3"
        assert memory._messages[123][2].content == "Message 4"

    def test_short_term_memory_get_user_messages(self):
        """Test getting messages for a user."""
        memory = ShortTermMemory(max_messages=10)

        for i in range(3):
            conversation = Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp="2024-01-01 12:00:0{i}",
                message_id=1000 + i,
                style_id=1,
            )
            memory.add(123, conversation)

        messages = memory.get_user_messages(123)

        assert len(messages) == 3
        assert messages[0].content == "Message 0"
        assert messages[1].content == "Message 1"
        assert messages[2].content == "Message 2"

    def test_short_term_memory_get_user_messages_empty(self):
        """Test getting messages for user with no messages."""
        memory = ShortTermMemory(max_messages=10)

        messages = memory.get_user_messages(123)

        assert messages == []

    def test_short_term_memory_get_user_messages_with_limit(self):
        """Test getting limited number of messages."""
        memory = ShortTermMemory(max_messages=10)

        for i in range(5):
            conversation = Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp="2024-01-01 12:00:0{i}",
                message_id=1000 + i,
                style_id=1,
            )
            memory.add(123, conversation)

        messages = memory.get_user_messages(123, limit=3)

        assert len(messages) == 3
        assert messages[0].content == "Message 0"

    def test_short_term_memory_clear_user(self):
        """Test clearing messages for a user."""
        memory = ShortTermMemory(max_messages=10)

        for i in range(3):
            conversation = Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp="2024-01-01 12:00:0{i}",
                message_id=1000 + i,
                style_id=1,
            )
            memory.add(123, conversation)

        assert len(memory._messages[123]) == 3

        memory.clear_user(123)

        assert 123 not in memory._messages

    def test_short_term_memory_clear_all(self):
        """Test clearing all messages."""
        memory = ShortTermMemory(max_messages=10)

        # Add messages for multiple users
        for user_id in [1, 2, 3]:
            for i in range(2):
                conversation = Conversation(
                    conversation_id=i,
                    user_id=user_id,
                    group_id=None,
                    role="user",
                    content=f"Message {i}",
                    timestamp="2024-01-01 12:00:0{i}",
                    message_id=1000 + i,
                    style_id=1,
                )
                memory.add(user_id, conversation)

        assert len(memory._messages) == 3

        memory.clear_all()

        assert len(memory._messages) == 0

    def test_short_term_memory_get_message_count(self):
        """Test getting message count for user."""
        memory = ShortTermMemory(max_messages=10)

        assert memory.get_message_count(123) == 0

        for i in range(3):
            conversation = Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp="2024-01-01 12:00:0{i}",
                message_id=1000 + i,
                style_id=1,
            )
            memory.add(123, conversation)

        assert memory.get_message_count(123) == 3

    def test_short_term_memory_get_total_message_count(self):
        """Test getting total message count across all users."""
        memory = ShortTermMemory(max_messages=10)

        # Add messages for multiple users
        for user_id in [1, 2, 3]:
            for i in range(2):
                conversation = Conversation(
                    conversation_id=i,
                    user_id=user_id,
                    group_id=None,
                    role="user",
                    content=f"Message {i}",
                    timestamp="2024-01-01 12:00:0{i}",
                    message_id=1000 + i,
                    style_id=1,
                )
                memory.add(user_id, conversation)

        assert memory.get_total_message_count() == 6

    def test_short_term_memory_get_recent_messages(self):
        """Test getting recent messages."""
        memory = ShortTermMemory(max_messages=10)

        for i in range(5):
            conversation = Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp=f"2024-01-01 12:00:0{i}",
                message_id=1000 + i,
                style_id=1,
            )
            memory.add(123, conversation)

        recent = memory.get_recent_messages(123, limit=3)

        assert len(recent) == 3
        assert recent[0].content == "Message 2"
        assert recent[1].content == "Message 3"
        assert recent[2].content == "Message 4"

    def test_short_term_memory_has_user(self):
        """Test checking if user has messages."""
        memory = ShortTermMemory(max_messages=10)

        assert memory.has_user(123) is False

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
        memory.add(123, conversation)

        assert memory.has_user(123) is True

    def test_short_term_memory_get_all_users(self):
        """Test getting all users with messages."""
        memory = ShortTermMemory(max_messages=10)

        # Add messages for multiple users
        for user_id in [1, 2, 3]:
            conversation = Conversation(
                conversation_id=1,
                user_id=user_id,
                group_id=None,
                role="user",
                content="Hello",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            )
            memory.add(user_id, conversation)

        users = memory.get_all_users()

        assert len(users) == 3
        assert 1 in users
        assert 2 in users
        assert 3 in users

    def test_short_term_memory_conversation_order(self):
        """Test that conversations maintain insertion order."""
        memory = ShortTermMemory(max_messages=10)

        timestamps = [
            "2024-01-01 12:00:00",
            "2024-01-01 12:00:01",
            "2024-01-01 12:00:02",
        ]

        for i, timestamp in enumerate(timestamps):
            conversation = Conversation(
                conversation_id=i,
                user_id=123,
                group_id=None,
                role="user",
                content=f"Message {i}",
                timestamp=timestamp,
                message_id=1000 + i,
                style_id=1,
            )
            memory.add(123, conversation)

        messages = memory.get_user_messages(123)

        assert messages[0].timestamp == "2024-01-01 12:00:00"
        assert messages[1].timestamp == "2024-01-01 12:00:01"
        assert messages[2].timestamp == "2024-01-01 12:00:02"
