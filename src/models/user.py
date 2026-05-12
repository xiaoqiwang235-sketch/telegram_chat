"""User model for representing Telegram users."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class User:
    """Represents a Telegram user.

    Attributes:
        user_id: Unique Telegram user ID
        username: Telegram username (optional)
        first_name: User's first name
        last_name: User's last name (optional)
        language_code: User's language code (optional)
        is_bot: Whether the user is a bot
        is_premium: Whether the user has Telegram Premium
    """

    user_id: int
    username: str | None
    first_name: str
    last_name: str | None = None
    language_code: str | None = None
    is_bot: bool = False
    is_premium: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert User model to dictionary.

        Returns:
            Dictionary representation of the user
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "language_code": self.language_code,
            "is_bot": self.is_bot,
            "is_premium": self.is_premium,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        """Create User model from dictionary.

        Args:
            data: Dictionary containing user data

        Returns:
            User instance
        """
        return cls(
            user_id=data["user_id"],
            username=data.get("username"),
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            language_code=data.get("language_code"),
            is_bot=data.get("is_bot", False),
            is_premium=data.get("is_premium", False),
        )

    def __repr__(self) -> str:
        """Return string representation of User.

        Returns:
            String representation
        """
        return (
            f"User(user_id={self.user_id}, username={self.username}, "
            f"first_name={self.first_name})"
        )
