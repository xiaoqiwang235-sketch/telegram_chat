"""GroupSettings model for group chat settings."""

from dataclasses import dataclass, field
from typing import Any

# Valid style IDs (1-6 corresponding to the 6 predefined styles)
VALID_STYLE_IDS = {1, 2, 3, 4, 5, 6}

# Default values
DEFAULT_AUTO_REPLY_ENABLED = True
DEFAULT_LANGUAGE = "zh-CN"


@dataclass
class GroupSettings:
    """Represents settings for a Telegram group chat.

    Attributes:
        group_id: Unique Telegram group chat ID
        style_id: Default conversation style ID for the group (1-6)
        welcome_message: Custom welcome message for new members
        auto_reply_enabled: Whether auto-reply is enabled
        language: Group language code
    """

    group_id: int
    style_id: int
    welcome_message: str | None = None
    auto_reply_enabled: bool = DEFAULT_AUTO_REPLY_ENABLED
    language: str = DEFAULT_LANGUAGE

    def __post_init__(self) -> None:
        """Validate group settings after initialization."""
        if self.style_id not in VALID_STYLE_IDS:
            raise ValueError(
                f"Invalid style_id '{self.style_id}'. Must be one of {VALID_STYLE_IDS}"
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert GroupSettings model to dictionary.

        Returns:
            Dictionary representation of the group settings
        """
        return {
            "group_id": self.group_id,
            "style_id": self.style_id,
            "welcome_message": self.welcome_message,
            "auto_reply_enabled": self.auto_reply_enabled,
            "language": self.language,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GroupSettings":
        """Create GroupSettings model from dictionary.

        Args:
            data: Dictionary containing group settings data

        Returns:
            GroupSettings instance
        """
        return cls(
            group_id=data["group_id"],
            style_id=data["style_id"],
            welcome_message=data.get("welcome_message"),
            auto_reply_enabled=data.get("auto_reply_enabled", DEFAULT_AUTO_REPLY_ENABLED),
            language=data.get("language", DEFAULT_LANGUAGE),
        )

    def __repr__(self) -> str:
        """Return string representation of GroupSettings.

        Returns:
            String representation
        """
        return (
            f"GroupSettings(group_id={self.group_id}, style_id={self.style_id}, "
            f"auto_reply_enabled={self.auto_reply_enabled}, language={self.language})"
        )
