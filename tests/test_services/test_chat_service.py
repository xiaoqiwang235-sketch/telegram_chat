"""Unit tests for Chat Service module."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.chat_service import ChatService
from src.models.conversation import Conversation
from src.models.user import User


class TestChatService:
    """Test suite for ChatService class."""

    @pytest.mark.asyncio
    async def test_chat_service_initialization(self):
        """Test ChatService initialization."""
        mock_mimo_client = MagicMock()
        mock_memory_manager = AsyncMock()
        mock_style_service = MagicMock()
        mock_user_repo = AsyncMock()
        mock_group_repo = AsyncMock()

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_repo,
        )

        assert service.mimo_client == mock_mimo_client
        assert service.memory_manager == mock_memory_manager
        assert service.style_service == mock_style_service

    @pytest.mark.asyncio
    async def test_chat_service_process_private_message(self):
        """Test processing private chat message."""
        mock_mimo_client = AsyncMock()
        mock_mimo_client.generate_response.return_value = "你好！有什么可以帮助你的吗？"

        mock_memory_manager = AsyncMock()
        mock_memory_manager.get_context.return_value = []
        mock_memory_manager.has_user.return_value = False

        mock_style_service = MagicMock()
        mock_style_service.get_system_prompt.return_value = "你是一个友好的助手。"

        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = User(
            user_id=123,
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        mock_user_repo.create_or_update.return_value = None

        mock_group_repo = AsyncMock()

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_group_repo,
        )

        response = await service.process_message(
            user_id=123,
            message="你好",
            group_id=None,
        )

        assert response == "你好！有什么可以帮助你的吗？"
        mock_mimo_client.generate_response.assert_called_once()

    @pytest.mark.asyncio
    async def test_chat_service_process_group_message_with_mention(self):
        """Test processing group message with bot mention."""
        mock_mimo_client = AsyncMock()
        mock_mimo_client.generate_response.return_value = "@testuser 你好！"

        mock_memory_manager = AsyncMock()
        mock_memory_manager.get_context.return_value = []

        mock_style_service = MagicMock()
        mock_style_service.get_system_prompt.return_value = "你是一个友好的助手。"

        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = User(
            user_id=123,
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        mock_group_repo = AsyncMock()
        mock_group_repo.get_by_id.return_value = {
            "group_id": 456,
            "style_id": 1,
            "welcome_message": "Welcome!",
            "auto_reply_enabled": True,
            "language": "zh-CN",
        }

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_group_repo,
        )

        response = await service.process_message(
            user_id=123,
            message="@botname 你好",
            group_id=456,
            bot_mentioned=True,
        )

        assert response == "@testuser 你好！"
        mock_mimo_client.generate_response.assert_called_once()

    @pytest.mark.asyncio
    async def test_chat_service_process_group_without_mention(self):
        """Test processing group message without bot mention."""
        mock_mimo_client = AsyncMock()

        mock_memory_manager = AsyncMock()

        mock_style_service = MagicMock()

        mock_user_repo = AsyncMock()

        mock_group_repo = AsyncMock()

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_group_repo,
        )

        response = await service.process_message(
            user_id=123,
            message="大家好吗",
            group_id=456,
            bot_mentioned=False,
        )

        # Should return None if bot not mentioned
        assert response is None
        mock_mimo_client.generate_response.assert_not_called()

    @pytest.mark.asyncio
    async def test_chat_service_with_user_style(self):
        """Test processing message with user's preferred style."""
        mock_mimo_client = AsyncMock()
        mock_mimo_client.generate_response.return_value = "你好呀！😊"

        mock_memory_manager = AsyncMock()
        mock_memory_manager.get_context.return_value = []

        mock_style_service = MagicMock()
        mock_style_service.get_system_prompt.return_value = "你是一个温柔体贴的助手。"

        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = User(
            user_id=123,
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        mock_user_prefs_repo = AsyncMock()
        mock_user_prefs_repo.get_by_user_id.return_value = {
            "style_id": 2,
            "language": "zh-CN",
        }

        mock_group_repo = AsyncMock()

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_group_repo,
        )

        response = await service.process_message(
            user_id=123,
            message="你好",
            group_id=None,
        )

        assert response == "你好呀！😊"
        # Should use user's preferred style
        mock_style_service.get_system_prompt.assert_called_once_with(2)

    @pytest.mark.asyncio
    async def test_chat_service_with_memory_context(self):
        """Test processing message with conversation memory."""
        mock_mimo_client = AsyncMock()
        mock_mimo_client.generate_response.return_value = "我记得你刚才说的是..."

        mock_memory_manager = AsyncMock()
        mock_memory_manager.get_context.return_value = [
            Conversation(
                conversation_id=1,
                user_id=123,
                group_id=None,
                role="user",
                content="我今天心情不好",
                timestamp="2024-01-01 12:00:00",
                message_id=1001,
                style_id=1,
            )
        ]
        mock_memory_manager.has_user.return_value = True

        mock_style_service = MagicMock()
        mock_style_service.get_system_prompt.return_value = "你是一个友好的助手。"

        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = User(
            user_id=123,
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        mock_group_repo = AsyncMock()

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_group_repo,
        )

        response = await service.process_message(
            user_id=123,
            message="你能安慰我吗",
            group_id=None,
        )

        assert response == "我记得你刚才说的是..."

        # Verify memory context was included
        call_args = mock_mimo_client.generate_response.call_args
        messages = call_args[0][0]  # First positional argument

        # Should include previous conversation
        assert len(messages) > 1
        assert messages[0]["role"] == "system"

    @pytest.mark.asyncio
    async def test_chat_service_saves_conversation(self):
        """Test that conversation is saved to memory."""
        mock_mimo_client = AsyncMock()
        mock_mimo_client.generate_response.return_value = "Response"

        mock_memory_manager = AsyncMock()
        mock_memory_manager.get_context.return_value = []
        mock_memory_manager.has_user.return_value = False
        mock_memory_manager.add_message = AsyncMock()

        mock_style_service = MagicMock()
        mock_style_service.get_system_prompt.return_value = "System prompt"

        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = User(
            user_id=123,
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        mock_group_repo = AsyncMock()

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_group_repo,
        )

        await service.process_message(
            user_id=123,
            message="Hello",
            group_id=None,
        )

        # Verify conversation was saved
        mock_memory_manager.add_message.assert_called()

    @pytest.mark.asyncio
    async def test_chat_service_empty_message(self):
        """Test processing empty message."""
        service = ChatService(
            mimo_client=AsyncMock(),
            memory_manager=AsyncMock(),
            style_service=MagicMock(),
            user_repo=AsyncMock(),
            group_repo=AsyncMock(),
        )

        with pytest.raises(ValueError, match="Message cannot be empty"):
            await service.process_message(
                user_id=123,
                message="",
                group_id=None,
            )

    @pytest.mark.asyncio
    async def test_chat_service_with_custom_temperature(self):
        """Test processing message with custom temperature."""
        mock_mimo_client = AsyncMock()
        mock_mimo_client.generate_response.return_value = "Response"

        mock_memory_manager = AsyncMock()
        mock_memory_manager.get_context.return_value = []

        mock_style_service = MagicMock()
        mock_style_service.get_system_prompt.return_value = "System prompt"

        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = User(
            user_id=123,
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        mock_group_repo = AsyncMock()

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_group_repo,
        )

        await service.process_message(
            user_id=123,
            message="Hello",
            group_id=None,
            temperature=0.5,
        )

        # Verify temperature was passed
        call_args = mock_mimo_client.generate_response.call_args
        assert call_args.kwargs.get("temperature") == 0.5

    @pytest.mark.asyncio
    async def test_chat_service_error_handling(self):
        """Test error handling in chat service."""
        mock_mimo_client = AsyncMock()
        mock_mimo_client.generate_response.side_effect = Exception("API Error")

        mock_memory_manager = AsyncMock()
        mock_memory_manager.get_context.return_value = []

        mock_style_service = MagicMock()
        mock_style_service.get_system_prompt.return_value = "System prompt"

        mock_user_repo = AsyncMock()
        mock_user_repo.get_by_id.return_value = User(
            user_id=123,
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        mock_group_repo = AsyncMock()

        service = ChatService(
            mimo_client=mock_mimo_client,
            memory_manager=mock_memory_manager,
            style_service=mock_style_service,
            user_repo=mock_user_repo,
            group_repo=mock_group_repo,
        )

        with pytest.raises(Exception, match="API Error"):
            await service.process_message(
                user_id=123,
                message="Hello",
                group_id=None,
            )
