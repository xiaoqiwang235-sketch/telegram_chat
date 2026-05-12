"""Memory manager integrating short-term and long-term memory."""

from typing import List, Dict, Optional

from src.memory.short_term_memory import ShortTermMemory
from src.memory.long_term_memory import LongTermMemory
from src.models.conversation import Conversation


class MemoryManager:
    """Unified memory manager combining short-term and long-term memory.

    Attributes:
        short_term_memory: Short-term in-memory storage
        long_term_memory: Long-term persistent storage
    """

    def __init__(
        self,
        short_term_memory: ShortTermMemory,
        long_term_memory: LongTermMemory,
    ) -> None:
        """Initialize memory manager.

        Args:
            short_term_memory: Short-term memory instance
            long_term_memory: Long-term memory instance
        """
        self.short_term_memory = short_term_memory
        self.long_term_memory = long_term_memory

    async def add_message(
        self, conversation: Conversation, save_long_term: bool = False
    ) -> None:
        """Add a message to memory.

        Args:
            conversation: Conversation to add
            save_long_term: Whether to save to long-term memory
        """
        # Always add to short-term memory
        self.short_term_memory.add(conversation.user_id, conversation)

        # Optionally save to long-term memory
        if save_long_term:
            await self.long_term_memory.add_conversation(conversation)

    async def get_context(
        self,
        user_id: int,
        group_id: Optional[int] = None,
        limit: int = 50,
    ) -> List[Conversation]:
        """Get conversation context combining both memories.

        Args:
            user_id: User ID
            group_id: Optional group ID
            limit: Maximum number of conversations

        Returns:
            Combined conversation history (long-term first, then short-term)
        """
        # Get long-term history
        long_term = await self.long_term_memory.get_conversation_history(
            user_id=user_id, group_id=group_id, limit=limit
        )

        # Get short-term history
        short_term = self.short_term_memory.get_user_messages(user_id, limit=limit)

        # Combine (long-term first for context)
        combined = long_term + short_term

        # Limit total results
        return combined[:limit]

    async def search(
        self,
        query: str,
        user_id: int,
        group_id: Optional[int] = None,
        k: int = 5,
    ) -> List[Dict]:
        """Search for similar conversations.

        Args:
            query: Search query
            user_id: User ID
            group_id: Optional group ID
            k: Number of results

        Returns:
            List of similar conversations
        """
        return await self.long_term_memory.search_similar(
            query=query,
            user_id=user_id,
            group_id=group_id,
            k=k,
        )

    async def clear_user(
        self, user_id: int, clear_long_term: bool = False
    ) -> None:
        """Clear memory for a user.

        Args:
            user_id: User ID to clear
            clear_long_term: Whether to clear long-term memory
        """
        # Always clear short-term memory
        self.short_term_memory.clear_user(user_id)

        # Optionally clear long-term memory
        if clear_long_term:
            await self.long_term_memory.delete_user_history(user_id)

    async def get_message_count(self, user_id: int) -> int:
        """Get total message count for a user.

        Args:
            user_id: User ID

        Returns:
            Total message count
        """
        short_term_count = self.short_term_memory.get_message_count(user_id)
        long_term_count = await self.long_term_memory.get_conversation_count(user_id)

        return short_term_count + long_term_count

    async def sync_to_long_term(self, user_id: int) -> int:
        """Sync short-term memory to long-term storage.

        Args:
            user_id: User ID to sync

        Returns:
            Number of messages synced
        """
        # Get all short-term messages for user
        messages = self.short_term_memory.get_user_messages(user_id)

        synced_count = 0
        for message in messages:
            await self.long_term_memory.add_conversation(message)
            synced_count += 1

        return synced_count

    async def get_recent_messages(
        self, user_id: int, limit: int = 10
    ) -> List[Conversation]:
        """Get recent messages from short-term memory.

        Args:
            user_id: User ID
            limit: Number of messages

        Returns:
            Recent messages
        """
        return self.short_term_memory.get_recent_messages(user_id, limit)

    async def has_user(self, user_id: int) -> bool:
        """Check if user has any messages in memory.

        Args:
            user_id: User ID

        Returns:
            True if user has messages
        """
        return self.short_term_memory.has_user(user_id)

    async def get_stats(self) -> Dict[str, int]:
        """Get memory statistics.

        Returns:
            Dictionary with memory stats
        """
        all_users = self.short_term_memory.get_all_users()

        short_term_total = self.short_term_memory.get_total_message_count()

        long_term_total = 0
        for user_id in all_users:
            long_term_total += await self.long_term_memory.get_conversation_count(
                user_id
            )

        return {
            "total_users": len(all_users),
            "short_term_messages": short_term_total,
            "long_term_messages": long_term_total,
            "total_messages": short_term_total + long_term_total,
        }

    async def clear_all(self, clear_long_term: bool = False) -> None:
        """Clear all memory.

        Args:
            clear_long_term: Whether to clear long-term memory
        """
        self.short_term_memory.clear_all()

        if clear_long_term:
            # Note: Clearing all long-term memory would require
            # iterating through all users and deleting their history
            # This is a potentially expensive operation
            pass
