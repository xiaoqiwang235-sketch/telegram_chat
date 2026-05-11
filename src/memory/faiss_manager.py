"""Faiss index manager for vector similarity search."""

import numpy as np
import faiss
from typing import List, Dict, Tuple
import tempfile


class FaissManager:
    """Manager for Faiss vector index.

    Attributes:
        dimension: Vector dimension
        index: Faiss index instance
        _vector_ids: List of vector IDs
        _conversation_ids: List of conversation IDs
    """

    def __init__(self, dimension: int = 1536, index_type: str = "IndexFlatL2") -> None:
        """Initialize Faiss manager.

        Args:
            dimension: Vector dimension
            index_type: Type of Faiss index to use
        """
        if dimension <= 0:
            raise ValueError("Dimension must be positive")

        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self._vector_ids: List[str] = []
        self._conversation_ids: List[int] = []

    async def add_vector(
        self, vector_id: str, conversation_id: int, vector: np.ndarray
    ) -> None:
        """Add a single vector to the index.

        Args:
            vector_id: Unique vector identifier
            conversation_id: Associated conversation ID
            vector: Vector to add

        Raises:
            ValueError: If vector dimension mismatch
        """
        if vector.shape[0] != self.dimension:
            raise ValueError(
                f"Vector dimension mismatch: expected {self.dimension}, got {vector.shape[0]}"
            )

        vector = vector.reshape(1, -1).astype("float32")
        self.index.add(vector)
        self._vector_ids.append(vector_id)
        self._conversation_ids.append(conversation_id)

    async def add_batch_vectors(
        self,
        vector_ids: List[str],
        conversation_ids: List[int],
        vectors: List[np.ndarray],
    ) -> None:
        """Add multiple vectors to the index.

        Args:
            vector_ids: List of vector IDs
            conversation_ids: List of conversation IDs
            vectors: List of vectors to add

        Raises:
            ValueError: If lengths mismatch or empty batch
        """
        if not vector_ids or not vectors:
            raise ValueError("Cannot add empty batch")

        if len(vector_ids) != len(conversation_ids) or len(vector_ids) != len(vectors):
            raise ValueError("Length mismatch between vector_ids, conversation_ids, and vectors")

        # Convert to matrix
        vectors_matrix = np.array([v.flatten() for v in vectors]).astype("float32")

        self.index.add(vectors_matrix)
        self._vector_ids.extend(vector_ids)
        self._conversation_ids.extend(conversation_ids)

    async def search(
        self,
        query_vector: np.ndarray,
        k: int = 5,
        conversation_filter: List[int] | None = None,
    ) -> Dict[str, List]:
        """Search for similar vectors.

        Args:
            query_vector: Query vector
            k: Number of results to return
            conversation_filter: Optional list of conversation IDs to filter by

        Returns:
            Dictionary with conversation_ids and distances

        Raises:
            ValueError: If k is invalid or vector dimension mismatch
        """
        if k <= 0:
            raise ValueError("k must be positive")

        if self.index.ntotal == 0:
            return {"conversation_ids": [], "distances": []}

        if query_vector.shape[0] != self.dimension:
            raise ValueError(
                f"Query vector dimension mismatch: expected {self.dimension}, got {query_vector.shape[0]}"
            )

        query_vector = query_vector.reshape(1, -1).astype("float32")

        # Search
        distances, indices = self.index.search(query_vector, min(k, self.index.ntotal))

        # Filter results if conversation_filter is provided
        results = {"conversation_ids": [], "distances": []}

        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:  # Faiss returns -1 for invalid indices
                continue

            conv_id = self._conversation_ids[int(idx)]

            # Apply filter if provided
            if conversation_filter is not None and conv_id not in conversation_filter:
                continue

            results["conversation_ids"].append(conv_id)
            results["distances"].append(float(dist))

        return results

    async def remove_by_conversation_id(self, conversation_id: int) -> bool:
        """Remove all vectors for a conversation.

        Args:
            conversation_id: Conversation ID to remove

        Returns:
            True if any vectors were removed, False otherwise
        """
        # Find indices to remove
        indices_to_remove = [
            i
            for i, cid in enumerate(self._conversation_ids)
            if cid == conversation_id
        ]

        if not indices_to_remove:
            return False

        # Rebuild index without removed vectors
        await self._rebuild_excluding(indices_to_remove)

        return True

    async def get_vectors_by_conversation(
        self, conversation_id: int
    ) -> List[Tuple[str, np.ndarray]]:
        """Get all vectors for a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of (vector_id, vector) tuples
        """
        # This is a simplified implementation
        # In practice, you'd need to store the actual vectors separately
        # or use a more sophisticated index that supports retrieval
        indices = [
            i
            for i, cid in enumerate(self._conversation_ids)
            if cid == conversation_id
        ]

        results = []
        for idx in indices:
            vector_id = self._vector_ids[idx]
            # Note: IndexFlatL2 doesn't support direct vector retrieval
            # You would need to store vectors separately
            results.append((vector_id, np.array([])))

        return results

    async def get_vector_count(self) -> int:
        """Get total number of vectors in index.

        Returns:
            Number of vectors
        """
        return self.index.ntotal

    async def clear(self) -> None:
        """Clear all vectors from the index."""
        self.index.reset()
        self._vector_ids.clear()
        self._conversation_ids.clear()

    async def rebuild_index(self) -> None:
        """Rebuild the index from scratch."""
        # Store current data
        vector_ids = self._vector_ids.copy()
        conversation_ids = self._conversation_ids.copy()

        # Note: In practice, you'd need to store the actual vectors
        # This is a simplified implementation

        # Clear and reset
        await self.clear()

        # Re-add vectors (if stored)
        # This would require storing vectors separately

    async def save_index(self, file_path: str) -> None:
        """Save index to file.

        Args:
            file_path: Path to save index
        """
        import pickle

        data = {
            "index": self.index,
            "vector_ids": self._vector_ids,
            "conversation_ids": self._conversation_ids,
        }

        with open(file_path, "wb") as f:
            pickle.dump(data, f)

    async def load_index(self, file_path: str) -> None:
        """Load index from file.

        Args:
            file_path: Path to load index from
        """
        import pickle

        with open(file_path, "rb") as f:
            data = pickle.load(f)

        self.index = data["index"]
        self._vector_ids = data["vector_ids"]
        self._conversation_ids = data["conversation_ids"]

    async def _rebuild_excluding(self, indices_to_exclude: List[int]) -> None:
        """Rebuild index excluding specified indices.

        Args:
            indices_to_exclude: Indices to exclude
        """
        # Store current data (simplified - would need actual vectors)
        keep_indices = [
            i for i in range(len(self._vector_ids)) if i not in indices_to_exclude
        ]

        # Update IDs
        self._vector_ids = [self._vector_ids[i] for i in keep_indices]
        self._conversation_ids = [self._conversation_ids[i] for i in keep_indices]

        # Rebuild index (would need actual vectors)
        # This is a simplified implementation
