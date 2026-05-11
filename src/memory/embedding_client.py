"""Embedding client for generating text embeddings."""

import asyncio
import numpy as np
from typing import List
import httpx


class EmbeddingClient:
    """Client for generating text embeddings using OpenAI-compatible API.

    Attributes:
        api_key: API key for the embedding service
        model: Model name for embeddings
        dimensions: Embedding dimensions
        base_url: Base URL for API endpoint
        timeout: Request timeout in seconds
    """

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-ada-002",
        dimensions: int = 1536,
        base_url: str = "https://api.openai.com",
        timeout: float = 30.0,
    ) -> None:
        """Initialize embedding client.

        Args:
            api_key: API key for authentication
            model: Embedding model name
            dimensions: Expected embedding dimensions
            base_url: Base URL for API endpoint
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.dimensions = dimensions
        self.base_url = base_url
        self.timeout = timeout

    async def generate_embedding(
        self, text: str, max_retries: int = 3
    ) -> np.ndarray:
        """Generate embedding for a single text.

        Args:
            text: Text to generate embedding for
            max_retries: Maximum number of retries on failure

        Returns:
            Embedding as numpy array

        Raises:
            ValueError: If text is empty
            Exception: If API request fails after retries
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        url = f"{self.base_url}/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {"input": text, "model": self.model}

        last_error = None
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, json=data, headers=headers)

                    if response.status_code == 200:
                        result = response.json()
                        embedding = result["data"][0]["embedding"]
                        return np.array(embedding, dtype=np.float32)
                    else:
                        error_info = response.json()
                        last_error = Exception(
                            f"API request failed: {error_info.get('error', {}).get('message', 'Unknown error')}"
                        )

            except Exception as e:
                last_error = e

            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        raise Exception(f"Failed to generate embedding after {max_retries} attempts: {last_error}")

    async def generate_batch_embeddings(
        self, texts: List[str], max_retries: int = 3
    ) -> List[np.ndarray]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to generate embeddings for
            max_retries: Maximum number of retries on failure

        Returns:
            List of embeddings as numpy arrays

        Raises:
            ValueError: If texts list is empty
            Exception: If API request fails after retries
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        # Process texts in batches to avoid API limits
        batch_size = 100
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            url = f"{self.base_url}/v1/embeddings"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            data = {"input": batch, "model": self.model}

            last_error = None
            for attempt in range(max_retries):
                try:
                    async with httpx.AsyncClient(timeout=self.timeout) as client:
                        response = await client.post(url, json=data, headers=headers)

                        if response.status_code == 200:
                            result = response.json()
                            embeddings = [
                                np.array(item["embedding"], dtype=np.float32)
                                for item in result["data"]
                            ]
                            all_embeddings.extend(embeddings)
                            break
                        else:
                            error_info = response.json()
                            last_error = Exception(
                                f"API request failed: {error_info.get('error', {}).get('message', 'Unknown error')}"
                            )

                except Exception as e:
                    last_error = e

                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
            else:
                raise Exception(
                    f"Failed to generate embeddings after {max_retries} attempts: {last_error}"
                )

        return all_embeddings
