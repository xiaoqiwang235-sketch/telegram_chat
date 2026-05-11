"""Unit tests for Conversation model."""

import pytest

from src.models.conversation import Conversation


class TestConversation:
    """Test suite for Conversation model."""

    def test_conversation_initialization(self):
        """Test Conversation model initialization with all fields."""
        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="user",
            content="Hello, how are you?",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        assert conversation.conversation_id == 1
        assert conversation.user_id == 123456789
        assert conversation.group_id is None
        assert conversation.role == "user"
        assert conversation.content == "Hello, how are you?"
        assert conversation.timestamp == "2024-01-01 12:00:00"
        assert conversation.message_id == 1001
        assert conversation.style_id == 1

    def test_conversation_initialization_group_chat(self):
        """Test Conversation model initialization for group chat."""
        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=987654321,
            role="user",
            content="Hello group!",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        assert conversation.group_id == 987654321

    def test_conversation_to_dict(self):
        """Test converting Conversation model to dictionary."""
        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="user",
            content="Hello, how are you?",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        conv_dict = conversation.to_dict()

        assert isinstance(conv_dict, dict)
        assert conv_dict["conversation_id"] == 1
        assert conv_dict["user_id"] == 123456789
        assert conv_dict["role"] == "user"
        assert conv_dict["content"] == "Hello, how are you?"

    def test_conversation_from_dict(self):
        """Test creating Conversation model from dictionary."""
        conv_dict = {
            "conversation_id": 1,
            "user_id": 123456789,
            "group_id": None,
            "role": "user",
            "content": "Hello, how are you?",
            "timestamp": "2024-01-01 12:00:00",
            "message_id": 1001,
            "style_id": 1,
        }

        conversation = Conversation.from_dict(conv_dict)

        assert conversation.conversation_id == 1
        assert conversation.user_id == 123456789
        assert conversation.role == "user"
        assert conversation.content == "Hello, how are you?"

    def test_conversation_equality(self):
        """Test Conversation model equality comparison."""
        conv1 = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="user",
            content="Hello",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )
        conv2 = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="user",
            content="Hello",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )
        conv3 = Conversation(
            conversation_id=2,
            user_id=987654321,
            group_id=None,
            role="user",
            content="Hi",
            timestamp="2024-01-01 12:00:01",
            message_id=1002,
            style_id=1,
        )

        assert conv1 == conv2
        assert conv1 != conv3

    def test_conversation_repr(self):
        """Test Conversation model string representation."""
        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="user",
            content="Hello, how are you?",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        repr_str = repr(conversation)

        assert "Conversation" in repr_str
        assert "1" in repr_str
        assert "123456789" in repr_str

    def test_conversation_invalid_role(self):
        """Test Conversation model with invalid role."""
        with pytest.raises(ValueError):
            Conversation(
                conversation_id=1,
                user_id=123456789,
                group_id=None,
                role="invalid_role",
                content="Hello",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            )

    def test_conversation_empty_content(self):
        """Test Conversation model with empty content."""
        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="user",
            content="",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        assert conversation.content == ""

    def test_conversation_long_content(self):
        """Test Conversation model with long content."""
        long_content = "A" * 10000
        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="user",
            content=long_content,
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        assert conversation.content == long_content

    def test_conversation_assistant_role(self):
        """Test Conversation model with assistant role."""
        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="assistant",
            content="Hello! How can I help you?",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        assert conversation.role == "assistant"

    def test_conversation_system_role(self):
        """Test Conversation model with system role."""
        conversation = Conversation(
            conversation_id=1,
            user_id=123456789,
            group_id=None,
            role="system",
            content="System message",
            timestamp="2024-01-01 12:00:00",
            message_id=1001,
            style_id=1,
        )

        assert conversation.role == "system"
