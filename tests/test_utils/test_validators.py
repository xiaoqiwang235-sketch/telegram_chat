"""Unit tests for Input Validator module."""

import pytest

from src.utils.validators import InputValidator


class TestInputValidator:
    """Test suite for InputValidator class."""

    def test_validate_user_id_valid(self):
        """Test validating valid user ID."""
        assert InputValidator.validate_user_id(123456789) == 123456789

    def test_validate_user_id_invalid_type(self):
        """Test validating user ID with invalid type."""
        with pytest.raises(ValueError, match="User ID must be an integer"):
            InputValidator.validate_user_id("invalid")

    def test_validate_user_id_negative(self):
        """Test validating negative user ID."""
        with pytest.raises(ValueError, match="User ID must be positive"):
            InputValidator.validate_user_id(-1)

    def test_validate_user_id_zero(self):
        """Test validating zero user ID."""
        with pytest.raises(ValueError, match="User ID must be positive"):
            InputValidator.validate_user_id(0)

    def test_validate_group_id_valid(self):
        """Test validating valid group ID."""
        assert InputValidator.validate_group_id(987654321) == 987654321

    def test_validate_group_id_none(self):
        """Test validating None group ID."""
        assert InputValidator.validate_group_id(None) is None

    def test_validate_group_id_invalid_type(self):
        """Test validating group ID with invalid type."""
        with pytest.raises(ValueError, match="Group ID must be an integer or None"):
            InputValidator.validate_group_id("invalid")

    def test_validate_group_id_negative(self):
        """Test validating negative group ID."""
        with pytest.raises(ValueError, match="Group ID must be positive"):
            InputValidator.validate_group_id(-1)

    def test_validate_style_id_valid(self):
        """Test validating valid style ID."""
        for style_id in range(1, 7):
            assert InputValidator.validate_style_id(style_id) == style_id

    def test_validate_style_id_invalid_low(self):
        """Test validating style ID too low."""
        with pytest.raises(ValueError, match="Style ID must be between 1 and 6"):
            InputValidator.validate_style_id(0)

    def test_validate_style_id_invalid_high(self):
        """Test validating style ID too high."""
        with pytest.raises(ValueError, match="Style ID must be between 1 and 6"):
            InputValidator.validate_style_id(7)

    def test_validate_message_valid(self):
        """Test validating valid message."""
        message = "Hello, how are you?"
        assert InputValidator.validate_message(message) == message

    def test_validate_message_empty(self):
        """Test validating empty message."""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            InputValidator.validate_message("")

    def test_validate_message_whitespace_only(self):
        """Test validating whitespace-only message."""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            InputValidator.validate_message("   ")

    def test_validate_message_too_long(self):
        """Test validating message that's too long."""
        long_message = "A" * 4001
        with pytest.raises(ValueError, match="Message too long"):
            InputValidator.validate_message(long_message)

    def test_validate_message_max_length(self):
        """Test validating message at max length."""
        max_message = "A" * 4000
        assert InputValidator.validate_message(max_message) == max_message

    def test_validate_username_valid(self):
        """Test validating valid username."""
        assert InputValidator.validate_username("testuser") == "testuser"

    def test_validate_username_none(self):
        """Test validating None username."""
        assert InputValidator.validate_username(None) is None

    def test_validate_username_empty(self):
        """Test validating empty username."""
        with pytest.raises(ValueError, match="Username cannot be empty"):
            InputValidator.validate_username("")

    def test_validate_username_too_long(self):
        """Test validating username that's too long."""
        long_username = "a" * 33
        with pytest.raises(ValueError, match="Username too long"):
            InputValidator.validate_username(long_username)

    def test_validate_username_max_length(self):
        """Test validating username at max length."""
        max_username = "a" * 32
        assert InputValidator.validate_username(max_username) == max_username

    def test_validate_language_code_valid(self):
        """Test validating valid language codes."""
        valid_codes = ["en", "zh-CN", "es", "fr", "de", "ja"]
        for code in valid_codes:
            assert InputValidator.validate_language_code(code) == code

    def test_validate_language_code_invalid_format(self):
        """Test validating invalid language code format."""
        with pytest.raises(ValueError, match="Invalid language code"):
            InputValidator.validate_language_code("invalid@code")

    def test_validate_language_code_empty(self):
        """Test validating empty language code."""
        with pytest.raises(ValueError, match="Language code cannot be empty"):
            InputValidator.validate_language_code("")

    def test_validate_language_code_default(self):
        """Test validating default language code."""
        assert InputValidator.validate_language_code("zh-CN") == "zh-CN"

    def test sanitize_html_valid(self):
        """Test sanitizing HTML in message."""
        message = "<script>alert('xss')</script>Hello"
        sanitized = InputValidator.sanitize_html(message)
        assert "<script>" not in sanitized
        assert "Hello" in sanitized

    def test sanitize_html_no_tags(self):
        """Test sanitizing message without HTML."""
        message = "Hello, how are you?"
        assert InputValidator.sanitize_html(message) == message

    def test_sanitize_html_allowed_tags(self):
        """Test sanitizing HTML with allowed tags."""
        message = "<b>Hello</b> <i>World</i>"
        sanitized = InputValidator.sanitize_html(message)
        # Should preserve some basic formatting
        assert "Hello" in sanitized
        assert "World" in sanitized

    def test_validate_conversation_role_valid(self):
        """Test validating valid conversation roles."""
        valid_roles = ["user", "assistant", "system"]
        for role in valid_roles:
            assert InputValidator.validate_conversation_role(role) == role

    def test_validate_conversation_role_invalid(self):
        """Test validating invalid conversation role."""
        with pytest.raises(ValueError, match="Invalid conversation role"):
            InputValidator.validate_conversation_role("invalid_role")

    def test_validate_conversation_role_empty(self):
        """Test validating empty conversation role."""
        with pytest.raises(ValueError, match="Conversation role cannot be empty"):
            InputValidator.validate_conversation_role("")

    def test_validate_limit_valid(self):
        """Test validating valid limit."""
        assert InputValidator.validate_limit(10) == 10

    def test_validate_limit_invalid_low(self):
        """Test validating limit too low."""
        with pytest.raises(ValueError, match="Limit must be between 1 and 1000"):
            InputValidator.validate_limit(0)

    def test_validate_limit_invalid_high(self):
        """Test validating limit too high."""
        with pytest.raises(ValueError, match="Limit must be between 1 and 1000"):
            InputValidator.validate_limit(1001)

    def test_validate_limit_boundary_values(self):
        """Test validating limit at boundary values."""
        assert InputValidator.validate_limit(1) == 1
        assert InputValidator.validate_limit(1000) == 1000
