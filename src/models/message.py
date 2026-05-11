"""Message model for storing Telegram messages."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    """Represents a Telegram message.

    Attributes:
        message_id: Unique Telegram message ID
        user_id: Telegram user ID who sent the message
        group_id: Telegram group chat ID (None for private chats)
        content: Message content/text
        timestamp: Message timestamp
        is_edited: Whether the message has been edited
        reply_to_message_id: ID of the message this replies to (None if not a reply)
    """

    message_id: int
    user_id: int
    group_id: int | None
    content: str
    timestamp: str
    is_edited: bool
    reply_to_message_id: int | None

    def to_dict(self) -> dict[str, Any]:
        """Convert Message model to dictionary.

        Returns:
            Dictionary representation of the message
        """
        return {
            "message_id": self.message_id,
            "user_id": self.user_id,
            "group_id": self.group_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "is_edited": self.is_edited,
            "reply_to_message_id": self.reply_to_message_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Message":
        """Create Message model from dictionary.

        Args:
            data: Dictionary containing message data

        Returns:
            Message instance
        """
        return cls(
            message_id=data["message_id"],
            user_id=data["user_id"],
            group_id=data.get("group_id"),
            content=data["content"],
            timestamp=data["timestamp"],
            is_edited=data.get("is_edited", False),
            reply_to_message_id=data.get("reply_to_message_id"),
        )

    def __repr__(self) -> str:
        """Return string representation of Message.

        Returns:
            String representation
        """
        return (
            f"Message(message_id={self.message_id}, user_id={self.user_id}, "
            f"content={self.content[:50]}...)"
        )
