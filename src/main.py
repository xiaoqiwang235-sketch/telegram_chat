"""Main entry point for Telegram bot."""

import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from src.database.connection_pool import ConnectionPool
from src.database.config import get_database_config
from src.repositories.user_repository import UserRepository
from src.repositories.conversation_repository import ConversationRepository
from src.repositories.conversation_vector_repository import ConversationVectorRepository
from src.repositories.group_settings_repository import GroupSettingsRepository
from src.repositories.user_preferences_repository import UserPreferencesRepository

from src.memory.short_term_memory import ShortTermMemory
from src.memory.embedding_client import EmbeddingClient
from src.memory.faiss_manager import FaissManager
from src.memory.long_term_memory import LongTermMemory
from src.memory.memory_manager import MemoryManager

from src.services.style_service import StyleService
from src.services.chat_service import ChatService

from src.handlers.command_handlers import (
    StartCommandHandler,
    HelpCommandHandler,
    StyleCommandHandler,
    SetStyleCommandHandler,
    ClearCommandHandler,
)
from src.handlers.admin_handlers import (
    GroupStyleCommandHandler,
    ResetUserCommandHandler,
    StatsCommandHandler,
)
from src.handlers.message_handler import MessageHandler


async def setup_application() -> Application:
    """Setup and configure Telegram bot application.

    Returns:
        Configured bot application
    """
    # Get bot token from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

    # Get admin IDs
    admin_ids_str = os.getenv("TELEGRAM_ADMIN_USER_IDS", "")
    admin_ids = [int(uid.strip()) for uid in admin_ids_str.split(",") if uid.strip()]

    # Initialize database connection pool
    db_config = get_database_config()
    pool = ConnectionPool(db_config)
    await pool.initialize()

    # Initialize repositories
    user_repo = UserRepository(pool)
    conversation_repo = ConversationRepository(pool)
    vector_repo = ConversationVectorRepository(pool)
    group_repo = GroupSettingsRepository(pool)
    user_prefs_repo = UserPreferencesRepository(pool)

    # Initialize memory components
    short_term_memory = ShortTermMemory(max_messages=50)

    # Initialize embedding client
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_base_url = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com")
    embedding_client = EmbeddingClient(
        api_key=openai_api_key,
        base_url=openai_base_url,
        dimensions=1536,
    )

    # Initialize Faiss manager
    faiss_manager = FaissManager(dimension=1536)

    # Initialize long-term memory
    long_term_memory = LongTermMemory(
        embedding_client=embedding_client,
        faiss_manager=faiss_manager,
        conversation_repo=conversation_repo,
        vector_repo=vector_repo,
    )

    # Initialize memory manager
    memory_manager = MemoryManager(
        short_term_memory=short_term_memory,
        long_term_memory=long_term_memory,
    )

    # Initialize style service
    style_service = StyleService()

    # Initialize Mimo client
    mimo_api_key = os.getenv("MIMO_API_KEY")
    mimo_base_url = os.getenv("MIMO_API_BASE_URL", "https://api.xiaomimimo.com")
    from src.integrations.mimo_client import MimoClient

    mimo_client = MimoClient(
        api_key=mimo_api_key,
        base_url=mimo_base_url,
    )

    # Initialize chat service
    chat_service = ChatService(
        mimo_client=mimo_client,
        memory_manager=memory_manager,
        style_service=style_service,
        user_repo=user_repo,
        group_repo=group_repo,
    )

    # Initialize handlers
    start_handler = StartCommandHandler(user_repo)
    help_handler = HelpCommandHandler()
    style_handler = StyleCommandHandler(style_service)
    setstyle_handler = SetStyleCommandHandler(user_prefs_repo)
    clear_handler = ClearCommandHandler(memory_manager)

    group_style_handler = GroupStyleCommandHandler(group_repo, admin_ids)
    reset_user_handler = ResetUserCommandHandler(memory_manager, admin_ids)
    stats_handler = StatsCommandHandler(memory_manager, admin_ids)

    message_handler_obj = MessageHandler(chat_service=chat_service)

    # Create application
    application = Application.builder().token(bot_token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_handler.handle))
    application.add_handler(CommandHandler("help", help_handler.handle))
    application.add_handler(CommandHandler("style", style_handler.handle))
    application.add_handler(CommandHandler("setstyle", setstyle_handler.handle))
    application.add_handler(CommandHandler("clear", clear_handler.handle))

    # Register admin command handlers
    application.add_handler(CommandHandler("groupstyle", group_style_handler.handle))
    application.add_handler(CommandHandler("resetuser", reset_user_handler.handle))
    application.add_handler(CommandHandler("stats", stats_handler.handle))

    # Register message handler (must be last)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler_obj.handle)
    )

    # Register error handler
    async def error_handler(update: object, context: object) -> None:
        """Log errors caused by updates."""
        logging.error(f"Exception while handling an update: {context.error}")

    application.add_error_handler(error_handler)

    return application


def main() -> None:
    """Main entry point for running the bot."""
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # Run the bot
    application = None

    async def run_bot():
        nonlocal application

        application = await setup_application()

        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        # Keep the bot running
        try:
            while True:
                import asyncio
                await asyncio.sleep(3600)  # Sleep for 1 hour
        except KeyboardInterrupt:
            pass
        finally:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()

    import asyncio

    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
