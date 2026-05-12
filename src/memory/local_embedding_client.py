"""Local embedding client using Sentence-Transformers."""

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer


class LocalEmbeddingClient:
    """Client for generating text embeddings using local models.

    Attributes:
        model: SentenceTransformer model instance
        model_name: Name of the loaded model
        dimensions: Embedding dimensions
    """

    def __init__(
        self,
        model_name: str = "moka-ai/m3e-base",
        dimensions: int = 768,
        device: str = "cpu",
    ) -> None:
        """Initialize local embedding client.

        Args:
            model_name: Model name from Hugging Face
            dimensions: Expected embedding dimensions
            device: Device to run model on ("cpu" or "cuda")
        """
        self.model_name = model_name
        self.dimensions = dimensions
        self.device = device

        # Load model (will download automatically if not present)
        print(f"[LocalEmbedding] Loading model: {model_name}")
        self.model = SentenceTransformer(model_name, device=device)
        print(f"[LocalEmbedding] Model loaded! Dimension: {self.model.get_sentence_embedding_dimension()}")

        # Update dimensions based on actual model
        self.dimensions = self.model.get_sentence_embedding_dimension()

    async def generate_embedding(
        self, text: str, max_retries: int = 1
    ) -> np.ndarray:
        """Generate embedding for a single text.

        Args:
            text: Text to generate embedding for
            max_retries: Maximum number of retries (not used for local model)

        Returns:
            Embedding as numpy array

        Raises:
            ValueError: If text is empty
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Generate embedding
        embedding = self.model.encode(text, convert_to_numpy=True)

        # Ensure float32 type for Faiss compatibility
        return embedding.astype(np.float32)

    async def generate_batch_embeddings(
        self, texts: List[str], max_retries: int = 1
    ) -> List[np.ndarray]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to generate embeddings for
            max_retries: Maximum number of retries (not used for local model)

        Returns:
            List of embeddings as numpy arrays

        Raises:
            ValueError: If texts list is empty
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        # Generate embeddings in batch
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        # Convert to list of arrays and ensure float32 type
        return [emb.astype(np.float32) for emb in embeddings]
