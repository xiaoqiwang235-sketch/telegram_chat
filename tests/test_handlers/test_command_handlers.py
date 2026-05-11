"""Unit tests for Command Handlers module."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Message, User, Chat

from src.handlers.command_handlers import (
    StartCommandHandler,
    HelpCommandHandler,
    StyleCommandHandler,
    SetStyleCommandHandler,
    ClearCommandHandler,
)


class TestStartCommandHandler:
    """Test suite for StartCommandHandler."""

    @pytest.mark.asyncio
    async def test_start_command_new_user(self):
        """Test /start command for new user."""
        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = None
        mock_user_repo.create.return_value = None

        handler = StartCommandHandler(user_repo=mock_user_repo)

        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123
        update.effective_user.username = "testuser"
        update.effective_user.first_name = "Test"

        update.effective_message = MagicMock(spec=Message)
        update.effective_message.reply_text = AsyncMock()

        context = MagicMock()

        await handler.handle(update, context)

        update.effective_message.reply_text.assert_called_once()
        call_args = update.effective_message.reply_text.call_args
        assert "欢迎" in str(call_args) or "welcome" in str(call_args).lower()

    @pytest.mark.asyncio
    async def test_start_command_existing_user(self):
        """Test /start command for existing user."""
        from src.models.user import User

        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = User(
            user_id=123,
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        handler = StartCommandHandler(user_repo=mock_user_repo)

        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123

        update.effective_message = MagicMock(spec=Message)
        update.effective_message.reply_text = AsyncMock()

        context = MagicMock()

        await handler.handle(update, context)

        update.effective_message.reply_text.assert_called_once()


class TestHelpCommandHandler:
    """Test suite for HelpCommandHandler."""

    @pytest.mark.asyncio
    async def test_help_command(self):
        """Test /help command."""
        handler = HelpCommandHandler()

        update = MagicMock(spec=Update)
        update.effective_message = MagicMock(spec=Message)
        update.effective_message.reply_text = AsyncMock()

        context = MagicMock()

        await handler.handle(update, context)

        update.effective_message.reply_text.assert_called_once()
        call_args = update.effective_message.reply_text.call_args
        help_text = str(call_args)
        assert "命令" in help_text or "command" in help_text.lower()


class TestStyleCommandHandler:
    """Test suite for StyleCommandHandler."""

    @pytest.mark.asyncio
    async def test_style_command(self):
        """Test /style command."""
        mock_style_service = MagicMock()
        mock_style_service.get_all_styles.return_value = [
            {
                "style_id": 1,
                "name": "幽默搞笑",
                "description": "幽默风趣",
            },
            {
                "style_id": 2,
                "name": "温柔体贴",
                "description": "温柔体贴",
            },
        ]

        handler = StyleCommandHandler(style_service=mock_style_service)

        update = MagicMock(spec=Update)
        update.effective_message = MagicMock(spec=Message)
        update.effective_message.reply_text = AsyncMock()

        context = MagicMock()

        await handler.handle(update, context)

        update.effective_message.reply_text.assert_called_once()
        call_args = update.effective_message.reply_text.call_args
        style_text = str(call_args)
        assert "风格" in style_text or "style" in style_text.lower()


class TestSetStyleCommandHandler:
    """Test suite for SetStyleCommandHandler."""

    @pytest.mark.asyncio
    async def test_set_style_command_valid(self):
        """Test /setstyle command with valid style."""
        mock_user_prefs_repo = AsyncMock()
        mock_user_prefs_repo.create_or_update.return_value = True

        handler = SetStyleCommandHandler(user_prefs_repo=mock_user_prefs_repo)

        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123

        update.effective_message = MagicMock(spec=Message)
        update.effective_message.reply_text = AsyncMock()

        context = MagicMock()
        context.args = ["1"]

        await handler.handle(update, context)

        update.effective_message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_style_command_no_args(self):
        """Test /setstyle command without arguments."""
        mock_user_prefs_repo = AsyncMock()

        handler = SetStyleCommandHandler(user_prefs_repo=mock_user_prefs_repo)

        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123

        update.effective_message = MagicMock(spec=Message)
        update.effective_message.reply_text = AsyncMock()

        context = MagicMock()
        context.args = []

        await handler.handle(update, context)

        # Should provide usage instructions
        update.effective_message.reply_text.assert_called_once()


class TestClearCommandHandler:
    """Test suite for ClearCommandHandler."""

    @pytest.mark.asyncio
    async def test_clear_command(self):
        """Test /clear command."""
        mock_memory_manager = AsyncMock()
        mock_memory_manager.clear_user.return_value = None

        handler = ClearCommandHandler(memory_manager=mock_memory_manager)

        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123

        update.effective_message = MagicMock(spec=Message)
        update.effective_message.reply_text = AsyncMock()

        context = MagicMock()

        await handler.handle(update, context)

        mock_memory_manager.clear_user.assert_called_once_with(123, clear_long_term=False)
        update.effective_message.reply_text.assert_called_once()
        call_args = update.effective_message.reply_text.call_args
        assert "清除" in str(call_args) or "clear" in str(call_args).lower()
