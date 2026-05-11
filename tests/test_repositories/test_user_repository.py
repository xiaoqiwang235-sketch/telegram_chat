"""Unit tests for User Repository module."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.models.user import User
from src.repositories.user_repository import UserRepository


class TestUserRepository:
    """Test suite for UserRepository class."""

    @pytest.mark.asyncio
    async def test_user_repository_create(self):
        """Test creating a new user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        user = User(
            user_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language_code="en",
        )

        created_user = await repo.create(user)

        assert created_user.user_id == 123456789
        assert created_user.username == "testuser"
        assert created_user.first_name == "Test"

    @pytest.mark.asyncio
    async def test_user_repository_get_by_id(self):
        """Test getting user by ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(
                123456789,
                "testuser",
                "Test",
                "User",
                "en",
                0,
                0,
            )
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        user = await repo.get_by_id(123456789)

        assert user is not None
        assert user.user_id == 123456789
        assert user.username == "testuser"
        assert user.first_name == "Test"

    @pytest.mark.asyncio
    async def test_user_repository_get_by_id_not_found(self):
        """Test getting non-existent user by ID."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        user = await repo.get_by_id(999999999)

        assert user is None

    @pytest.mark.asyncio
    async def test_user_repository_get_by_username(self):
        """Test getting user by username."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(
                123456789,
                "testuser",
                "Test",
                "User",
                "en",
                0,
                0,
            )
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        user = await repo.get_by_username("testuser")

        assert user is not None
        assert user.username == "testuser"

    @pytest.mark.asyncio
    async def test_user_repository_get_by_username_not_found(self):
        """Test getting non-existent user by username."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        user = await repo.get_by_username("nonexistent")

        assert user is None

    @pytest.mark.asyncio
    async def test_user_repository_update(self):
        """Test updating a user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        user = User(
            user_id=123456789,
            username="updateduser",
            first_name="Updated",
            last_name="Name",
            language_code="es",
        )

        updated_user = await repo.update(user)

        assert updated_user.username == "updateduser"
        assert updated_user.first_name == "Updated"

    @pytest.mark.asyncio
    async def test_user_repository_delete(self):
        """Test deleting a user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        result = await repo.delete(123456789)

        assert result is True

    @pytest.mark.asyncio
    async def test_user_repository_delete_not_found(self):
        """Test deleting non-existent user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.rowcount = 0
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        result = await repo.delete(999999999)

        assert result is False

    @pytest.mark.asyncio
    async def test_user_repository_exists(self):
        """Test checking if user exists."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(1,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        exists = await repo.exists(123456789)

        assert exists is True

    @pytest.mark.asyncio
    async def test_user_repository_not_exists(self):
        """Test checking if non-existent user exists."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        exists = await repo.exists(999999999)

        assert exists is False

    @pytest.mark.asyncio
    async def test_user_repository_get_all(self):
        """Test getting all users."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(
            return_value=[
                (123456789, "user1", "Test", "User", "en", 0, 0),
                (987654321, "user2", "Another", "User", "es", 0, 0),
            ]
        )
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        users = await repo.get_all()

        assert len(users) == 2
        assert users[0].user_id == 123456789
        assert users[1].user_id == 987654321

    @pytest.mark.asyncio
    async def test_user_repository_get_all_empty(self):
        """Test getting all users when none exist."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchall = AsyncMock(return_value=[])
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        users = await repo.get_all()

        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_user_repository_count(self):
        """Test counting total users."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=(42,))
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        count = await repo.count()

        assert count == 42

    @pytest.mark.asyncio
    async def test_user_repository_create_or_update_new(self):
        """Test create_or_update with new user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)  # User doesn't exist
        mock_cursor.lastrowid = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        user = User(
            user_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        result = await repo.create_or_update(user)

        assert result.user_id == 123456789

    @pytest.mark.asyncio
    async def test_user_repository_create_or_update_existing(self):
        """Test create_or_update with existing user."""
        mock_pool = AsyncMock()
        mock_connection = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.execute = AsyncMock()
        mock_cursor.fetchone = AsyncMock(
            return_value=(123456789, "olduser", "Old", "User", "en", 0, 0)
        )  # User exists
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.acquire = AsyncMock(return_value=mock_connection)
        mock_pool.release = MagicMock()

        repo = UserRepository(mock_pool)

        user = User(
            user_id=123456789,
            username="newuser",
            first_name="New",
            last_name="Name",
        )

        result = await repo.create_or_update(user)

        assert result.username == "newuser"
        assert result.first_name == "New"
