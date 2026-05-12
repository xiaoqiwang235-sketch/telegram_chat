"""Unit tests for User model."""

import pytest

from src.models.user import User


class TestUser:
    """Test suite for User model."""

    def test_user_initialization(self):
        """Test User model initialization with all fields."""
        user = User(
            user_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language_code="en",
            is_bot=False,
            is_premium=False,
        )

        assert user.user_id == 123456789
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.language_code == "en"
        assert user.is_bot is False
        assert user.is_premium is False

    def test_user_initialization_minimal(self):
        """Test User model initialization with minimal required fields."""
        user = User(
            user_id=123456789,
            username="testuser",
            first_name="Test",
        )

        assert user.user_id == 123456789
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name is None
        assert user.language_code is None
        assert user.is_bot is False
        assert user.is_premium is False

    def test_user_to_dict(self):
        """Test converting User model to dictionary."""
        user = User(
            user_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language_code="en",
        )

        user_dict = user.to_dict()

        assert isinstance(user_dict, dict)
        assert user_dict["user_id"] == 123456789
        assert user_dict["username"] == "testuser"
        assert user_dict["first_name"] == "Test"
        assert user_dict["last_name"] == "User"
        assert user_dict["language_code"] == "en"

    def test_user_from_dict(self):
        """Test creating User model from dictionary."""
        user_dict = {
            "user_id": 123456789,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "language_code": "en",
            "is_bot": False,
            "is_premium": False,
        }

        user = User.from_dict(user_dict)

        assert user.user_id == 123456789
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.language_code == "en"
        assert user.is_bot is False
        assert user.is_premium is False

    def test_user_from_dict_minimal(self):
        """Test creating User model from minimal dictionary."""
        user_dict = {
            "user_id": 123456789,
            "username": "testuser",
            "first_name": "Test",
        }

        user = User.from_dict(user_dict)

        assert user.user_id == 123456789
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name is None
        assert user.is_bot is False  # Default value

    def test_user_equality(self):
        """Test User model equality comparison."""
        user1 = User(user_id=123456789, username="testuser", first_name="Test")
        user2 = User(user_id=123456789, username="testuser", first_name="Test")
        user3 = User(user_id=987654321, username="otheruser", first_name="Other")

        assert user1 == user2
        assert user1 != user3

    def test_user_repr(self):
        """Test User model string representation."""
        user = User(user_id=123456789, username="testuser", first_name="Test")

        repr_str = repr(user)

        assert "User" in repr_str
        assert "123456789" in repr_str
        assert "testuser" in repr_str

    def test_user_with_bot_account(self):
        """Test User model with bot account."""
        user = User(
            user_id=123456789,
            username="testbot",
            first_name="Test",
            is_bot=True,
        )

        assert user.is_bot is True

    def test_user_with_premium_account(self):
        """Test User model with premium account."""
        user = User(
            user_id=123456789,
            username="testuser",
            first_name="Test",
            is_premium=True,
        )

        assert user.is_premium is True

    def test_user_invalid_user_id_type(self):
        """Test User model with invalid user_id type."""
        with pytest.raises(TypeError):
            User(user_id="invalid", username="testuser", first_name="Test")

    def test_user_empty_username(self):
        """Test User model with empty username."""
        user = User(user_id=123456789, username="", first_name="Test")

        assert user.username == ""

    def test_user_none_username(self):
        """Test User model with None username."""
        user = User(user_id=123456789, username=None, first_name="Test")

        assert user.username is None
