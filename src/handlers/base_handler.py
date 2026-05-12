"""Base handler for Telegram updates."""

from telegram import Update
from telegram.ext import ContextTypes


class BaseHandler:
    """Base class for Telegram handlers."""

    async def pre_process(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Pre-process update before handling.

        Args:
            update: Telegram update
            context: Bot context
        """
        pass

    async def post_process(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Post-process update after handling.

        Args:
            update: Telegram update
            context: Bot context
        """
        pass
