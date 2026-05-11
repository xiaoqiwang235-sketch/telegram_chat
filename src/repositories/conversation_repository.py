"""Conversation repository for database operations."""

from typing import List

from src.database.connection_pool import ConnectionPool
from src.models.conversation import Conversation
from src.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository):
    """Repository for Conversation model operations."""

    async def create(self, conversation: Conversation) -> Conversation:
        """Create a new conversation.

        Args:
            conversation: Conversation to create

        Returns:
            Created conversation
        """
        query = """
            INSERT INTO conversations (user_id, group_id, role, content, timestamp, message_id, style_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            conversation.user_id,
            conversation.group_id,
            conversation.role,
            conversation.content,
            conversation.timestamp,
            conversation.message_id,
            conversation.style_id,
        )

        await self._execute_write(query, params)
        return conversation

    async def get_by_id(self, conversation_id: int) -> Conversation | None:
        """Get conversation by ID.

        Args:
            conversation_id: Conversation ID to search for

        Returns:
            Conversation if found, None otherwise
        """
        query = """
            SELECT conversation_id, user_id, group_id, role, content, timestamp, message_id, style_id
            FROM conversations
            WHERE conversation_id = %s
        """
        result = await self._execute_query_one(query, (conversation_id,))

        if result:
            return self._row_to_conversation(result)
        return None

    async def get_by_user_id(
        self, user_id: int, limit: int = 100
    ) -> List[Conversation]:
        """Get conversations by user ID.

        Args:
            user_id: User ID to search for
            limit: Maximum number of results

        Returns:
            List of conversations
        """
        query = """
            SELECT conversation_id, user_id, group_id, role, content, timestamp, message_id, style_id
            FROM conversations
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        results = await self._execute_query(query, (user_id, limit))
        return [self._row_to_conversation(row) for row in results]

    async def get_by_group_id(
        self, group_id: int, limit: int = 100
    ) -> List[Conversation]:
        """Get conversations by group ID.

        Args:
            group_id: Group ID to search for
            limit: Maximum number of results

        Returns:
            List of conversations
        """
        query = """
            SELECT conversation_id, user_id, group_id, role, content, timestamp, message_id, style_id
            FROM conversations
            WHERE group_id = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        results = await self._execute_query(query, (group_id, limit))
        return [self._row_to_conversation(row) for row in results]

    async def get_recent_by_user(
        self, user_id: int, limit: int = 10
    ) -> List[Conversation]:
        """Get recent conversations for a user.

        Args:
            user_id: User ID to search for
            limit: Maximum number of results

        Returns:
            List of recent conversations
        """
        return await self.get_by_user_id(user_id, limit)

    async def delete(self, conversation_id: int) -> bool:
        """Delete a conversation.

        Args:
            conversation_id: Conversation ID to delete

        Returns:
            True if deleted, False if not found
        """
        query = "DELETE FROM conversations WHERE conversation_id = %s"
        rows_affected = await self._execute_write(query, (conversation_id,))
        return rows_affected > 0

    async def delete_by_user(self, user_id: int) -> int:
        """Delete all conversations for a user.

        Args:
            user_id: User ID to delete conversations for

        Returns:
            Number of conversations deleted
        """
        query = "DELETE FROM conversations WHERE user_id = %s"
        return await self._execute_write(query, (user_id,))

    async def count_by_user(self, user_id: int) -> int:
        """Count conversations for a user.

        Args:
            user_id: User ID to count conversations for

        Returns:
            Number of conversations
        """
        query = "SELECT COUNT(*) FROM conversations WHERE user_id = %s"
        result = await self._execute_query_one(query, (user_id,))
        if result:
            return result[0]
        return 0

    async def exists(self, conversation_id: int) -> bool:
        """Check if conversation exists.

        Args:
            conversation_id: Conversation ID to check

        Returns:
            True if conversation exists, False otherwise
        """
        query = "SELECT 1 FROM conversations WHERE conversation_id = %s"
        result = await self._execute_query_one(query, (conversation_id,))
        return result is not None

    async def get_conversation_history(
        self, user_id: int, group_id: int | None = None, limit: int = 50
    ) -> List[Conversation]:
        """Get conversation history for a user/group.

        Args:
            user_id: User ID to search for
            group_id: Optional group ID to filter by
            limit: Maximum number of results

        Returns:
            List of conversations in chronological order
        """
        if group_id is not None:
            query = """
                SELECT conversation_id, user_id, group_id, role, content, timestamp, message_id, style_id
                FROM conversations
                WHERE user_id = %s AND group_id = %s
                ORDER BY timestamp ASC
                LIMIT %s
            """
            results = await self._execute_query(query, (user_id, group_id, limit))
        else:
            query = """
                SELECT conversation_id, user_id, group_id, role, content, timestamp, message_id, style_id
                FROM conversations
                WHERE user_id = %s AND group_id IS NULL
                ORDER BY timestamp ASC
                LIMIT %s
            """
            results = await self._execute_query(query, (user_id, limit))

        return [self._row_to_conversation(row) for row in results]

    def _row_to_conversation(self, row: tuple) -> Conversation:
        """Convert database row to Conversation object.

        Args:
            row: Database row tuple

        Returns:
            Conversation instance
        """
        return Conversation(
            conversation_id=row[0],
            user_id=row[1],
            group_id=row[2],
            role=row[3],
            content=row[4],
            timestamp=row[5],
            message_id=row[6],
            style_id=row[7],
        )
