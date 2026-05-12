"""Unit tests for Database Config module."""

import os
import pytest

from src.database.config import DatabaseConfig, get_database_config


class TestDatabaseConfig:
    """Test suite for DatabaseConfig class."""

    def test_database_config_initialization(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig initialization with environment variables."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "3306")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")
        monkeypatch.setenv("DB_POOL_SIZE", "5")
        monkeypatch.setenv("DB_MAX_OVERFLOW", "10")

        config = DatabaseConfig()

        assert config.host == "localhost"
        assert config.port == 3306
        assert config.database == "test_db"
        assert config.user == "test_user"
        assert config.password == "test_password"
        assert config.pool_size == 5
        assert config.max_overflow == 10

    def test_database_config_default_values(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig with default values."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "default_db")
        monkeypatch.setenv("DB_USER", "default_user")
        monkeypatch.setenv("DB_PASSWORD", "default_password")

        config = DatabaseConfig()

        assert config.port == 3306  # Default
        assert config.pool_size == 5  # Default
        assert config.max_overflow == 10  # Default

    def test_database_config_connection_string(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig connection string generation."""
        monkeypatch.setenv("DB_HOST", "testhost")
        monkeypatch.setenv("DB_PORT", "3307")
        monkeypatch.setenv("DB_NAME", "testdb")
        monkeypatch.setenv("DB_USER", "testuser")
        monkeypatch.setenv("DB_PASSWORD", "testpass")

        config = DatabaseConfig()
        conn_str = config.get_connection_string()

        assert "testhost" in conn_str
        assert "3307" in conn_str
        assert "testdb" in conn_str
        assert "testuser" in conn_str
        assert "testpass" in conn_str

    def test_database_config_missing_required_field(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig with missing required environment variable."""
        # Remove required environment variable
        monkeypatch.delenv("DB_HOST", raising=False)

        with pytest.raises(ValueError, match="DB_HOST"):
            DatabaseConfig()

    def test_database_config_invalid_port(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig with invalid port number."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")
        monkeypatch.setenv("DB_PORT", "invalid")

        with pytest.raises(ValueError):
            DatabaseConfig()

    def test_database_config_port_out_of_range(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig with port number out of valid range."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")
        monkeypatch.setenv("DB_PORT", "99999")

        with pytest.raises(ValueError):
            DatabaseConfig()

    def test_database_config_invalid_pool_size(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig with invalid pool size."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")
        monkeypatch.setenv("DB_POOL_SIZE", "invalid")

        with pytest.raises(ValueError):
            DatabaseConfig()

    def test_database_config_negative_pool_size(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig with negative pool size."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")
        monkeypatch.setenv("DB_POOL_SIZE", "-5")

        with pytest.raises(ValueError):
            DatabaseConfig()

    def test_database_config_invalid_max_overflow(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig with invalid max overflow."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")
        monkeypatch.setenv("DB_MAX_OVERFLOW", "invalid")

        with pytest.raises(ValueError):
            DatabaseConfig()

    def test_database_config_negative_max_overflow(self, monkeypatch: pytest.MonkeyPatch):
        """Test DatabaseConfig with negative max overflow."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")
        monkeypatch.setenv("DB_MAX_OVERFLOW", "-10")

        with pytest.raises(ValueError):
            DatabaseConfig()


class TestGetDatabaseConfig:
    """Test suite for get_database_config function."""

    def test_get_database_config_singleton(self, monkeypatch: pytest.MonkeyPatch):
        """Test that get_database_config returns singleton instance."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")

        config1 = get_database_config()
        config2 = get_database_config()

        assert config1 is config2
        assert id(config1) == id(config2)

    def test_get_database_config_creates_once(self, monkeypatch: pytest.MonkeyPatch):
        """Test that get_database_config creates instance only once."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")

        config = get_database_config()

        # Verify it's a DatabaseConfig instance
        assert isinstance(config, DatabaseConfig)
        assert config.host == "localhost"
        assert config.database == "test_db"

    def test_get_database_config_caching(self, monkeypatch: pytest.MonkeyPatch):
        """Test that get_database_config caches the configuration."""
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_NAME", "test_db")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_password")

        config1 = get_database_config()

        # Change environment variable after first call
        monkeypatch.setenv("DB_HOST", "newhost")

        config2 = get_database_config()

        # Should still return the cached instance with original value
        assert config1 is config2
        assert config2.host == "localhost"
