"""Database configuration and connection management."""

import os
from dataclasses import dataclass
from typing import ClassVar

# Global configuration instance (singleton)
_config_instance: "DatabaseConfig | None" = None


@dataclass
class DatabaseConfig:
    """Database configuration class.

    Attributes:
        host: Database host address
        port: Database port number
        database: Database name
        user: Database user
        password: Database password
        pool_size: Connection pool size
        max_overflow: Maximum overflow connections
    """

    host: str
    port: int
    database: str
    user: str
    password: str
    pool_size: int = 5
    max_overflow: int = 10

    def __post_init__(self) -> None:
        """Validate database configuration after initialization."""
        # Validate port
        try:
            port_int = int(self.port)
            if port_int < 1 or port_int > 65535:
                raise ValueError(f"Port must be between 1 and 65535, got {port_int}")
            # Convert to int if it was a string
            if isinstance(self.port, str):
                self.port = port_int
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid port value: {self.port}") from e

        # Validate pool_size
        try:
            pool_size_int = int(self.pool_size)
            if pool_size_int < 0:
                raise ValueError(f"Pool size must be non-negative, got {pool_size_int}")
            if isinstance(self.pool_size, str):
                self.pool_size = pool_size_int
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid pool_size value: {self.pool_size}") from e

        # Validate max_overflow
        try:
            max_overflow_int = int(self.max_overflow)
            if max_overflow_int < 0:
                raise ValueError(
                    f"Max overflow must be non-negative, got {max_overflow_int}"
                )
            if isinstance(self.max_overflow, str):
                self.max_overflow = max_overflow_int
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid max_overflow value: {self.max_overflow}") from e

    def get_connection_string(self) -> str:
        """Generate database connection string.

        Returns:
            Connection string for pymysql
        """
        return (
            f"mysql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )


def get_database_config() -> DatabaseConfig:
    """Get or create database configuration singleton.

    Reads configuration from environment variables:
    - DB_HOST: Database host
    - DB_PORT: Database port (default: 3306)
    - DB_NAME: Database name
    - DB_USER: Database user
    - DB_PASSWORD: Database password
    - DB_POOL_SIZE: Connection pool size (default: 5)
    - DB_MAX_OVERFLOW: Maximum overflow connections (default: 10)

    Returns:
        DatabaseConfig instance

    Raises:
        ValueError: If required environment variables are missing
    """
    global _config_instance

    if _config_instance is None:
        # Read from environment variables
        host = os.getenv("DB_HOST")
        if not host:
            raise ValueError("DB_HOST environment variable is required")

        database = os.getenv("DB_NAME")
        if not database:
            raise ValueError("DB_NAME environment variable is required")

        user = os.getenv("DB_USER")
        if not user:
            raise ValueError("DB_USER environment variable is required")

        password = os.getenv("DB_PASSWORD")
        if not password:
            raise ValueError("DB_PASSWORD environment variable is required")

        port = os.getenv("DB_PORT", "3306")
        pool_size = os.getenv("DB_POOL_SIZE", "5")
        max_overflow = os.getenv("DB_MAX_OVERFLOW", "10")

        _config_instance = DatabaseConfig(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

    return _config_instance
