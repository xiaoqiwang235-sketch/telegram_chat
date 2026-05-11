"""Input validation utilities."""

import re
from typing import Any


class InputValidator:
    """Input validation utilities for user input."""

    # Maximum lengths
    MAX_MESSAGE_LENGTH = 4000
    MAX_USERNAME_LENGTH = 32
    MAX_LIMIT = 1000

    # Valid conversation roles
    VALID_ROLES = {"user", "assistant", "system"}

    # Valid style IDs
    VALID_STYLE_IDS = {1, 2, 3, 4, 5, 6}

    @staticmethod
    def validate_user_id(user_id: Any) -> int:
        """Validate user ID.

        Args:
            user_id: User ID to validate

        Returns:
            Validated user ID

        Raises:
            ValueError: If user ID is invalid
        """
        if not isinstance(user_id, int):
            raise ValueError("User ID must be an integer")
        if user_id <= 0:
            raise ValueError("User ID must be positive")
        return user_id

    @staticmethod
    def validate_group_id(group_id: Any) -> int | None:
        """Validate group ID.

        Args:
            group_id: Group ID to validate

        Returns:
            Validated group ID or None

        Raises:
            ValueError: If group ID is invalid
        """
        if group_id is None:
            return None
        if not isinstance(group_id, int):
            raise ValueError("Group ID must be an integer or None")
        if group_id <= 0:
            raise ValueError("Group ID must be positive")
        return group_id

    @staticmethod
    def validate_style_id(style_id: Any) -> int:
        """Validate style ID.

        Args:
            style_id: Style ID to validate

        Returns:
            Validated style ID

        Raises:
            ValueError: If style ID is invalid
        """
        if not isinstance(style_id, int):
            raise ValueError("Style ID must be an integer")
        if style_id not in InputValidator.VALID_STYLE_IDS:
            raise ValueError(f"Style ID must be between 1 and 6")
        return style_id

    @staticmethod
    def validate_message(message: Any) -> str:
        """Validate message content.

        Args:
            message: Message to validate

        Returns:
            Validated message

        Raises:
            ValueError: If message is invalid
        """
        if not isinstance(message, str):
            raise ValueError("Message must be a string")
        if not message.strip():
            raise ValueError("Message cannot be empty")
        if len(message) > InputValidator.MAX_MESSAGE_LENGTH:
            raise ValueError(f"Message too long (max {InputValidator.MAX_MESSAGE_LENGTH})")
        return message

    @staticmethod
    def validate_username(username: Any) -> str | None:
        """Validate username.

        Args:
            username: Username to validate

        Returns:
            Validated username or None

        Raises:
            ValueError: If username is invalid
        """
        if username is None:
            return None
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        if not username.strip():
            raise ValueError("Username cannot be empty")
        if len(username) > InputValidator.MAX_USERNAME_LENGTH:
            raise ValueError(
                f"Username too long (max {InputValidator.MAX_USERNAME_LENGTH})"
            )
        return username

    @staticmethod
    def validate_language_code(language_code: Any) -> str:
        """Validate language code.

        Args:
            language_code: Language code to validate

        Returns:
            Validated language code

        Raises:
            ValueError: If language code is invalid
        """
        if not isinstance(language_code, str):
            raise ValueError("Language code must be a string")
        if not language_code.strip():
            raise ValueError("Language code cannot be empty")

        # Basic format validation (xx or xx-XX)
        pattern = r"^[a-z]{2}(-[A-Z]{2})?$"
        if not re.match(pattern, language_code):
            raise ValueError("Invalid language code format")

        return language_code

    @staticmethod
    def sanitize_html(message: str) -> str:
        """Sanitize HTML from message.

        Args:
            message: Message to sanitize

        Returns:
            Sanitized message
        """
        # Remove script tags and content
        import re

        # Remove script tags
        message = re.sub(r"<script[^>]*>.*?</script>", "", message, flags=re.IGNORECASE | re.DOTALL)

        # Remove other potentially dangerous tags
        dangerous_tags = ["iframe", "object", "embed", "form", "input", "button"]
        for tag in dangerous_tags:
            message = re.sub(
                fr"<{tag}[^>]*>.*?</{tag}>",
                "",
                message,
                flags=re.IGNORECASE | re.DOTALL,
            )

        return message

    @staticmethod
    def validate_conversation_role(role: Any) -> str:
        """Validate conversation role.

        Args:
            role: Role to validate

        Returns:
            Validated role

        Raises:
            ValueError: If role is invalid
        """
        if not isinstance(role, str):
            raise ValueError("Conversation role must be a string")
        if not role.strip():
            raise ValueError("Conversation role cannot be empty")
        if role not in InputValidator.VALID_ROLES:
            raise ValueError(f"Invalid conversation role '{role}'. Must be one of {InputValidator.VALID_ROLES}")
        return role

    @staticmethod
    def validate_limit(limit: Any) -> int:
        """Validate limit parameter.

        Args:
            limit: Limit to validate

        Returns:
            Validated limit

        Raises:
            ValueError: If limit is invalid
        """
        if not isinstance(limit, int):
            raise ValueError("Limit must be an integer")
        if limit < 1 or limit > InputValidator.MAX_LIMIT:
            raise ValueError(f"Limit must be between 1 and {InputValidator.MAX_LIMIT}")
        return limit
