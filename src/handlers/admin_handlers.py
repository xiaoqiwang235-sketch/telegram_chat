"""Admin command handlers for group management."""

from telegram import Update
from telegram.ext import ContextTypes
from typing import List

from src.handlers.base_handler import BaseHandler
from src.repositories.group_settings_repository import GroupSettingsRepository
from src.repositories.user_repository import UserRepository
from src.memory.memory_manager import MemoryManager


class GroupStyleCommandHandler(BaseHandler):
    """Handler for /groupstyle command (admin only)."""

    def __init__(
        self,
        group_repo: GroupSettingsRepository,
        admin_ids: List[int],
    ) -> None:
        """Initialize group style command handler.

        Args:
            group_repo: Group settings repository
            admin_ids: List of admin user IDs
        """
        super().__init__()
        self.group_repo = group_repo
        self.admin_ids = admin_ids

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /groupstyle command.

        Args:
            update: Telegram update
            context: Bot context
        """
        # Check if user is admin
        if update.effective_user.id not in self.admin_ids:
            await update.effective_message.reply_text(
                "❌ 此命令仅管理员可用。"
            )
            return

        # Check if in group
        if update.effective_chat.type not in ["group", "supergroup"]:
            await update.effective_message.reply_text(
                "此命令仅在群组中可用。"
            )
            return

        group_id = update.effective_chat.id

        if not context.args or len(context.args) == 0:
            # Show current style
            settings = await self.group_repo.get_by_id(group_id)
            if settings:
                style_names = {
                    1: "幽默搞笑",
                    2: "温柔体贴",
                    3: "傲娇",
                    4: "严肃专业",
                    5: "卖萌可爱",
                    6: "知性理性",
                }
                current_style = style_names.get(settings.style_id, "Unknown")
                await update.effective_message.reply_text(
                    f"当前群组风格: {current_style}\n\n"
                    f"用法: /groupstyle <编号>\n"
                    f"可用风格: 1-6"
                )
            else:
                await update.effective_message.reply_text(
                    "群组尚未设置风格。\n\n"
                    "用法: /groupstyle <编号>\n"
                    "可用风格: 1-6"
                )
            return

        try:
            style_id = int(context.args[0])

            if not (1 <= style_id <= 6):
                await update.effective_message.reply_text(
                    "无效的风格编号。请使用 1-6 之间的数字。"
                )
                return

            # Set or create group settings
            await self.group_repo.create_or_update(
                group_id=group_id,
                style_id=style_id,
                welcome_message=None,
                auto_reply_enabled=True,
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
                f"✅ 群组对话风格已设置为: {style_names[style_id]}"
            )

        except ValueError:
            await update.effective_message.reply_text(
                "无效的格式。请使用数字，例如: /groupstyle 1"
            )


class ResetUserCommandHandler(BaseHandler):
    """Handler for /resetuser command (admin only)."""

    def __init__(
        self,
        memory_manager: MemoryManager,
        admin_ids: List[int],
    ) -> None:
        """Initialize reset user command handler.

        Args:
            memory_manager: Memory manager
            admin_ids: List of admin user IDs
        """
        super().__init__()
        self.memory_manager = memory_manager
        self.admin_ids = admin_ids

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /resetuser command.

        Args:
            update: Telegram update
            context: Bot context
        """
        # Check if user is admin
        if update.effective_user.id not in self.admin_ids:
            await update.effective_message.reply_text(
                "❌ 此命令仅管理员可用。"
            )
            return

        if not context.args or len(context.args) == 0:
            await update.effective_message.reply_text(
                "用法: /resetuser <用户ID>\n\n"
                "回复用户消息或使用其用户ID来重置其对话记录。"
            )
            return

        try:
            # Parse user ID
            if context.args[0].startswith("@"):
                # Username provided (would need to lookup)
                username = context.args[0].lstrip("@")
                await update.effective_message.reply_text(
                    f"❌ 不支持用户名查找，请使用用户ID。"
                )
                return
            else:
                user_id = int(context.args[0])

            # Reset user memory
            await self.memory_manager.clear_user(user_id, clear_long_term=True)

            await update.effective_message.reply_text(
                f"✅ 用户 {user_id} 的对话记录已重置。"
            )

        except ValueError:
            await update.effective_message.reply_text(
                "无效的格式。请使用数字用户ID。"
            )


class StatsCommandHandler(BaseHandler):
    """Handler for /stats command (admin only)."""

    def __init__(
        self,
        memory_manager: MemoryManager,
        admin_ids: List[int],
    ) -> None:
        """Initialize stats command handler.

        Args:
            memory_manager: Memory manager
            admin_ids: List of admin user IDs
        """
        super().__init__()
        self.memory_manager = memory_manager
        self.admin_ids = admin_ids

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /stats command.

        Args:
            update: Telegram update
            context: Bot context
        """
        # Check if user is admin
        if update.effective_user.id not in self.admin_ids:
            await update.effective_message.reply_text(
                "❌ 此命令仅管理员可用。"
            )
            return

        # Get statistics
        stats = await self.memory_manager.get_stats()

        stats_text = f"""📊 *机器人统计*

👥 总用户数: {stats['total_users']}
💬 短期消息: {stats['short_term_messages']}
🗃️ 长期消息: {stats['long_term_messages']}
📝 总消息数: {stats['total_messages']}"""

        await update.effective_message.reply_text(stats_text, parse_mode="Markdown")
