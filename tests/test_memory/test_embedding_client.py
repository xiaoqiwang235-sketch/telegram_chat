"""Unit tests for Embedding Client module."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import numpy as np

from src.memory.embedding_client import EmbeddingClient


class TestEmbeddingClient:
    """Test suite for EmbeddingClient class."""

    @pytest.mark.asyncio
    async def test_embedding_client_initialization(self):
        """Test EmbeddingClient initialization."""
        client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        assert client.api_key == "test_key"
        assert client.model == "text-embedding-ada-002"
        assert client.dimensions == 1536

    @pytest.mark.asyncio
    async def test_embedding_client_generate_embedding(self):
        """Test generating embedding for text."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"embedding": [0.1] * 1536}],
            "model": "text-embedding-ada-002",
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            embedding = await mock_client.generate_embedding("Hello, world!")

            assert isinstance(embedding, np.ndarray)
            assert embedding.shape == (1536,)
            assert embedding.dtype == np.float32

    @pytest.mark.asyncio
    async def test_embedding_client_generate_batch_embeddings(self):
        """Test generating embeddings for multiple texts."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"embedding": [0.1] * 1536},
                {"embedding": [0.2] * 1536},
                {"embedding": [0.3] * 1536},
            ],
            "model": "text-embedding-ada-002",
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            texts = ["Text 1", "Text 2", "Text 3"]
            embeddings = await mock_client.generate_batch_embeddings(texts)

            assert isinstance(embeddings, list)
            assert len(embeddings) == 3
            assert all(isinstance(emb, np.ndarray) for emb in embeddings)
            assert all(emb.shape == (1536,) for emb in embeddings)

    @pytest.mark.asyncio
    async def test_embedding_client_api_error(self):
        """Test handling API errors."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        # Mock httpx client with error response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"message": "Invalid API key"}
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            with pytest.raises(Exception, match="API request failed"):
                await mock_client.generate_embedding("Hello")

    @pytest.mark.asyncio
    async def test_embedding_client_empty_text(self):
        """Test generating embedding for empty text."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        with pytest.raises(ValueError, match="Text cannot be empty"):
            await mock_client.generate_embedding("")

    @pytest.mark.asyncio
    async def test_embedding_client_long_text(self):
        """Test generating embedding for long text."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"embedding": [0.1] * 1536}],
            "model": "text-embedding-ada-002",
        }

        long_text = "A" * 10000

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            embedding = await mock_client.generate_embedding(long_text)

            assert embedding.shape == (1536,)

    @pytest.mark.asyncio
    async def test_embedding_client_unicode_text(self):
        """Test generating embedding for unicode text."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"embedding": [0.1] * 1536}],
            "model": "text-embedding-ada-002",
        }

        unicode_text = "你好！🌍🌎🌏 世界"

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            embedding = await mock_client.generate_embedding(unicode_text)

            assert embedding.shape == (1536,)

    @pytest.mark.asyncio
    async def test_embedding_client_special_characters(self):
        """Test generating embedding for text with special characters."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"embedding": [0.1] * 1536}],
            "model": "text-embedding-ada-002",
        }

        special_text = "Test! @#$%^&*()_+-={}[]|\\:;\"'<>?,./~`"

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            embedding = await mock_client.generate_embedding(special_text)

            assert embedding.shape == (1536,)

    @pytest.mark.asyncio
    async def test_embedding_client_batch_empty_list(self):
        """Test generating embeddings for empty list."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        with pytest.raises(ValueError, match="Texts list cannot be empty"):
            await mock_client.generate_batch_embeddings([])

    @pytest.mark.asyncio
    async def test_embedding_client_different_dimensions(self):
        """Test embedding client with different dimensions."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=512,
        )

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"embedding": [0.1] * 512}],
            "model": "text-embedding-ada-002",
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            embedding = await mock_client.generate_embedding("Hello")

            assert embedding.shape == (512,)

    @pytest.mark.asyncio
    async def test_embedding_client_retry_on_failure(self):
        """Test retry mechanism on API failure."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        # Mock httpx client - fail first, succeed second
        mock_error = MagicMock()
        mock_error.status_code = 500

        mock_success = MagicMock()
        mock_success.status_code = 200
        mock_success.json.return_value = {
            "data": [{"embedding": [0.1] * 1536}],
            "model": "text-embedding-ada-002",
        }

        with patch("httpx.AsyncClient.post", side_effect=[mock_error, mock_success]):
            embedding = await mock_client.generate_embedding("Hello", max_retries=2)

            assert embedding.shape == (1536,)

    @pytest.mark.asyncio
    async def test_embedding_client_custom_base_url(self):
        """Test embedding client with custom base URL."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
            base_url="https://custom.api.com",
        )

        assert mock_client.base_url == "https://custom.api.com"

    @pytest.mark.asyncio
    async def test_embedding_client_timeout(self):
        """Test embedding client with timeout."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
            timeout=30.0,
        )

        assert mock_client.timeout == 30.0

    @pytest.mark.asyncio
    async def test_embedding_client_embedding_type(self):
        """Test that embeddings are numpy arrays with float32 type."""
        mock_client = EmbeddingClient(
            api_key="test_key",
            model="text-embedding-ada-002",
            dimensions=1536,
        )

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"embedding": [0.1, 0.2, 0.3]}],
            "model": "text-embedding-ada-002",
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            embedding = await mock_client.generate_embedding("Test")

            assert isinstance(embedding, np.ndarray)
            assert embedding.dtype == np.float32
            assert list(embedding) == [0.1, 0.2, 0.3]
