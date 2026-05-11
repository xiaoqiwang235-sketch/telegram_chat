"""Conversation model for storing chat messages."""

from dataclasses import dataclass
from typing import Any

# Valid conversation roles
VALID_ROLES = {"user", "assistant", "system"}


@dataclass
class Conversation:
    """Represents a conversation message.

    Attributes:
        conversation_id: Unique conversation identifier
        user_id: Telegram user ID
        group_id: Telegram group chat ID (None for private chats)
        role: Message role (user, assistant, or system)
        content: Message content
        timestamp: Message timestamp
        message_id: Telegram message ID
        style_id: ID of the style used for the message
    """

    conversation_id: int
    user_id: int
    group_id: int | None
    role: str
    content: str
    timestamp: str
    message_id: int | None
    style_id: int | None

    def __post_init__(self) -> None:
        """Validate conversation role after initialization."""
        if self.role not in VALID_ROLES:
            raise ValueError(
                f"Invalid role '{self.role}'. Must be one of {VALID_ROLES}"
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert Conversation model to dictionary.

        Returns:
            Dictionary representation of the conversation
        """
        return {
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "group_id": self.group_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
            "message_id": self.message_id,
            "style_id": self.style_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Conversation":
        """Create Conversation model from dictionary.

        Args:
            data: Dictionary containing conversation data

        Returns:
            Conversation instance
        """
        return cls(
            conversation_id=data["conversation_id"],
            user_id=data["user_id"],
            group_id=data.get("group_id"),
            role=data["role"],
            content=data["content"],
            timestamp=data["timestamp"],
            message_id=data.get("message_id"),
            style_id=data.get("style_id"),
        )

    def __repr__(self) -> str:
        """Return string representation of Conversation.

        Returns:
            String representation
        """
        return (
            f"Conversation(conversation_id={self.conversation_id}, "
            f"user_id={self.user_id}, role={self.role}, "
            f"content={self.content[:50]}...)"
        )
