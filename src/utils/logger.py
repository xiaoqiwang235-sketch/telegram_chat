"""Logging utilities."""

import logging
import sys
from pathlib import Path
from typing import Optional

# Global logger instances (singletons per name)
_loggers: dict[str, "Logger"] = {}


class Logger:
    """Logger wrapper for consistent logging across the application."""

    def __init__(
        self,
        name: str = "telegram_chatbot",
        level: int = logging.INFO,
        log_file: Optional[str | Path] = None,
        console: bool = True,
    ) -> None:
        """Initialize logger.

        Args:
            name: Logger name
            level: Logging level
            log_file: Optional log file path
            console: Whether to log to console
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Clear existing handlers
        self.logger.handlers.clear()

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Add console handler if requested
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # Add file handler if log file specified
        if log_file:
            # Create log directory if it doesn't exist
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Prevent propagation to avoid duplicate logs
        self.logger.propagate = False

    def info(self, message: str, *args, **kwargs) -> None:
        """Log info message.

        Args:
            message: Message to log
            *args: Additional arguments for the log handler
            **kwargs: Additional keyword arguments for the log handler
        """
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        """Log warning message.

        Args:
            message: Message to log
            *args: Additional arguments for the log handler
            **kwargs: Additional keyword arguments for the log handler
        """
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        """Log error message.

        Args:
            message: Message to log
            *args: Additional arguments for the log handler
            **kwargs: Additional keyword arguments for the log handler
        """
        self.logger.error(message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs) -> None:
        """Log debug message.

        Args:
            message: Message to log
            *args: Additional arguments for the log handler
            **kwargs: Additional keyword arguments for the log handler
        """
        self.logger.debug(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        """Log critical message.

        Args:
            message: Message to log
            *args: Additional arguments for the log handler
            **kwargs: Additional keyword arguments for the log handler
        """
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs) -> None:
        """Log exception with traceback.

        Args:
            message: Message to log
            *args: Additional arguments for the log handler
            **kwargs: Additional keyword arguments for the log handler
        """
        self.logger.exception(message, *args, **kwargs)

    def set_level(self, level: int) -> None:
        """Set logging level.

        Args:
            level: Logging level to set
        """
        self.logger.setLevel(level)

    def __enter__(self) -> "Logger":
        """Context manager entry.

        Returns:
            Logger instance
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        # Close all handlers
        for handler in self.logger.handlers:
            handler.close()


def get_logger(
    name: str = "telegram_chatbot",
    level: int = logging.INFO,
    log_file: Optional[str | Path] = None,
    console: bool = True,
) -> Logger:
    """Get or create logger instance.

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
        console: Whether to log to console

    Returns:
        Logger instance
    """
    if name not in _loggers:
        _loggers[name] = Logger(name, level, log_file, console)
    return _loggers[name]
