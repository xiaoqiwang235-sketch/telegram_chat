"""Database configuration and connection management."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Literal

# Global configuration instance (singleton)
_config_instance: "DatabaseConfig | None" = None

DatabaseType = Literal["mysql", "sqlite"]


@dataclass
class DatabaseConfig:
    """Database configuration class supporting MySQL and SQLite.

    Attributes:
        db_type: Type of database ('mysql' or 'sqlite')
        host: Database host (MySQL only)
        port: Database port (MySQL only)
        database: Database name (MySQL only)
        db_path: Path to SQLite database file (SQLite only)
        user: Database user (MySQL only)
        password: Database password (MySQL only)
        pool_size: Connection pool size
        max_overflow: Maximum overflow connections (MySQL only)
    """

    db_type: DatabaseType = "mysql"
    # MySQL attributes
    host: str = "localhost"
    port: int = 3306
    database: str = "telegram_chatbot"
    user: str = "root"
    password: str = ""
    # SQLite attributes
    db_path: str = "data/telegram_chatbot.db"
    # Common attributes
    pool_size: int = 5
    max_overflow: int = 10

    def __post_init__(self) -> None:
        """Validate database configuration after initialization."""
        if self.db_type == "mysql":
            # Validate port
            try:
                port_int = int(self.port)
                if port_int < 1 or port_int > 65535:
                    raise ValueError(f"Port must be between 1 and 65535, got {port_int}")
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
        elif self.db_type == "sqlite":
            # Ensure db_path is a valid path
            path_obj = Path(self.db_path)
            # Create parent directory if it doesn't exist
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            self.db_path = str(path_obj.absolute())

    def get_connection_string(self) -> str:
        """Generate database connection string.

        Returns:
            Connection string for the configured database
        """
        if self.db_type == "mysql":
            return (
                f"mysql://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )
        else:  # sqlite
            return f"sqlite:///{self.db_path}"


def get_database_config() -> DatabaseConfig:
    """Get or create database configuration singleton.

    Reads configuration from environment variables:
    - DB_TYPE: Database type ('mysql' or 'sqlite', default: 'sqlite')
    - DB_HOST: Database host (MySQL only)
    - DB_PORT: Database port (MySQL only, default: 3306)
    - DB_NAME: Database name (MySQL only)
    - DB_USER: Database user (MySQL only)
    - DB_PASSWORD: Database password (MySQL only)
    - DB_PATH: Path to SQLite database file (SQLite only, default: 'data/telegram_chatbot.db')
    - DB_POOL_SIZE: Connection pool size (default: 5)
    - DB_MAX_OVERFLOW: Maximum overflow connections (MySQL only, default: 10)

    Returns:
        DatabaseConfig instance

    Raises:
        ValueError: If required environment variables are missing
    """
    global _config_instance

    if _config_instance is None:
        # Get database type from environment
        db_type = os.getenv("DB_TYPE", "sqlite").lower()

        if db_type not in ("mysql", "sqlite"):
            raise ValueError(f"DB_TYPE must be 'mysql' or 'sqlite', got '{db_type}'")

        if db_type == "mysql":
            # MySQL configuration
            host = os.getenv("DB_HOST")
            if not host:
                raise ValueError("DB_HOST environment variable is required for MySQL")

            database = os.getenv("DB_NAME")
            if not database:
                raise ValueError("DB_NAME environment variable is required for MySQL")

            user = os.getenv("DB_USER")
            if not user:
                raise ValueError("DB_USER environment variable is required for MySQL")

            password = os.getenv("DB_PASSWORD")
            if not password:
                raise ValueError("DB_PASSWORD environment variable is required for MySQL")

            port = os.getenv("DB_PORT", "3306")
            pool_size = os.getenv("DB_POOL_SIZE", "5")
            max_overflow = os.getenv("DB_MAX_OVERFLOW", "10")

            _config_instance = DatabaseConfig(
                db_type="mysql",
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                pool_size=pool_size,
                max_overflow=max_overflow,
            )
        else:  # sqlite
            # SQLite configuration
            db_path = os.getenv("DB_PATH", "data/telegram_chatbot.db")
            pool_size = os.getenv("DB_POOL_SIZE", "5")

            _config_instance = DatabaseConfig(
                db_type="sqlite",
                db_path=db_path,
                pool_size=int(pool_size),
            )

    return _config_instance
