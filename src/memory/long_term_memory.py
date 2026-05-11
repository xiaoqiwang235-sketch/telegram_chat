"""Long-term memory implementation using database and Faiss."""

import numpy as np
from typing import List, Dict, Optional
import uuid

from src.memory.faiss_manager import FaissManager
from src.memory.embedding_client import EmbeddingClient
from src.models.conversation import Conversation
from src.repositories.conversation_repository import ConversationRepository
from src.repositories.conversation_vector_repository import ConversationVectorRepository


class LongTermMemory:
    """Long-term memory for storing and retrieving conversations.

    Attributes:
        embedding_client: Client for generating embeddings
        faiss_manager: Manager for vector similarity search
        conversation_repo: Repository for conversation persistence
        vector_repo: Repository for vector persistence
    """

    def __init__(
        self,
        embedding_client: EmbeddingClient,
        faiss_manager: FaissManager,
        conversation_repo: ConversationRepository,
        vector_repo: ConversationVectorRepository,
    ) -> None:
        """Initialize long-term memory.

        Args:
            embedding_client: Embedding generation client
            faiss_manager: Faiss index manager
            conversation_repo: Conversation repository
            vector_repo: Vector repository
        """
        self.embedding_client = embedding_client
        self.faiss_manager = faiss_manager
        self.conversation_repo = conversation_repo
        self.vector_repo = vector_repo

    async def add_conversation(self, conversation: Conversation) -> bool:
        """Add a conversation to long-term memory.

        Args:
            conversation: Conversation to add

        Returns:
            True if added successfully
        """
        # Generate embedding
        embedding = await self.embedding_client.generate_embedding(conversation.content)

        # Save conversation to database
        await self.conversation_repo.create(conversation)

        # Save vector to database
        vector_id = f"vec_{conversation.conversation_id}_{uuid.uuid4().hex[:8]}"
        await self.vector_repo.create(conversation.conversation_id, embedding, vector_id)

        # Add to Faiss index
        await self.faiss_manager.add_vector(
            vector_id=vector_id,
            conversation_id=conversation.conversation_id,
            vector=embedding,
        )

        return True

    async def search_similar(
        self,
        query: str,
        user_id: int,
        group_id: Optional[int] = None,
        k: int = 5,
    ) -> List[Dict]:
        """Search for similar conversations.

        Args:
            query: Search query
            user_id: User ID to filter by
            group_id: Optional group ID to filter by
            k: Number of results to return

        Returns:
            List of similar conversations with metadata
        """
        # Generate query embedding
        query_embedding = await self.embedding_client.generate_embedding(query)

        # Search in Faiss index
        search_results = await self.faiss_manager.search(query_embedding, k=k * 2)

        # Get conversation details
        results = []
        for conv_id, distance in zip(
            search_results["conversation_ids"],
            search_results["distances"],
        ):
            conversation = await self.conversation_repo.get_by_id(conv_id)

            if conversation is None:
                continue

            # Filter by user_id
            if conversation.user_id != user_id:
                continue

            # Filter by group_id if specified
            if group_id is not None and conversation.group_id != group_id:
                continue

            results.append(
                {
                    "conversation_id": conversation.conversation_id,
                    "user_id": conversation.user_id,
                    "group_id": conversation.group_id,
                    "role": conversation.role,
                    "content": conversation.content,
                    "timestamp": conversation.timestamp,
                    "distance": distance,
                }
            )

            if len(results) >= k:
                break

        return results

    async def get_conversation_history(
        self,
        user_id: int,
        group_id: Optional[int] = None,
        limit: int = 50,
    ) -> List[Conversation]:
        """Get conversation history for a user/group.

        Args:
            user_id: User ID
            group_id: Optional group ID
            limit: Maximum number of conversations to return

        Returns:
            List of conversations in chronological order
        """
        return await self.conversation_repo.get_conversation_history(
            user_id=user_id, group_id=group_id, limit=limit
        )

    async def delete_conversation(self, conversation_id: int) -> bool:
        """Delete a conversation from long-term memory.

        Args:
            conversation_id: Conversation ID to delete

        Returns:
            True if deleted successfully
        """
        # Delete from database
        await self.conversation_repo.delete(conversation_id)
        await self.vector_repo.delete(conversation_id)

        # Remove from Faiss index
        await self.faiss_manager.remove_by_conversation_id(conversation_id)

        return True

    async def delete_user_history(self, user_id: int) -> int:
        """Delete all conversation history for a user.

        Args:
            user_id: User ID to delete history for

        Returns:
            Number of conversations deleted
        """
        # Get all user conversations
        conversations = await self.conversation_repo.get_conversation_history(
            user_id=user_id, limit=10000
        )

        # Delete each conversation
        for conv in conversations:
            await self.delete_conversation(conv.conversation_id)

        return len(conversations)

    async def get_conversation_count(self, user_id: int) -> int:
        """Get number of conversations for a user.

        Args:
            user_id: User ID

        Returns:
            Number of conversations
        """
        return await self.conversation_repo.count_by_user(user_id)

    async def rebuild_index(self) -> None:
        """Rebuild the Faiss index from database.

        This is useful when the index becomes corrupted or out of sync.
        """
        # Clear current index
        await self.faiss_manager.clear()

        # Get all conversations from database
        all_convs = await self.conversation_repo.get_all()

        # Rebuild index
        for conv in all_convs:
            vector = await self.vector_repo.get_by_conversation_id(conv.conversation_id)
            if vector is not None:
                vector_id = f"vec_{conv.conversation_id}"
                await self.faiss_manager.add_vector(
                    vector_id=vector_id,
                    conversation_id=conv.conversation_id,
                    vector=vector,
                )
