"""Command handlers for Telegram bot commands."""

from telegram import Update
from telegram.ext import ContextTypes

from src.handlers.base_handler import BaseHandler
from src.repositories.user_repository import UserRepository
from src.services.style_service import StyleService
from src.repositories.user_preferences_repository import UserPreferencesRepository
from src.memory.memory_manager import MemoryManager


class StartCommandHandler(BaseHandler):
    """Handler for /start command."""

    def __init__(self, user_repo: UserRepository) -> None:
        """Initialize start command handler.

        Args:
            user_repo: User repository
        """
        super().__init__()
        self.user_repo = user_repo

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command.

        Args:
            update: Telegram update
            context: Bot context
        """
        user_id = update.effective_user.id

        # Check if user exists
        user = await self.user_repo.get_by_id(user_id)

        if user is None:
            # Create new user
            from src.models.user import User

            user = User(
                user_id=user_id,
                username=update.effective_user.username,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name,
            )
            await self.user_repo.create(user)

            welcome_message = (
                f"欢迎 {user.first_name}！我是你的AI聊天助手。\n\n"
                "我可以陪你聊天，回答你的问题，还有很多有趣的功能。\n"
                "输入 /help 查看所有命令。"
            )
        else:
            welcome_message = f"欢迎回来，{user.first_name}！"

        await update.effective_message.reply_text(welcome_message)


class HelpCommandHandler(BaseHandler):
    """Handler for /help command."""

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command.

        Args:
            update: Telegram update
            context: Bot context
        """
        help_text = """📚 *可用命令*

*基础命令:*
/start - 开始使用机器人
/help - 显示此帮助信息

*对话风格:*
/style - 查看所有对话风格
/setstyle <编号> - 设置你的对话风格

*记忆管理:*
/clear - 清除短期对话记录

*对话风格:*
1. 幽默搞笑 - 轻松有趣，经常讲笑话
2. 温柔体贴 - 温暖关怀，理解感受
3. 傲娇 - 外冷内热，傲娇性格
4. 严肃专业 - 专业准确，理性分析
5. 卖萌可爱 - 俏皮活泼，可爱卖萌
6. 知性理性 - 深度思考，逻辑清晰

💡 在群组中，请 @我 来获得回复。"""

        await update.effective_message.reply_text(help_text, parse_mode="Markdown")


class StyleCommandHandler(BaseHandler):
    """Handler for /style command."""

    def __init__(self, style_service: StyleService) -> None:
        """Initialize style command handler.

        Args:
            style_service: Style service
        """
        super().__init__()
        self.style_service = style_service

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /style command.

        Args:
            update: Telegram update
            context: Bot context
        """
        styles = self.style_service.get_all_styles()

        style_list = "\n".join([
            f"{s['style_id']}. {s['name']} - {s['description']}"
            for s in styles
        ])

        message = f"🎭 *对话风格*\n\n{style_list}\n\n使用 /setstyle <编号> 来设置你的风格。"

        await update.effective_message.reply_text(message, parse_mode="Markdown")


class SetStyleCommandHandler(BaseHandler):
    """Handler for /setstyle command."""

    def __init__(self, user_prefs_repo: UserPreferencesRepository) -> None:
        """Initialize set style command handler.

        Args:
            user_prefs_repo: User preferences repository
        """
        super().__init__()
        self.user_prefs_repo = user_prefs_repo

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /setstyle command.

        Args:
            update: Telegram update
            context: Bot context
        """
        if not context.args or len(context.args) == 0:
            await update.effective_message.reply_text(
                "用法: /setstyle <风格编号>\n\n"
                "使用 /style 查看所有可用风格。"
            )
            return

        try:
            style_id = int(context.args[0])

            if not (1 <= style_id <= 6):
                await update.effective_message.reply_text(
                    "无效的风格编号。请使用 1-6 之间的数字。"
                )
                return

            # Set user preference
            await self.user_prefs_repo.create_or_update(
                user_id=update.effective_user.id,
                style_id=style_id,
                language="zh-CN",
            )

            style_names = {
                1: "幽默搞笑",
                2: "温柔体贴",
                3: "傲娇",
                4: "严肃专业",
                5: "卖萌可爱",
                6: "知性理性",
            }

            await update.effective_message.reply_text(
                f"✅ 对话风格已设置为: {style_names[style_id]}"
            )

        except ValueError:
            await update.effective_message.reply_text(
                "无效的格式。请使用数字，例如: /setstyle 1"
            )


class ClearCommandHandler(BaseHandler):
    """Handler for /clear command."""

    def __init__(self, memory_manager: MemoryManager) -> None:
        """Initialize clear command handler.

        Args:
            memory_manager: Memory manager
        """
        super().__init__()
        self.memory_manager = memory_manager

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /clear command.

        Args:
            update: Telegram update
            context: Bot context
        """
        user_id = update.effective_user.id

        # Clear short-term memory
        await self.memory_manager.clear_user(user_id, clear_long_term=False)

        await update.effective_message.reply_text(
            "✅ 短期对话记录已清除。\n\n"
            "注意：长期记忆保留。如需完全清除，请联系管理员。"
        )
