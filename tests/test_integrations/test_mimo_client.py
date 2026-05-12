"""Unit tests for XiaoMi MiMo Client module."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx


class TestMimoClient:
    """Test suite for MimoClient class."""

    @pytest.mark.asyncio
    async def test_mimo_client_initialization(self):
        """Test MimoClient initialization."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(
            api_key="test_key",
            base_url="https://api.xiaomimimo.com",
            model="mi-mimo-model",
        )

        assert client.api_key == "test_key"
        assert client.base_url == "https://api.xiaomimimo.com"
        assert client.model == "mi-mimo-model"

    @pytest.mark.asyncio
    async def test_mimo_client_generate_response(self):
        """Test generating chat response."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello! How can I help you?"
                    }
                }
            ],
            "model": "mi-mimo-model",
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            response = await client.generate_response(
                messages=[{"role": "user", "content": "Hello"}],
                system_prompt="You are a helpful assistant.",
            )

            assert response == "Hello! How can I help you?"

    @pytest.mark.asyncio
    async def test_mimo_client_generate_response_with_style(self):
        """Test generating response with style."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "你好！😊 有什么我可以帮助你的吗？"
                    }
                }
            ],
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            response = await client.generate_response(
                messages=[{"role": "user", "content": "Hi"}],
                system_prompt="你是一个温柔体贴的助手。",
            )

            assert "你好" in response

    @pytest.mark.asyncio
    async def test_mimo_client_generate_response_empty_messages(self):
        """Test generating response with empty messages."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        with pytest.raises(ValueError, match="Messages list cannot be empty"):
            await client.generate_response(
                messages=[],
                system_prompt="You are helpful.",
            )

    @pytest.mark.asyncio
    async def test_mimo_client_api_error(self):
        """Test handling API errors."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        # Mock httpx client with error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"message": "Invalid API key"}
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            with pytest.raises(Exception, match="API request failed"):
                await client.generate_response(
                    messages=[{"role": "user", "content": "Hello"}],
                    system_prompt="You are helpful.",
                )

    @pytest.mark.asyncio
    async def test_mimo_client_retry_on_failure(self):
        """Test retry mechanism on API failure."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        # Mock httpx client - fail first, succeed second
        mock_error = MagicMock()
        mock_error.status_code = 500

        mock_success = MagicMock()
        mock_success.status_code = 200
        mock_success.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Success!"
                    }
                }
            ],
        }

        with patch("httpx.AsyncClient.post", side_effect=[mock_error, mock_success]):
            response = await client.generate_response(
                messages=[{"role": "user", "content": "Hello"}],
                system_prompt="You are helpful.",
                max_retries=2,
            )

            assert response == "Success!"

    @pytest.mark.asyncio
    async def test_mimo_client_with_temperature(self):
        """Test generating response with temperature parameter."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Response"
                    }
                }
            ],
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response) as mock_post:
            await client.generate_response(
                messages=[{"role": "user", "content": "Hello"}],
                system_prompt="You are helpful.",
                temperature=0.7,
            )

            # Verify temperature was passed
            call_args = mock_post.call_args
            assert "json" in call_args.kwargs
            assert "temperature" in call_args.kwargs["json"]

    @pytest.mark.asyncio
    async def test_mimo_client_with_max_tokens(self):
        """Test generating response with max_tokens parameter."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Response"
                    }
                }
            ],
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response) as mock_post:
            await client.generate_response(
                messages=[{"role": "user", "content": "Hello"}],
                system_prompt="You are helpful.",
                max_tokens=1000,
            )

            # Verify max_tokens was passed
            call_args = mock_post.call_args
            assert "json" in call_args.kwargs
            assert "max_tokens" in call_args.kwargs["json"]

    @pytest.mark.asyncio
    async def test_mimo_client_long_conversation_history(self):
        """Test generating response with long conversation history."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Based on our conversation..."
                    }
                }
            ],
        }

        # Create long conversation history
        messages = [
            {"role": "user", "content": f"Message {i}"}
            for i in range(50)
        ]

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            response = await client.generate_response(
                messages=messages,
                system_prompt="You are helpful.",
            )

            assert "Based on our conversation" in response

    @pytest.mark.asyncio
    async def test_mimo_client_custom_timeout(self):
        """Test client with custom timeout."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key", timeout=60.0)

        assert client.timeout == 60.0

    @pytest.mark.asyncio
    async def test_mimo_client_unicode_content(self):
        """Test generating response with unicode content."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "你好！🎉 欢迎使用我们的服务！"
                    }
                }
            ],
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            response = await client.generate_response(
                messages=[{"role": "user", "content": "你好"}],
                system_prompt="你是一个友好的助手。",
            )

            assert "你好" in response
            assert "🎉" in response

    @pytest.mark.asyncio
    async def test_mimo_client_streaming_not_supported(self):
        """Test that streaming is not supported."""
        from src.integrations.mimo_client import MimoClient

        client = MimoClient(api_key="test_key")

        with pytest.raises(NotImplementedError, match="Streaming not supported"):
            await client.generate_response_stream(
                messages=[{"role": "user", "content": "Hello"}],
                system_prompt="You are helpful.",
            )
