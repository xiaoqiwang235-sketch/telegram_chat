"""Short-term memory implementation using in-memory storage."""

from collections import deque
from typing import Deque, List

from src.models.conversation import Conversation


class ShortTermMemory:
    """Short-term memory for storing recent conversations in memory.

    Attributes:
        max_messages: Maximum number of messages per user
        _messages: Dictionary mapping user_id to message queue
    """

    def __init__(self, max_messages: int = 50) -> None:
        """Initialize short-term memory.

        Args:
            max_messages: Maximum messages to store per user (default: 50)
        """
        self.max_messages = max_messages
        self._messages: dict[int, Deque[Conversation]] = {}

    def add(self, user_id: int, conversation: Conversation) -> None:
        """Add a conversation to short-term memory.

        Args:
            user_id: User ID
            conversation: Conversation to add
        """
        if user_id not in self._messages:
            self._messages[user_id] = deque(maxlen=self.max_messages)

        self._messages[user_id].append(conversation)

    def get_user_messages(self, user_id: int, limit: int | None = None) -> List[Conversation]:
        """Get messages for a user.

        Args:
            user_id: User ID to get messages for
            limit: Optional limit on number of messages

        Returns:
            List of conversations (ordered oldest to newest)
        """
        if user_id not in self._messages:
            return []

        messages = list(self._messages[user_id])

        if limit is not None:
            messages = messages[:limit]

        return messages

    def get_recent_messages(self, user_id: int, limit: int = 10) -> List[Conversation]:
        """Get recent messages for a user.

        Args:
            user_id: User ID to get messages for
            limit: Number of recent messages to return

        Returns:
            List of recent conversations
        """
        if user_id not in self._messages:
            return []

        messages = list(self._messages[user_id])
        start = max(0, len(messages) - limit)
        return messages[start:]

    def clear_user(self, user_id: int) -> None:
        """Clear all messages for a user.

        Args:
            user_id: User ID to clear messages for
        """
        if user_id in self._messages:
            del self._messages[user_id]

    def clear_all(self) -> None:
        """Clear all messages from memory."""
        self._messages.clear()

    def get_message_count(self, user_id: int) -> int:
        """Get number of messages for a user.

        Args:
            user_id: User ID to count messages for

        Returns:
            Number of messages
        """
        if user_id not in self._messages:
            return 0
        return len(self._messages[user_id])

    def get_total_message_count(self) -> int:
        """Get total number of messages across all users.

        Returns:
            Total message count
        """
        return sum(len(messages) for messages in self._messages.values())

    def has_user(self, user_id: int) -> bool:
        """Check if user has any messages in memory.

        Args:
            user_id: User ID to check

        Returns:
            True if user has messages, False otherwise
        """
        return user_id in self._messages and len(self._messages[user_id]) > 0

    def get_all_users(self) -> List[int]:
        """Get all users with messages in memory.

        Returns:
            List of user IDs
        """
        return list(self._messages.keys())
