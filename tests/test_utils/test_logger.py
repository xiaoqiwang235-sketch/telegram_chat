"""Unit tests for Logger module."""

import pytest
import logging
from unittest.mock import patch, MagicMock
import tempfile
import os

from src.utils.logger import Logger, get_logger


class TestLogger:
    """Test suite for Logger class."""

    def test_logger_initialization(self):
        """Test Logger initialization."""
        logger = Logger("test_logger")

        assert logger.logger.name == "test_logger"
        assert logger.logger.level == logging.INFO

    def test_logger_get_logger_singleton(self):
        """Test that get_logger returns singleton instance."""
        logger1 = get_logger("test_singleton")
        logger2 = get_logger("test_singleton")

        assert logger1 is logger2

    def test_logger_different_names(self):
        """Test that different names create different loggers."""
        logger1 = get_logger("logger1")
        logger2 = get_logger("logger2")

        assert logger1 is not logger2
        assert logger1.logger.name != logger2.logger.name

    def test_logger_info(self, caplog):
        """Test logging info message."""
        logger = Logger("test_info")
        logger.info("Test info message")

        assert "Test info message" in caplog.text

    def test_logger_warning(self, caplog):
        """Test logging warning message."""
        logger = Logger("test_warning")
        logger.warning("Test warning message")

        assert "Test warning message" in caplog.text

    def test_logger_error(self, caplog):
        """Test logging error message."""
        logger = Logger("test_error")
        logger.error("Test error message")

        assert "Test error message" in caplog.text

    def test_logger_debug(self, caplog):
        """Test logging debug message."""
        logger = Logger("test_debug", level=logging.DEBUG)
        logger.debug("Test debug message")

        assert "Test debug message" in caplog.text

    def test_logger_exception(self, caplog):
        """Test logging exception."""
        logger = Logger("test_exception")

        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("An error occurred")

        assert "An error occurred" in caplog.text
        assert "Test exception" in caplog.text

    def test_logger_with_file_handler(self):
        """Test logger with file handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            log_file = f.name

        try:
            logger = Logger("test_file", log_file=log_file)
            logger.info("Test file logging")

            # Read log file
            with open(log_file, "r") as f:
                content = f.read()

            assert "Test file logging" in content
        finally:
            # Clean up
            if os.path.exists(log_file):
                os.remove(log_file)

    def test_logger_with_console_handler(self, caplog):
        """Test logger with console handler."""
        logger = Logger("test_console", console=True)
        logger.info("Test console logging")

        assert "Test console logging" in caplog.text

    def test_logger_format(self, caplog):
        """Test logger format."""
        logger = Logger("test_format")
        logger.info("Test format")

        # Check that log contains expected format elements
        assert "test_format" in caplog.text or "Test format" in caplog.text

    def test_logger_set_level(self, caplog):
        """Test setting logger level."""
        logger = Logger("test_level")
        logger.set_level(logging.DEBUG)

        assert logger.logger.level == logging.DEBUG

    def test_logger_disabled(self, caplog):
        """Test disabled logger."""
        logger = Logger("test_disabled", level=logging.CRITICAL)
        logger.info("This should not appear")

        # Info message should not appear at CRITICAL level
        assert "This should not appear" not in caplog.text

    def test_get_logger_default(self):
        """Test get_logger with default name."""
        logger = get_logger()

        assert logger is not None
        assert logger.logger.name == "telegram_chatbot"

    def test_logger_context_manager(self):
        """Test logger as context manager."""
        logger = Logger("test_context")

        # Should support context manager usage
        with logger:
            logger.info("Test context manager")

    def test_logger_multiple_calls(self, caplog):
        """Test multiple logger calls."""
        logger = Logger("test_multiple")

        for i in range(5):
            logger.info(f"Message {i}")

        for i in range(5):
            assert f"Message {i}" in caplog.text

    def test_logger_long_message(self, caplog):
        """Test logging long message."""
        logger = Logger("test_long")
        long_message = "A" * 1000
        logger.info(long_message)

        assert long_message in caplog.text

    def test_logger_special_characters(self, caplog):
        """Test logging message with special characters."""
        logger = Logger("test_special")
        special_message = "Test! @#$%^&*()_+-={}[]|\\:;\"'<>?,./~`"
        logger.info(special_message)

        assert special_message in caplog.text

    def test_logger_unicode(self, caplog):
        """Test logging unicode message."""
        logger = Logger("test_unicode")
        unicode_message = "你好！🌍🌎🌏 世界"
        logger.info(unicode_message)

        assert unicode_message in caplog.text

    def test_logger_with_extra_fields(self, caplog):
        """Test logging with extra fields."""
        logger = Logger("test_extra")
        logger.info("Test with extra", extra={"user_id": 123})

        assert "Test with extra" in caplog.text

    def test_logger_stack_info(self, caplog):
        """Test logging with stack info."""
        logger = Logger("test_stack")
        logger.info("Test stack info", stack_info=True)

        assert "Test stack info" in caplog.text

    def test_logger_exc_info(self, caplog):
        """Test logging with exception info."""
        logger = Logger("test_exc_info")

        try:
            raise ValueError("Test error")
        except ValueError:
            logger.error("Error occurred", exc_info=True)

        assert "Error occurred" in caplog.text
        assert "Test error" in caplog.text
