"""Unit tests for Style Service module."""

import pytest

from src.services.style_service import StyleService


class TestStyleService:
    """Test suite for StyleService class."""

    def test_style_service_initialization(self):
        """Test StyleService initialization."""
        service = StyleService()

        assert service is not None
        assert len(service.styles) == 6

    def test_style_service_get_style_by_id(self):
        """Test getting style by ID."""
        service = StyleService()

        # Test all 6 styles
        for style_id in range(1, 7):
            style = service.get_style(style_id)
            assert style is not None
            assert "style_id" in style
            assert style["style_id"] == style_id
            assert "name" in style
            assert "system_prompt" in style

    def test_style_service_get_all_styles(self):
        """Test getting all styles."""
        service = StyleService()

        styles = service.get_all_styles()

        assert len(styles) == 6
        assert all("style_id" in style for style in styles)
        assert all("name" in style for style in styles)

    def test_style_service_get_style_names(self):
        """Test getting all style names."""
        service = StyleService()

        names = service.get_style_names()

        assert len(names) == 6
        expected_names = [
            "幽默搞笑",
            "温柔体贴",
            "傲娇",
            "严肃专业",
            "卖萌可爱",
            "知性理性",
        ]
        assert names == expected_names

    def test_style_service_humorous_style(self):
        """Test humorous style content."""
        service = StyleService()

        style = service.get_style(1)

        assert style["name"] == "幽默搞笑"
        assert "幽默" in style["system_prompt"] or "搞笑" in style["system_prompt"]
        assert "搞笑" in style["description"]

    def test_style_service_gentle_style(self):
        """Test gentle style content."""
        service = StyleService()

        style = service.get_style(2)

        assert style["name"] == "温柔体贴"
        assert "温柔" in style["system_prompt"] or "体贴" in style["system_prompt"]

    def test_style_service_tsundere_style(self):
        """Test tsundere style content."""
        service = StyleService()

        style = service.get_style(3)

        assert style["name"] == "傲娇"
        assert "傲娇" in style["system_prompt"] or "tsundere" in style["system_prompt"].lower()

    def test_style_service_professional_style(self):
        """Test professional style content."""
        service = StyleService()

        style = service.get_style(4)

        assert style["name"] == "严肃专业"
        assert "专业" in style["system_prompt"] or "严肃" in style["system_prompt"]

    def test_style_service_cute_style(self):
        """Test cute style content."""
        service = StyleService()

        style = service.get_style(5)

        assert style["name"] == "卖萌可爱"
        assert "可爱" in style["system_prompt"] or "卖萌" in style["system_prompt"]

    def test_style_service_rational_style(self):
        """Test rational style content."""
        service = StyleService()

        style = service.get_style(6)

        assert style["name"] == "知性理性"
        assert "理性" in style["system_prompt"] or "知性" in style["system_prompt"]

    def test_style_service_get_system_prompt(self):
        """Test getting system prompt for style."""
        service = StyleService()

        prompt = service.get_system_prompt(1)

        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_style_service_invalid_style_id(self):
        """Test getting invalid style ID."""
        service = StyleService()

        with pytest.raises(ValueError, match="Invalid style ID"):
            service.get_style(999)

    def test_style_service_style_id_range(self):
        """Test that style IDs are in valid range."""
        service = StyleService()

        styles = service.get_all_styles()

        style_ids = [style["style_id"] for style in styles]
        assert all(1 <= sid <= 6 for sid in style_ids)

    def test_style_service_unique_names(self):
        """Test that all style names are unique."""
        service = StyleService()

        styles = service.get_all_styles()
        names = [style["name"] for style in styles]

        assert len(names) == len(set(names))

    def test_style_service_system_prompt_format(self):
        """Test that system prompts are properly formatted."""
        service = StyleService()

        for style_id in range(1, 7):
            prompt = service.get_system_prompt(style_id)

            assert isinstance(prompt, str)
            assert len(prompt) > 20  # Should be substantive
            assert not prompt.isspace()

    def test_style_service_get_style_by_name(self):
        """Test getting style by name."""
        service = StyleService()

        style = service.get_style_by_name("幽默搞笑")

        assert style is not None
        assert style["style_id"] == 1

    def test_style_service_get_style_by_invalid_name(self):
        """Test getting style by invalid name."""
        service = StyleService()

        with pytest.raises(ValueError, match="Style not found"):
            service.get_style_by_name("不存在的风格")

    def test_style_service_is_valid_style_id(self):
        """Test validating style IDs."""
        service = StyleService()

        for style_id in range(1, 7):
            assert service.is_valid_style_id(style_id) is True

        assert service.is_valid_style_id(0) is False
        assert service.is_valid_style_id(7) is False
        assert service.is_valid_style_id(-1) is False

    def test_style_service_default_style(self):
        """Test default style (should be humorous)."""
        service = StyleService()

        default_style = service.get_default_style()

        assert default_style is not None
        assert default_style["style_id"] == 1
        assert default_style["name"] == "幽默搞笑"

    def test_style_service_all_descriptions(self):
        """Test that all styles have descriptions."""
        service = StyleService()

        styles = service.get_all_styles()

        assert all("description" in style for style in styles)
        assert all(len(style["description"]) > 0 for style in styles)
