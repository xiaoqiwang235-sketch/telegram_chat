"""Unit tests for Message model."""

import pytest

from src.models.message import Message


class TestMessage:
    """Test suite for Message model."""

    def test_message_initialization(self):
        """Test Message model initialization with all fields."""
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content="Hello, how are you?",
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )

        assert message.message_id == 1001
        assert message.user_id == 123456789
        assert message.group_id is None
        assert message.content == "Hello, how are you?"
        assert message.timestamp == "2024-01-01 12:00:00"
        assert message.is_edited is False
        assert message.reply_to_message_id is None

    def test_message_initialization_group_chat(self):
        """Test Message model initialization for group chat."""
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=987654321,
            content="Hello group!",
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )

        assert message.group_id == 987654321

    def test_message_with_reply(self):
        """Test Message model with reply to another message."""
        message = Message(
            message_id=1002,
            user_id=123456789,
            group_id=None,
            content="This is a reply",
            timestamp="2024-01-01 12:00:01",
            is_edited=False,
            reply_to_message_id=1001,
        )

        assert message.reply_to_message_id == 1001

    def test_message_edited(self):
        """Test Message model with edited flag."""
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content="Edited content",
            timestamp="2024-01-01 12:00:00",
            is_edited=True,
            reply_to_message_id=None,
        )

        assert message.is_edited is True

    def test_message_to_dict(self):
        """Test converting Message model to dictionary."""
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content="Hello, how are you?",
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )

        msg_dict = message.to_dict()

        assert isinstance(msg_dict, dict)
        assert msg_dict["message_id"] == 1001
        assert msg_dict["user_id"] == 123456789
        assert msg_dict["content"] == "Hello, how are you?"
        assert msg_dict["is_edited"] is False

    def test_message_from_dict(self):
        """Test creating Message model from dictionary."""
        msg_dict = {
            "message_id": 1001,
            "user_id": 123456789,
            "group_id": None,
            "content": "Hello, how are you?",
            "timestamp": "2024-01-01 12:00:00",
            "is_edited": False,
            "reply_to_message_id": None,
        }

        message = Message.from_dict(msg_dict)

        assert message.message_id == 1001
        assert message.user_id == 123456789
        assert message.content == "Hello, how are you?"
        assert message.is_edited is False

    def test_message_equality(self):
        """Test Message model equality comparison."""
        msg1 = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content="Hello",
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )
        msg2 = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content="Hello",
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )
        msg3 = Message(
            message_id=1002,
            user_id=987654321,
            group_id=None,
            content="Hi",
            timestamp="2024-01-01 12:00:01",
            is_edited=False,
            reply_to_message_id=None,
        )

        assert msg1 == msg2
        assert msg1 != msg3

    def test_message_repr(self):
        """Test Message model string representation."""
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content="Hello, how are you?",
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )

        repr_str = repr(message)

        assert "Message" in repr_str
        assert "1001" in repr_str
        assert "123456789" in repr_str

    def test_message_empty_content(self):
        """Test Message model with empty content."""
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content="",
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )

        assert message.content == ""

    def test_message_long_content(self):
        """Test Message model with long content."""
        long_content = "A" * 10000
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content=long_content,
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )

        assert message.content == long_content

    def test_message_special_characters(self):
        """Test Message model with special characters."""
        special_content = "Hello! @#$%^&*()_+-=[]{}|;:,.<>?🎉"
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content=special_content,
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )

        assert message.content == special_content

    def test_message_unicode_content(self):
        """Test Message model with unicode content."""
        unicode_content = "你好！🌍🌎🌏"
        message = Message(
            message_id=1001,
            user_id=123456789,
            group_id=None,
            content=unicode_content,
            timestamp="2024-01-01 12:00:00",
            is_edited=False,
            reply_to_message_id=None,
        )

        assert message.content == unicode_content
