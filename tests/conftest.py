"""Pytest configuration and fixtures."""

import asyncio
import os
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient as HttpxAsyncClient
from pytest_mock import MockerFixture

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock environment variables for testing."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token_123")
    monkeypatch.setenv("TELEGRAM_ADMIN_USER_IDS", "123456789,987654321")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "3306")
    monkeypatch.setenv("DB_NAME", "test_chatbot")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_password")
    monkeypatch.setenv("DB_POOL_SIZE", "5")
    monkeypatch.setenv("DB_MAX_OVERFLOW", "10")
    monkeypatch.setenv("MIMO_API_BASE_URL", "https://api.test.com")
    monkeypatch.setenv("MIMO_API_KEY", "test_mimo_key")
    monkeypatch.setenv("MIMO_MODEL", "test-model")
    monkeypatch.setenv("OPENAI_API_BASE_URL", "https://api.openai.test")
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
    monkeypatch.setenv("OPENAI_EMBEDDING_DIMENSIONS", "1536")
    monkeypatch.setenv("FAISS_INDEX_TYPE", "IndexFlatL2")
    monkeypatch.setenv("FAISS_NLIST", "100")
    monkeypatch.setenv("FAISS_NPROBE", "10")
    monkeypatch.setenv("RATE_LIMIT_MAX_REQUESTS", "20")
    monkeypatch.setenv("RATE_LIMIT_WINDOW_SECONDS", "60")
    monkeypatch.setenv("SHORT_TERM_MEMORY_MAX_MESSAGES", "50")
    monkeypatch.setenv("LONG_TERM_MEMORY_RETRIEVE_TOP_K", "5")
    monkeypatch.setenv("LONG_TERM_MEMORY_REBUILD_THRESHOLD", "1000")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    monkeypatch.setenv("LOG_FILE", "logs/test.log")


@pytest.fixture
def mock_db_pool(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock database connection pool."""
    mock_pool = MagicMock()
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.execute.return_value = None
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []
    mock_cursor.rowcount = 0

    mock_connection.cursor.return_value = mock_cursor
    mock_connection.__aenter__.return_value = mock_connection
    mock_connection.__aexit__.return_value = None

    mock_pool.acquire.return_value = mock_connection
    mock_pool.release.return_value = None

    return mock_pool


@pytest.fixture
def mock_httpx_client(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    """Mock httpx.AsyncClient for API calls."""
    mock_client = AsyncMock(spec=HttpxAsyncClient)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test response"}}],
        "data": [{"embedding": [0.1] * 1536}],
    }
    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response

    return mock_client


@pytest.fixture
async def mock_faiss_index(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    """Mock Faiss index for vector search."""
    mock_index = AsyncMock()
    mock_index.search.return_value = (
        [[0.1, 0.2, 0.3]],  # distances
        [[1, 2, 3]],  # indices
    )
    mock_index.add.return_value = None
    mock_index.reset.return_value = None

    return mock_index


@pytest.fixture
def mock_telegram_bot(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock telegram bot instance."""
    mock_bot = MagicMock()
    mock_application = MagicMock()
    mock_update = MagicMock()
    mock_context = MagicMock()

    # Mock update object
    mock_update.effective_user.id = 123456789
    mock_update.effective_user.username = "test_user"
    mock_update.effective_chat.id = 123456789
    mock_update.effective_chat.type = "private"
    mock_update.message.text = "test message"
    mock_update.message.reply_text.return_value = None

    # Mock context object
    mock_context.bot.send_message.return_value = None
    mock_context.args = []
    mock_context.user_data = {}

    mock_bot.application = mock_application
    mock_bot.update = mock_update
    mock_bot.context = mock_context

    return mock_bot


@pytest.fixture
def temp_database(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Create temporary database file for testing."""
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DB_PATH", str(db_file))
    return db_file


@pytest.fixture
def mock_log_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Create temporary log file for testing."""
    log_file = tmp_path / "test.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))
    return log_file


# Async test helpers
@pytest.fixture
async def async_client() -> AsyncGenerator[HttpxAsyncClient, None]:
    """Create async HTTP client for testing."""
    async with HttpxAsyncClient() as client:
        yield client


# Test database setup helpers
@pytest.fixture
def test_db_url() -> str:
    """Get test database URL."""
    return "mysql://test_user:test_password@localhost:3306/test_chatbot"


@pytest.fixture
def mock_redis_client(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock Redis client for rate limiting tests."""
    mock_client = MagicMock()
    mock_client.get.return_value = None
    mock_client.set.return_value = True
    mock_client.delete.return_value = True
    mock_client.exists.return_value = 0

    return mock_client
