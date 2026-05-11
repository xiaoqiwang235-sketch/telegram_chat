"""Unit tests for Style model."""

import pytest

from src.models.style import Style


class TestStyle:
    """Test suite for Style model."""

    def test_style_initialization(self):
        """Test Style model initialization with all fields."""
        style = Style(
            style_id=1,
            name="幽默搞笑",
            system_prompt="You are a humorous assistant.",
            description="Makes jokes and funny comments",
        )

        assert style.style_id == 1
        assert style.name == "幽默搞笑"
        assert style.system_prompt == "You are a humorous assistant."
        assert style.description == "Makes jokes and funny comments"

    def test_style_to_dict(self):
        """Test converting Style model to dictionary."""
        style = Style(
            style_id=1,
            name="温柔体贴",
            system_prompt="You are a gentle and caring assistant.",
            description="Shows empathy and kindness",
        )

        style_dict = style.to_dict()

        assert isinstance(style_dict, dict)
        assert style_dict["style_id"] == 1
        assert style_dict["name"] == "温柔体贴"
        assert style_dict["system_prompt"] == "You are a gentle and caring assistant."
        assert style_dict["description"] == "Shows empathy and kindness"

    def test_style_from_dict(self):
        """Test creating Style model from dictionary."""
        style_dict = {
            "style_id": 1,
            "name": "傲娇",
            "system_prompt": "You are a tsundere assistant.",
            "description": "Acts cold but is actually caring",
        }

        style = Style.from_dict(style_dict)

        assert style.style_id == 1
        assert style.name == "傲娇"
        assert style.system_prompt == "You are a tsundere assistant."
        assert style.description == "Acts cold but is actually caring"

    def test_style_equality(self):
        """Test Style model equality comparison."""
        style1 = Style(
            style_id=1,
            name="幽默搞笑",
            system_prompt="You are humorous.",
            description="Funny",
        )
        style2 = Style(
            style_id=1,
            name="幽默搞笑",
            system_prompt="You are humorous.",
            description="Funny",
        )
        style3 = Style(
            style_id=2,
            name="温柔体贴",
            system_prompt="You are gentle.",
            description="Gentle",
        )

        assert style1 == style2
        assert style1 != style3

    def test_style_repr(self):
        """Test Style model string representation."""
        style = Style(
            style_id=1,
            name="严肃专业",
            system_prompt="You are professional.",
            description="Professional",
        )

        repr_str = repr(style)

        assert "Style" in repr_str
        assert "1" in repr_str
        assert "严肃专业" in repr_str

    def test_style_all_predefined_styles(self):
        """Test all 6 predefined conversation styles."""
        styles = [
            (1, "幽默搞笑", "Humorous and funny"),
            (2, "温柔体贴", "Gentle and caring"),
            (3, "傲娇", "Tsundere"),
            (4, "严肃专业", "Serious and professional"),
            (5, "卖萌可爱", "Cute and adorable"),
            (6, "知性理性", "Rational and intellectual"),
        ]

        for style_id, name, description in styles:
            style = Style(
                style_id=style_id,
                name=name,
                system_prompt=f"You are {description.lower()}.",
                description=description,
            )

            assert style.style_id == style_id
            assert style.name == name
            assert style.description == description

    def test_style_empty_name(self):
        """Test Style model with empty name."""
        with pytest.raises(ValueError):
            Style(
                style_id=1,
                name="",
                system_prompt="You are test.",
                description="Test",
            )

    def test_style_empty_system_prompt(self):
        """Test Style model with empty system prompt."""
        with pytest.raises(ValueError):
            Style(
                style_id=1,
                name="Test",
                system_prompt="",
                description="Test",
            )

    def test_style_long_system_prompt(self):
        """Test Style model with long system prompt."""
        long_prompt = "A" * 10000
        style = Style(
            style_id=1,
            name="Test",
            system_prompt=long_prompt,
            description="Test",
        )

        assert style.system_prompt == long_prompt

    def test_style_special_characters_in_name(self):
        """Test Style model with special characters in name."""
        style = Style(
            style_id=1,
            name="测试风格！@#",
            system_prompt="You are test.",
            description="Test",
        )

        assert "测试风格！@#" in style.name

    def test_style_unicode_content(self):
        """Test Style model with unicode content."""
        style = Style(
            style_id=1,
            name="Emoji风格😀🎉",
            system_prompt="You are fun! 😊",
            description="带有表情符号的风格",
        )

        assert "😀🎉" in style.name
        assert "😊" in style.system_prompt
        assert "带有表情符号的风格" in style.description
