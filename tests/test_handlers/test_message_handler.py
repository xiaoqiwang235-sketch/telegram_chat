"""Unit tests for Message Handler module."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Message, User, Chat

from src.handlers.message_handler import MessageHandler


class TestMessageHandler:
    """Test suite for MessageHandler class."""

    @pytest.mark.asyncio
    async def test_message_handler_private_chat(self):
        """Test handling private chat message."""
        mock_chat_service = AsyncMock()
        mock_chat_service.process_message.return_value = "Hello!"

        handler = MessageHandler(chat_service=mock_chat_service)

        # Create mock update
        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123
        update.effective_user.username = "testuser"
        update.effective_user.first_name = "Test"
        update.effective_user.last_name = "User"

        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = 123
        update.effective_chat.type = "private"

        update.message = MagicMock(spec=Message)
        update.message.text = "Hello bot"
        update.message.message_id = 1001

        update.effective_message = update.message

        context = MagicMock()

        await handler.handle(update, context)

        # Verify chat service was called
        mock_chat_service.process_message.assert_called_once_with(
            user_id=123,
            message="Hello bot",
            group_id=None,
            bot_mentioned=True,
        )

    @pytest.mark.asyncio
    async def test_message_handler_group_chat_with_mention(self):
        """Test handling group chat message with bot mention."""
        mock_chat_service = AsyncMock()
        mock_chat_service.process_message.return_value = "@testuser Hello!"

        handler = MessageHandler(chat_service=mock_chat_service)

        # Create mock update
        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123
        update.effective_user.username = "testuser"

        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = 456
        update.effective_chat.type = "group"

        update.message = MagicMock(spec=Message)
        update.message.text = "@botname Hello"
        update.message.message_id = 1002
        update.message.reply_text = AsyncMock()

        update.effective_message = update.message

        context = MagicMock()

        await handler.handle(update, context)

        # Verify response was sent
        update.message.reply_text.assert_called_once_with("@testuser Hello!")

    @pytest.mark.asyncio
    async def test_message_handler_group_chat_without_mention(self):
        """Test handling group chat message without bot mention."""
        mock_chat_service = AsyncMock()
        mock_chat_service.process_message.return_value = None

        handler = MessageHandler(chat_service=mock_chat_service)

        # Create mock update
        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123

        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = 456
        update.effective_chat.type = "group"

        update.message = MagicMock(spec=Message)
        update.message.text = "Hello everyone"
        update.message.reply_text = AsyncMock()

        update.effective_message = update.message

        context = MagicMock()

        await handler.handle(update, context)

        # Should not reply if bot not mentioned
        update.message.reply_text.assert_not_called()

    @pytest.mark.asyncio
    async def test_message_handler_error_handling(self):
        """Test error handling in message handler."""
        mock_chat_service = AsyncMock()
        mock_chat_service.process_message.side_effect = Exception("API Error")

        handler = MessageHandler(chat_service=mock_chat_service)

        # Create mock update
        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123
        update.effective_user.username = "testuser"

        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = 123
        update.effective_chat.type = "private"

        update.message = MagicMock(spec=Message)
        update.message.text = "Hello"
        update.message.reply_text = AsyncMock()

        update.effective_message = update.message

        context = MagicMock()

        await handler.handle(update, context)

        # Should reply with error message
        update.message.reply_text.assert_called_once()
        call_args = update.message.reply_text.call_args
        assert "error" in str(call_args).lower() or "错误" in str(call_args)

    @pytest.mark.asyncio
    async def test_message_handler_empty_message(self):
        """Test handling empty message."""
        mock_chat_service = AsyncMock()

        handler = MessageHandler(chat_service=mock_chat_service)

        # Create mock update
        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123

        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = 123
        update.effective_chat.type = "private"

        update.message = MagicMock(spec=Message)
        update.message.text = ""
        update.message.reply_text = AsyncMock()

        update.effective_message = update.message

        context = MagicMock()

        await handler.handle(update, context)

        # Should not process empty messages
        mock_chat_service.process_message.assert_not_called()
