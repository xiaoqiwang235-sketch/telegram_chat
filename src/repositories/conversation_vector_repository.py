"""ConversationVector repository for database operations."""

import numpy as np
from typing import List, Tuple

from src.database.connection_pool import ConnectionPool
from src.repositories.base_repository import BaseRepository


class ConversationVectorRepository(BaseRepository):
    """Repository for conversation vector operations."""

    async def create(
        self, conversation_id: int, vector: np.ndarray, vector_id: str
    ) -> bool:
        """Create a new conversation vector.

        Args:
            conversation_id: Conversation ID
            vector: Vector embedding (numpy array)
            vector_id: Unique vector identifier

        Returns:
            True if created successfully
        """
        query = """
            INSERT INTO conversation_vectors (conversation_id, vector, vector_id)
            VALUES (%s, %s, %s)
        """
        vector_bytes = vector.tobytes()
        params = (conversation_id, vector_bytes, vector_id)

        await self._execute_write(query, params)
        return True

    async def get_by_conversation_id(
        self, conversation_id: int
    ) -> np.ndarray | None:
        """Get vector by conversation ID.

        Args:
            conversation_id: Conversation ID to search for

        Returns:
            Vector if found, None otherwise
        """
        query = """
            SELECT vector
            FROM conversation_vectors
            WHERE conversation_id = %s
        """
        result = await self._execute_query_one(query, (conversation_id,))

        if result:
            return self._bytes_to_vector(result[0])
        return None

    async def get_all_vectors(self, limit: int = 100) -> List[np.ndarray]:
        """Get all vectors.

        Args:
            limit: Maximum number of vectors to return

        Returns:
            List of vectors
        """
        query = """
            SELECT vector
            FROM conversation_vectors
            LIMIT %s
        """
        results = await self._execute_query(query, (limit,))
        return [self._bytes_to_vector(row[0]) for row in results if row[0]]

    async def delete(self, conversation_id: int) -> bool:
        """Delete a conversation vector.

        Args:
            conversation_id: Conversation ID to delete

        Returns:
            True if deleted, False if not found
        """
        query = "DELETE FROM conversation_vectors WHERE conversation_id = %s"
        rows_affected = await self._execute_write(query, (conversation_id,))
        return rows_affected > 0

    async def count(self) -> int:
        """Count total number of vectors.

        Returns:
            Total vector count
        """
        query = "SELECT COUNT(*) FROM conversation_vectors"
        result = await self._execute_query_one(query)
        if result:
            return result[0]
        return 0

    async def exists(self, conversation_id: int) -> bool:
        """Check if conversation vector exists.

        Args:
            conversation_id: Conversation ID to check

        Returns:
            True if vector exists, False otherwise
        """
        query = "SELECT 1 FROM conversation_vectors WHERE conversation_id = %s"
        result = await self._execute_query_one(query, (conversation_id,))
        return result is not None

    async def get_by_vector_id(self, vector_id: str) -> int | None:
        """Get conversation ID by vector ID.

        Args:
            vector_id: Vector ID to search for

        Returns:
            Conversation ID if found, None otherwise
        """
        query = """
            SELECT conversation_id
            FROM conversation_vectors
            WHERE vector_id = %s
        """
        result = await self._execute_query_one(query, (vector_id,))
        if result:
            return result[0]
        return None

    async def batch_insert(
        self, vectors: List[Tuple[int, np.ndarray, str]]
    ) -> int:
        """Batch insert conversation vectors.

        Args:
            vectors: List of tuples (conversation_id, vector, vector_id)

        Returns:
            Number of vectors inserted
        """
        query = """
            INSERT INTO conversation_vectors (conversation_id, vector, vector_id)
            VALUES (%s, %s, %s)
        """
        params_list = [
            (conv_id, vector.tobytes(), vec_id)
            for conv_id, vector, vec_id in vectors
        ]

        return await self._execute_batch(query, params_list)

    async def delete_by_conversation_id(self, conversation_id: int) -> int:
        """Delete all vectors for a conversation.

        Args:
            conversation_id: Conversation ID to delete vectors for

        Returns:
            Number of vectors deleted
        """
        query = "DELETE FROM conversation_vectors WHERE conversation_id = %s"
        return await self._execute_write(query, (conversation_id,))

    def _bytes_to_vector(self, vector_bytes: bytes) -> np.ndarray:
        """Convert bytes to numpy array.

        Args:
            vector_bytes: Vector as bytes

        Returns:
            Vector as numpy array
        """
        return np.frombuffer(vector_bytes, dtype=np.float32)
