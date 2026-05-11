"""Unit tests for GroupSettings model."""

import pytest

from src.models.group_settings import GroupSettings


class TestGroupSettings:
    """Test suite for GroupSettings model."""

    def test_group_settings_initialization(self):
        """Test GroupSettings model initialization with all fields."""
        group_settings = GroupSettings(
            group_id=987654321,
            style_id=1,
            welcome_message="Welcome to the group!",
            auto_reply_enabled=True,
            language="en",
        )

        assert group_settings.group_id == 987654321
        assert group_settings.style_id == 1
        assert group_settings.welcome_message == "Welcome to the group!"
        assert group_settings.auto_reply_enabled is True
        assert group_settings.language == "en"

    def test_group_settings_minimal(self):
        """Test GroupSettings model initialization with minimal required fields."""
        group_settings = GroupSettings(
            group_id=987654321,
            style_id=1,
        )

        assert group_settings.group_id == 987654321
        assert group_settings.style_id == 1
        assert group_settings.welcome_message is None
        assert group_settings.auto_reply_enabled is True  # Default
        assert group_settings.language == "zh-CN"  # Default

    def test_group_settings_to_dict(self):
        """Test converting GroupSettings model to dictionary."""
        group_settings = GroupSettings(
            group_id=987654321,
            style_id=2,
            welcome_message="Hello!",
            auto_reply_enabled=False,
            language="zh-CN",
        )

        settings_dict = group_settings.to_dict()

        assert isinstance(settings_dict, dict)
        assert settings_dict["group_id"] == 987654321
        assert settings_dict["style_id"] == 2
        assert settings_dict["welcome_message"] == "Hello!"
        assert settings_dict["auto_reply_enabled"] is False
        assert settings_dict["language"] == "zh-CN"

    def test_group_settings_from_dict(self):
        """Test creating GroupSettings model from dictionary."""
        settings_dict = {
            "group_id": 987654321,
            "style_id": 3,
            "welcome_message": "Welcome!",
            "auto_reply_enabled": True,
            "language": "en",
        }

        group_settings = GroupSettings.from_dict(settings_dict)

        assert group_settings.group_id == 987654321
        assert group_settings.style_id == 3
        assert group_settings.welcome_message == "Welcome!"
        assert group_settings.auto_reply_enabled is True
        assert group_settings.language == "en"

    def test_group_settings_from_dict_minimal(self):
        """Test creating GroupSettings model from minimal dictionary."""
        settings_dict = {
            "group_id": 987654321,
            "style_id": 1,
        }

        group_settings = GroupSettings.from_dict(settings_dict)

        assert group_settings.group_id == 987654321
        assert group_settings.style_id == 1
        assert group_settings.welcome_message is None
        assert group_settings.auto_reply_enabled is True  # Default
        assert group_settings.language == "zh-CN"  # Default

    def test_group_settings_equality(self):
        """Test GroupSettings model equality comparison."""
        settings1 = GroupSettings(
            group_id=987654321,
            style_id=1,
            welcome_message="Welcome",
            auto_reply_enabled=True,
            language="en",
        )
        settings2 = GroupSettings(
            group_id=987654321,
            style_id=1,
            welcome_message="Welcome",
            auto_reply_enabled=True,
            language="en",
        )
        settings3 = GroupSettings(
            group_id=123456789,
            style_id=2,
            welcome_message="Hello",
            auto_reply_enabled=False,
            language="zh-CN",
        )

        assert settings1 == settings2
        assert settings1 != settings3

    def test_group_settings_repr(self):
        """Test GroupSettings model string representation."""
        group_settings = GroupSettings(
            group_id=987654321,
            style_id=1,
            welcome_message="Welcome!",
            auto_reply_enabled=True,
            language="en",
        )

        repr_str = repr(group_settings)

        assert "GroupSettings" in repr_str
        assert "987654321" in repr_str
        assert "1" in repr_str

    def test_group_settings_invalid_style_id(self):
        """Test GroupSettings model with invalid style_id."""
        with pytest.raises(ValueError):
            GroupSettings(
                group_id=987654321,
                style_id=10,  # Invalid: must be 1-6
            )

    def test_group_settings_invalid_style_id_zero(self):
        """Test GroupSettings model with style_id = 0."""
        with pytest.raises(ValueError):
            GroupSettings(
                group_id=987654321,
                style_id=0,
            )

    def test_group_settings_negative_style_id(self):
        """Test GroupSettings model with negative style_id."""
        with pytest.raises(ValueError):
            GroupSettings(
                group_id=987654321,
                style_id=-1,
            )

    def test_group_settings_all_valid_style_ids(self):
        """Test GroupSettings model with all valid style IDs (1-6)."""
        for style_id in range(1, 7):
            group_settings = GroupSettings(
                group_id=987654321,
                style_id=style_id,
            )

            assert group_settings.style_id == style_id

    def test_group_settings_empty_welcome_message(self):
        """Test GroupSettings model with empty welcome message."""
        group_settings = GroupSettings(
            group_id=987654321,
            style_id=1,
            welcome_message="",
            auto_reply_enabled=True,
            language="en",
        )

        assert group_settings.welcome_message == ""

    def test_group_settings_long_welcome_message(self):
        """Test GroupSettings model with long welcome message."""
        long_message = "A" * 10000
        group_settings = GroupSettings(
            group_id=987654321,
            style_id=1,
            welcome_message=long_message,
            auto_reply_enabled=True,
            language="en",
        )

        assert group_settings.welcome_message == long_message

    def test_group_settings_different_languages(self):
        """Test GroupSettings model with different languages."""
        languages = ["en", "zh-CN", "es", "fr", "de", "ja"]

        for language in languages:
            group_settings = GroupSettings(
                group_id=987654321,
                style_id=1,
                language=language,
            )

            assert group_settings.language == language

    def test_group_settings_auto_reply_enabled_true(self):
        """Test GroupSettings model with auto_reply_enabled = True."""
        group_settings = GroupSettings(
            group_id=987654321,
            style_id=1,
            auto_reply_enabled=True,
        )

        assert group_settings.auto_reply_enabled is True

    def test_group_settings_auto_reply_enabled_false(self):
        """Test GroupSettings model with auto_reply_enabled = False."""
        group_settings = GroupSettings(
            group_id=987654321,
            style_id=1,
            auto_reply_enabled=False,
        )

        assert group_settings.auto_reply_enabled is False
