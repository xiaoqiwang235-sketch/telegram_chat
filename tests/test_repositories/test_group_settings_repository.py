"""Unit tests for GroupSettings Repository module."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.models.group_settings import GroupSettings
from src.repositories.group_settings_repository import GroupSettingsRepository


class TestGroupSettingsRepository:
    """Test suite for GroupSettingsRepository class."""

    @pytest.mark.asyncio
    async def test_group_settings_repository_create(self):
        """Test creating new group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        settings = GroupSettings(
            group_id=987654321,
            style_id=1,
            welcome_message="Welcome!",
            auto_reply_enabled=True,
            language="en",
        )

        created_settings = await repo.create(settings)

        assert created_settings.group_id == 987654321
        assert created_settings.style_id == 1
        assert created_settings.welcome_message == "Welcome!"

    @pytest.mark.asyncio
    async def test_group_settings_repository_get_by_id(self):
        """Test getting group settings by ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(
                987654321,
                1,
                "Welcome!",
                1,
                "en",
            )
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        settings = await repo.get_by_id(987654321)

        assert settings is not None
        assert settings.group_id == 987654321
        assert settings.style_id == 1
        assert settings.welcome_message == "Welcome!"

    @pytest.mark.asyncio
    async def test_group_settings_repository_get_by_id_not_found(self):
        """Test getting non-existent group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        settings = await repo.get_by_id(999999999)

        assert settings is None

    @pytest.mark.asyncio
    async def test_group_settings_repository_update(self):
        """Test updating group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        settings = GroupSettings(
            group_id=987654321,
            style_id=2,
            welcome_message="Updated welcome",
            auto_reply_enabled=False,
            language="zh-CN",
        )

        updated_settings = await repo.update(settings)

        assert updated_settings.style_id == 2
        assert updated_settings.welcome_message == "Updated welcome"
        assert updated_settings.auto_reply_enabled is False
        assert updated_settings.language == "zh-CN"

    @pytest.mark.asyncio
    async def test_group_settings_repository_delete(self):
        """Test deleting group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        result = await repo.delete(987654321)

        assert result is True

    @pytest.mark.asyncio
    async def test_group_settings_repository_delete_not_found(self):
        """Test deleting non-existent group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 0
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        result = await repo.delete(999999999)

        assert result is False

    @pytest.mark.asyncio
    async def test_group_settings_repository_exists(self):
        """Test checking if group settings exist."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(1,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        exists = await repo.exists(987654321)

        assert exists is True

    @pytest.mark.asyncio
    async def test_group_settings_repository_not_exists(self):
        """Test checking if non-existent group settings exist."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        exists = await repo.exists(999999999)

        assert exists is False

    @pytest.mark.asyncio
    async def test_group_settings_repository_get_all(self):
        """Test getting all group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (987654321, 1, "Welcome1", 1, "en"),
                (123456789, 2, "Welcome2", 1, "zh-CN"),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        all_settings = await repo.get_all()

        assert len(all_settings) == 2
        assert all_settings[0].group_id == 987654321
        assert all_settings[1].group_id == 123456789

    @pytest.mark.asyncio
    async def test_group_settings_repository_get_all_empty(self):
        """Test getting all group settings when none exist."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        all_settings = await repo.get_all()

        assert len(all_settings) == 0

    @pytest.mark.asyncio
    async def test_group_settings_repository_count(self):
        """Test counting total group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(5,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        count = await repo.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_group_settings_repository_create_or_update_new(self):
        """Test create_or_update with new group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)  # Settings don't exist
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        settings = GroupSettings(
            group_id=987654321,
            style_id=1,
            welcome_message="Welcome!",
        )

        result = await repo.create_or_update(settings)

        assert result.group_id == 987654321
        assert result.style_id == 1

    @pytest.mark.asyncio
    async def test_group_settings_repository_create_or_update_existing(self):
        """Test create_or_update with existing group settings."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(987654321, 1, "Old welcome", 1, "en")
        )  # Settings exist
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        settings = GroupSettings(
            group_id=987654321,
            style_id=2,
            welcome_message="New welcome",
        )

        result = await repo.create_or_update(settings)

        assert result.style_id == 2
        assert result.welcome_message == "New welcome"

    @pytest.mark.asyncio
    async def test_group_settings_repository_get_by_style_id(self):
        """Test getting group settings by style ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (987654321, 1, "Welcome1", 1, "en"),
                (123456789, 1, "Welcome2", 1, "zh-CN"),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        settings = await repo.get_by_style_id(1)

        assert len(settings) == 2
        assert all(s.style_id == 1 for s in settings)

    @pytest.mark.asyncio
    async def test_group_settings_repository_get_by_style_id_empty(self):
        """Test getting group settings by style ID with no results."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = GroupSettingsRepository(mock_pool)

        settings = await repo.get_by_style_id(6)

        assert len(settings) == 0
