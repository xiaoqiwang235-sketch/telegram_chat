"""Input sanitization utilities."""

import re
import unicodedata
from typing import Any


class InputSanitizer:
    """Input sanitization utilities for cleaning user input."""

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text by normalizing whitespace.

        Args:
            text: Text to sanitize

        Returns:
            Sanitized text
        """
        if not text:
            return ""

        # Replace all whitespace sequences (spaces, tabs, newlines) with single space
        text = re.sub(r"\s+", " ", text)

        # Strip leading and trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def sanitize_markdown(text: str) -> str:
        """Sanitize markdown text.

        Args:
            text: Markdown text to sanitize

        Returns:
            Sanitized markdown text
        """
        if not text:
            return ""

        # Basic markdown sanitization
        # Remove excessive bold/italic markers
        text = re.sub(r"\*{4,}", "", text)  # Remove 4+ asterisks
        text = re.sub(r"_{4,}", "", text)  # Remove 4+ underscores

        # Normalize whitespace
        text = InputSanitizer.sanitize_text(text)

        return text

    @staticmethod
    def sanitize_username(username: str) -> str:
        """Sanitize username by removing @ symbol and whitespace.

        Args:
            username: Username to sanitize

        Returns:
            Sanitized username
        """
        if not username:
            return ""

        # Remove @ symbol if present
        username = username.lstrip("@")

        # Remove whitespace
        username = re.sub(r"\s+", "", username)

        return username

    @staticmethod
    def sanitize_command(command: str) -> str:
        """Sanitize command by normalizing format.

        Args:
            command: Command to sanitize

        Returns:
            Sanitized command
        """
        if not command:
            return ""

        # Strip leading/trailing whitespace
        command = command.strip()

        # Ensure command starts with /
        if not command.startswith("/"):
            command = "/" + command

        # Normalize multiple slashes
        command = re.sub(r"/+", "/", command)

        return command

    @staticmethod
    def escape_sql(text: str) -> str:
        """Escape SQL special characters.

        Args:
            text: Text to escape

        Returns:
            Escaped text
        """
        if not text:
            return ""

        # Escape single quotes
        text = text.replace("'", "''")

        # Escape backslashes
        text = text.replace("\\", "\\\\")

        return text

    @staticmethod
    def truncate_text(text: str, max_length: int, add_ellipsis: bool = False) -> str:
        """Truncate text to maximum length.

        Args:
            text: Text to truncate
            max_length: Maximum length
            add_ellipsis: Whether to add ellipsis (...) if truncated

        Returns:
            Truncated text
        """
        if not text or len(text) <= max_length:
            return text

        if add_ellipsis and max_length > 3:
            return text[: max_length - 3] + "..."
        else:
            return text[:max_length]

    @staticmethod
    def remove_diacritics(text: str) -> str:
        """Remove diacritical marks from text.

        Args:
            text: Text to process

        Returns:
            Text without diacritics
        """
        if not text:
            return ""

        # Normalize unicode characters
        normalized = unicodedata.normalize("NFKD", text)

        # Remove combining characters
        return "".join(
            [c for c in normalized if not unicodedata.combining(c)]
        )

    @staticmethod
    def sanitize_html(text: str) -> str:
        """Remove HTML tags from text.

        Args:
            text: Text to sanitize

        Returns:
            Text without HTML tags
        """
        if not text:
            return ""

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)

        # Clean up whitespace
        text = InputSanitizer.sanitize_text(text)

        return text
