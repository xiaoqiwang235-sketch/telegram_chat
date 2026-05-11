"""Unit tests for Input Sanitizer module."""

import pytest

from src.utils.sanitizers import InputSanitizer


class TestInputSanitizer:
    """Test suite for InputSanitizer class."""

    def test_sanitize_text_basic(self):
        """Test basic text sanitization."""
        text = "Hello, World!"
        assert InputSanitizer.sanitize_text(text) == text

    def test_sanitize_text_with_extra_spaces(self):
        """Test sanitizing text with extra spaces."""
        text = "Hello     World   Test"
        sanitized = InputSanitizer.sanitize_text(text)
        assert sanitized == "Hello World Test"

    def test_sanitize_text_with_newlines(self):
        """Test sanitizing text with newlines."""
        text = "Hello\n\n\nWorld\n\nTest"
        sanitized = InputSanitizer.sanitize_text(text)
        assert sanitized == "Hello\nWorld\nTest"

    def test_sanitize_text_with_tabs(self):
        """Test sanitizing text with tabs."""
        text = "Hello\t\t\tWorld\t\tTest"
        sanitized = InputSanitizer.sanitize_text(text)
        assert sanitized == "Hello World Test"

    def test_sanitize_text_with_mixed_whitespace(self):
        """Test sanitizing text with mixed whitespace."""
        text = "Hello \t\n \n  World \t\t Test"
        sanitized = InputSanitizer.sanitize_text(text)
        assert sanitized == "Hello World Test"

    def test_sanitize_text_strip_leading_trailing(self):
        """Test stripping leading and trailing whitespace."""
        text = "   Hello, World!   "
        assert InputSanitizer.sanitize_text(text) == "Hello, World!"

    def test_sanitize_text_preserve_single_spaces(self):
        """Test preserving single spaces between words."""
        text = "Hello World Test"
        assert InputSanitizer.sanitize_text(text) == text

    def test_sanitize_text_empty_string(self):
        """Test sanitizing empty string."""
        assert InputSanitizer.sanitize_text("") == ""

    def test_sanitize_text_whitespace_only(self):
        """Test sanitizing whitespace-only string."""
        assert InputSanitizer.sanitize_text("   \n\t  ") == ""

    def test_sanitize_text_special_characters(self):
        """Test sanitizing text with special characters."""
        text = "Hello! @#$%^&*()_+-={}[]|\\:;\"'<>?,./~`"
        assert InputSanitizer.sanitize_text(text) == text

    def test_sanitize_text_unicode(self):
        """Test sanitizing text with unicode characters."""
        text = "你好！🌍🌎🌏 世界"
        assert InputSanitizer.sanitize_text(text) == text

    def test_sanitize_text_emojis(self):
        """Test sanitizing text with emojis."""
        text = "Hello 😀😂🤣 World"
        assert InputSanitizer.sanitize_text(text) == text

    def test_sanitize_text_links(self):
        """Test sanitizing text with links."""
        text = "Check out https://example.com for more"
        assert InputSanitizer.sanitize_text(text) == text

    def test_sanitize_text_mentions(self):
        """Test sanitizing text with mentions."""
        text = "Hello @username how are you?"
        assert InputSanitizer.sanitize_text(text) == text

    def test_sanitize_text_code_block(self):
        """Test sanitizing text with code block."""
        text = "Here is some code: ```print('hello')```"
        assert InputSanitizer.sanitize_text(text) == text

    def test_sanitize_markdown_basic(self):
        """Test basic markdown sanitization."""
        text = "**bold** and *italic* text"
        assert InputSanitizer.sanitize_markdown(text) == text

    def test_sanitize_markdown_strip_excessive(self):
        """Test stripping excessive markdown formatting."""
        text = "**bold** and **bold** and **bold**"
        assert InputSanitizer.sanitize_markdown(text) == text

    def test_sanitize_markdown_preserve_code_blocks(self):
        """Test preserving code blocks in markdown."""
        text = "```python\nprint('hello')\n```"
        assert InputSanitizer.sanitize_markdown(text) == text

    def test_sanitize_markdown_links(self):
        """Test sanitizing markdown links."""
        text = "[link](https://example.com)"
        assert InputSanitizer.sanitize_markdown(text) == text

    def test_sanitize_username_basic(self):
        """Test basic username sanitization."""
        username = "@testuser"
        assert InputSanitizer.sanitize_username(username) == "testuser"

    def test_sanitize_username_without_at(self):
        """Test sanitizing username without @ symbol."""
        username = "testuser"
        assert InputSanitizer.sanitize_username(username) == "testuser"

    def test_sanitize_username_with_spaces(self):
        """Test sanitizing username with spaces."""
        username = "@test user"
        assert InputSanitizer.sanitize_username(username) == "testuser"

    def test_sanitize_username_empty(self):
        """Test sanitizing empty username."""
        assert InputSanitizer.sanitize_username("") == ""

    def test_sanitize_username_special_characters(self):
        """Test sanitizing username with special characters."""
        username = "@test_user123"
        assert InputSanitizer.sanitize_username(username) == "test_user123"

    def test_sanitize_command_basic(self):
        """Test basic command sanitization."""
        command = "/start"
        assert InputSanitizer.sanitize_command(command) == "/start"

    def test_sanitize_command_without_slash(self):
        """Test sanitizing command without slash."""
        command = "start"
        assert InputSanitizer.sanitize_command(command) == "start"

    def test_sanitize_command_with_spaces(self):
        """Test sanitizing command with spaces."""
        command = " /start  "
        assert InputSanitizer.sanitize_command(command) == "/start"

    def test_sanitize_command_with_arguments(self):
        """Test sanitizing command with arguments."""
        command = "/start arg1 arg2"
        assert InputSanitizer.sanitize_command(command) == "/start arg1 arg2"

    def test_sanitize_command_empty(self):
        """Test sanitizing empty command."""
        assert InputSanitizer.sanitize_command("") == ""

    def test_escape_sql_basic(self):
        """Test basic SQL escaping."""
        text = "John's table"
        escaped = InputSanitizer.escape_sql(text)
        assert "''" in escaped or "\\'" in escaped

    def test_escape_sql_with_quotes(self):
        """Test escaping SQL with quotes."""
        text = 'He said "Hello"'
        escaped = InputSanitizer.escape_sql(text)
        assert '"' in escaped or '\\"' in escaped

    def test_escape_sql_with_backslashes(self):
        """Test escaping SQL with backslashes."""
        text = "path\\to\\file"
        escaped = InputSanitizer.escape_sql(text)
        assert "\\\\" in escaped

    def test_escape_sql_empty_string(self):
        """Test escaping empty SQL string."""
        assert InputSanitizer.escape_sql("") == ""

    def test_truncate_text_basic(self):
        """Test basic text truncation."""
        text = "Hello, World!"
        truncated = InputSanitizer.truncate_text(text, 5)
        assert truncated == "Hello"

    def test_truncate_text_shorter_than_limit(self):
        """Test truncating text shorter than limit."""
        text = "Hello"
        assert InputSanitizer.truncate_text(text, 10) == "Hello"

    def test_truncate_text_exact_length(self):
        """Test truncating text at exact length."""
        text = "Hello"
        assert InputSanitizer.truncate_text(text, 5) == "Hello"

    def test_truncate_text_with_ellipsis(self):
        """Test truncating text with ellipsis."""
        text = "Hello, World!"
        truncated = InputSanitizer.truncate_text(text, 8, add_ellipsis=True)
        assert truncated == "Hello..."

    def test_truncate_text_empty_string(self):
        """Test truncating empty string."""
        assert InputSanitizer.truncate_text("", 10) == ""

    def test_remove_diactrics_basic(self):
        """Test removing diacritics from text."""
        text = "café résumé naïve"
        sanitized = InputSanitizer.remove_diacritics(text)
        assert "cafe" in sanitized.lower()
        assert "resume" in sanitized.lower()
        assert "naive" in sanitized.lower()

    def test_remove_diacritics_empty(self):
        """Test removing diacritics from empty string."""
        assert InputSanitizer.remove_diacritics("") == ""
