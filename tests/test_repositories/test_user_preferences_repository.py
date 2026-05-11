"""Unit tests for UserPreferences Repository module."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.repositories.user_preferences_repository import UserPreferencesRepository


class TestUserPreferencesRepository:
    """Test suite for UserPreferencesRepository class."""

    @pytest.mark.asyncio
    async def test_user_preferences_repository_create(self):
        """Test creating new user preferences."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        result = await repo.create(
            user_id=123456789,
            style_id=1,
            language="en",
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_user_preferences_repository_get_by_id(self):
        """Test getting user preferences by ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(
                1,
                123456789,
                1,
                "en",
            )
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        prefs = await repo.get_by_id(1)

        assert prefs is not None
        assert prefs["id"] == 1
        assert prefs["user_id"] == 123456789
        assert prefs["style_id"] == 1
        assert prefs["language"] == "en"

    @pytest.mark.asyncio
    async def test_user_preferences_repository_get_by_user_id(self):
        """Test getting user preferences by user ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(
                1,
                123456789,
                2,
                "zh-CN",
            )
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        prefs = await repo.get_by_user_id(123456789)

        assert prefs is not None
        assert prefs["user_id"] == 123456789
        assert prefs["style_id"] == 2
        assert prefs["language"] == "zh-CN"

    @pytest.mark.asyncio
    async def test_user_preferences_repository_get_by_user_id_not_found(self):
        """Test getting preferences for non-existent user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        prefs = await repo.get_by_user_id(999999999)

        assert prefs is None

    @pytest.mark.asyncio
    async def test_user_preferences_repository_update(self):
        """Test updating user preferences."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        result = await repo.update(
            user_id=123456789,
            style_id=3,
            language="es",
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_user_preferences_repository_update_not_found(self):
        """Test updating preferences for non-existent user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 0
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        result = await repo.update(
            user_id=999999999,
            style_id=1,
            language="en",
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_user_preferences_repository_delete(self):
        """Test deleting user preferences."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        result = await repo.delete(123456789)

        assert result is True

    @pytest.mark.asyncio
    async def test_user_preferences_repository_delete_not_found(self):
        """Test deleting preferences for non-existent user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 0
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        result = await repo.delete(999999999)

        assert result is False

    @pytest.mark.asyncio
    async def test_user_preferences_repository_exists(self):
        """Test checking if user preferences exist."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(1,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        exists = await repo.exists(123456789)

        assert exists is True

    @pytest.mark.asyncio
    async def test_user_preferences_repository_not_exists(self):
        """Test checking if non-existent user preferences exist."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        exists = await repo.exists(999999999)

        assert exists is False

    @pytest.mark.asyncio
    async def test_user_preferences_repository_get_all(self):
        """Test getting all user preferences."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (1, 123456789, 1, "en"),
                (2, 987654321, 2, "zh-CN"),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        all_prefs = await repo.get_all()

        assert len(all_prefs) == 2
        assert all_prefs[0]["user_id"] == 123456789
        assert all_prefs[1]["user_id"] == 987654321

    @pytest.mark.asyncio
    async def test_user_preferences_repository_get_all_empty(self):
        """Test getting all user preferences when none exist."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        all_prefs = await repo.get_all()

        assert len(all_prefs) == 0

    @pytest.mark.asyncio
    async def test_user_preferences_repository_count(self):
        """Test counting total user preferences."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(50,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        count = await repo.count()

        assert count == 50

    @pytest.mark.asyncio
    async def test_user_preferences_repository_create_or_update_new(self):
        """Test create_or_update with new user preferences."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)  # Preferences don't exist
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        result = await repo.create_or_update(
            user_id=123456789,
            style_id=1,
            language="en",
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_user_preferences_repository_create_or_update_existing(self):
        """Test create_or_update with existing user preferences."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(1, 123456789, 1, "en")
        )  # Preferences exist
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        result = await repo.create_or_update(
            user_id=123456789,
            style_id=2,
            language="zh-CN",
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_user_preferences_repository_get_by_style_id(self):
        """Test getting user preferences by style ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (1, 123456789, 1, "en"),
                (2, 987654321, 1, "zh-CN"),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        prefs = await repo.get_by_style_id(1)

        assert len(prefs) == 2
        assert all(p["style_id"] == 1 for p in prefs)

    @pytest.mark.asyncio
    async def test_user_preferences_repository_get_by_style_id_empty(self):
        """Test getting user preferences by style ID with no results."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserPreferencesRepository(mock_pool)

        prefs = await repo.get_by_style_id(6)

        assert len(prefs) == 0
