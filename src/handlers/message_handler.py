"""Message handler for processing Telegram messages."""

import re
from telegram import Update
from telegram.ext import ContextTypes

from src.handlers.base_handler import BaseHandler
from src.services.chat_service import ChatService


class MessageHandler(BaseHandler):
    """Handler for processing text messages.

    Attributes:
        chat_service: Chat service for processing messages
    """

    def __init__(self, chat_service: ChatService) -> None:
        """Initialize message handler.

        Args:
            chat_service: Chat service instance
        """
        super().__init__()
        self.chat_service = chat_service

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming message.

        Args:
            update: Telegram update
            context: Bot context
        """
        await self.pre_process(update, context)

        try:
            # Extract message info
            user_id = update.effective_user.id
            message_text = update.effective_message.text

            # Check if private chat or group
            chat_type = update.effective_chat.type
            group_id = None
            bot_mentioned = True

            if chat_type in ["group", "supergroup"]:
                group_id = update.effective_chat.id
                # Check if bot was mentioned
                bot_mentioned = self._is_bot_mentioned(message_text, context)

            # Process message
            response = await self.chat_service.process_message(
                user_id=user_id,
                message=message_text,
                group_id=group_id,
                bot_mentioned=bot_mentioned,
            )

            # Send response if generated
            if response is not None:
                await update.effective_message.reply_text(response)

        except Exception as e:
            # Handle error gracefully
            error_message = f"抱歉，处理消息时出错: {str(e)}"
            await update.effective_message.reply_text(error_message)

        await self.post_process(update, context)

    def _is_bot_mentioned(
        self, message: str, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Check if bot was mentioned in message.

        Args:
            message: Message text
            context: Bot context

        Returns:
            True if bot was mentioned, False otherwise
        """
        if not message:
            return False

        # Get bot username
        bot_username = context.bot.username

        # Check for @mention
        mention_pattern = f"@{re.escape(bot_username)}"
        if re.search(mention_pattern, message, re.IGNORECASE):
            return True

        return False
