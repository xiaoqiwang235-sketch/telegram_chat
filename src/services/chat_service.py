"""Chat service for processing conversations."""

from typing import Optional
from datetime import datetime

from src.services.style_service import StyleService
from src.memory.memory_manager import MemoryManager
from src.models.conversation import Conversation
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.repositories.group_settings_repository import GroupSettingsRepository
from src.integrations.mimo_client import MimoClient
from src.utils.validators import InputValidator


class ChatService:
    """Service for processing chat messages and generating responses.

    Attributes:
        mimo_client: XiaoMi MiMo API client
        memory_manager: Memory manager for context
        style_service: Style management service
        user_repo: User repository
        group_repo: Group settings repository
    """

    def __init__(
        self,
        mimo_client: MimoClient,
        memory_manager: MemoryManager,
        style_service: StyleService,
        user_repo: UserRepository,
        group_repo: GroupSettingsRepository,
    ) -> None:
        """Initialize chat service.

        Args:
            mimo_client: Mimo API client
            memory_manager: Memory manager
            style_service: Style service
            user_repo: User repository
            group_repo: Group settings repository
        """
        self.mimo_client = mimo_client
        self.memory_manager = memory_manager
        self.style_service = style_service
        self.user_repo = user_repo
        self.group_repo = group_repo

    async def process_message(
        self,
        user_id: int,
        message: str,
        group_id: Optional[int] = None,
        bot_mentioned: bool = True,
        temperature: float = 0.7,
    ) -> Optional[str]:
        """Process a chat message and generate response.

        Args:
            user_id: User ID
            message: User message
            group_id: Optional group ID
            bot_mentioned: Whether bot was mentioned (for groups)
            temperature: Sampling temperature

        Returns:
            Bot response or None if bot should not respond

        Raises:
            ValueError: If message is empty
        """
        # Validate input
        message = InputValidator.validate_message(message)

        # For group chats, only respond if mentioned
        if group_id is not None and not bot_mentioned:
            return None

        # Get or create user
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            user = User(
                user_id=user_id,
                username=None,
                first_name="User",
                last_name=None,
            )
            await self.user_repo.create(user)

        # Determine style to use
        # Priority: User preference > Group setting > Default
        style_id = await self._determine_style(user_id, group_id)

        # Get system prompt for style
        system_prompt = self.style_service.get_system_prompt(style_id)

        # Get conversation context
        context = await self.memory_manager.get_context(user_id, group_id)

        # Prepare messages for API
        messages = []
        for conv in context:
            messages.append({
                "role": conv.role,
                "content": conv.content,
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": message,
        })

        # Generate response
        try:
            response = await self.mimo_client.generate_response(
                messages=messages,
                system_prompt=system_prompt,
                temperature=temperature,
            )

            # Save conversation to memory
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save user message
            user_conversation = Conversation(
                conversation_id=0,  # Will be assigned by database
                user_id=user_id,
                group_id=group_id,
                role="user",
                content=message,
                timestamp=timestamp,
                message_id=None,
                style_id=style_id,
            )
            await self.memory_manager.add_message(user_conversation, save_long_term=True)

            # Save assistant response
            assistant_conversation = Conversation(
                conversation_id=0,
                user_id=user_id,
                group_id=group_id,
                role="assistant",
                content=response,
                timestamp=timestamp,
                message_id=None,
                style_id=style_id,
            )
            await self.memory_manager.add_message(
                assistant_conversation, save_long_term=True
            )

            return response

        except Exception as e:
            # Log error and re-raise
            raise Exception(f"Failed to process message: {e}")

    async def _determine_style(
        self, user_id: int, group_id: Optional[int]
    ) -> int:
        """Determine conversation style to use.

        Priority: User preference > Group setting > Default (1)

        Args:
            user_id: User ID
            group_id: Optional group ID

        Returns:
            Style ID (1-6)
        """
        # Default style
        default_style = 1

        # For group chats, use group setting if available
        if group_id is not None:
            group_settings = await self.group_repo.get_by_id(group_id)
            if group_settings is not None:
                return group_settings.style_id

        # For private chats, use user preference if available
        # This would require UserPreferencesRepository
        # For now, return default
        return default_style
