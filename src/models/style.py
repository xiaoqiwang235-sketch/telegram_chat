"""Style model for conversation styles."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Style:
    """Represents a conversation style.

    Attributes:
        style_id: Unique style identifier
        name: Style name
        system_prompt: System prompt for this style
        description: Style description
    """

    style_id: int
    name: str
    system_prompt: str
    description: str

    def __post_init__(self) -> None:
        """Validate style fields after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("Style name cannot be empty")
        if not self.system_prompt or not self.system_prompt.strip():
            raise ValueError("System prompt cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        """Convert Style model to dictionary.

        Returns:
            Dictionary representation of the style
        """
        return {
            "style_id": self.style_id,
            "name": self.name,
            "system_prompt": self.system_prompt,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Style":
        """Create Style model from dictionary.

        Args:
            data: Dictionary containing style data

        Returns:
            Style instance
        """
        return cls(
            style_id=data["style_id"],
            name=data["name"],
            system_prompt=data["system_prompt"],
            description=data["description"],
        )

    def __repr__(self) -> str:
        """Return string representation of Style.

        Returns:
            String representation
        """
        return f"Style(style_id={self.style_id}, name={self.name}, description={self.description})"
