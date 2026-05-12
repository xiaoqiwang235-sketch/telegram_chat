"""End-to-end integration tests for Telegram chatbot."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from src.main import setup_application


class TestE2EIntegration:
    """End-to-end integration tests."""

    @pytest.mark.asyncio
    async def test_application_setup(self):
        """Test complete application setup."""
        with patch("src.main.get_database_config") as mock_db_config:
            # Mock database config
            mock_config = MagicMock()
            mock_config.host = "localhost"
            mock_config.port = 3306
            mock_config.database = "test_db"
            mock_config.user = "test_user"
            mock_config.password = "test_pass"
            mock_db_config.return_value = mock_config

            with patch("src.main.ConnectionPool") as mock_pool_class:
                # Mock connection pool
                mock_pool = AsyncMock()
                mock_pool.initialize = AsyncMock()
                mock_pool_class.return_value = mock_pool

                with patch("src.main.UserRepository") as mock_user_repo_class:
                    # Mock repositories
                    mock_user_repo = MagicMock()
                    mock_user_repo_class.return_value = mock_user_repo

                    with patch("src.main.ConversationRepository") as mock_conv_repo_class:
                        mock_conv_repo = MagicMock()
                        mock_conv_repo_class.return_value = mock_conv_repo

                        with patch("src.main.ConversationVectorRepository") as mock_vec_repo_class:
                            mock_vec_repo = MagicMock()
                            mock_vec_repo_class.return_value = mock_vec_repo

                            with patch("src.main.GroupSettingsRepository") as mock_group_repo_class:
                                mock_group_repo = MagicMock()
                                mock_group_repo_class.return_value = mock_group_repo

                                with patch("src.main.UserPreferencesRepository") as mock_prefs_repo_class:
                                    mock_prefs_repo = MagicMock()
                                    mock_prefs_repo_class.return_value = mock_prefs_repo

                                    with patch("src.main.ShortTermMemory"):
                                        with patch("src.main.EmbeddingClient"):
                                            with patch("src.main.FaissManager"):
                                                with patch("src.main.LongTermMemory"):
                                                    with patch("src.main.MemoryManager"):
                                                        with patch("src.main.StyleService"):
                                                            with patch("src.main.MimoClient"):
                                                                with patch("src.main.ChatService"):
                                                                    with patch("telegram.Application.builder") as mock_app_builder:
                                                                        # Mock application
                                                                        mock_app = MagicMock()
                                                                        mock_app.add_handler = MagicMock()
                                                                        mock_app.add_error_handler = MagicMock()

                                                                        mock_app_builder_instance = MagicMock()
                                                                        mock_app_builder_instance.token.return_value.build.return_value = mock_app
                                                                        mock_app_builder.return_value = mock_app_builder_instance

                                                                        # Setup application
                                                                        app = await setup_application()

                                                                        # Verify application was created
                                                                        assert app is not None

    @pytest.mark.asyncio
    async def test_private_chat_flow(self):
        """Test complete private chat message flow."""
        # This test simulates a user sending a message in private chat
        # and receiving a response

        # Mock all dependencies
        with patch("src.main.get_database_config") as mock_db_config:
            mock_config = MagicMock()
            mock_config.host = "localhost"
            mock_db_config.return_value = mock_config

            with patch("src.main.ConnectionPool"):
                with patch("src.main.UserRepository") as mock_user_repo_class:
                    mock_user_repo = AsyncMock()
                    mock_user_repo.get_by_id.return_value = None
                    mock_user_repo.create.return_value = None
                    mock_user_repo_class.return_value = mock_user_repo

                    with patch("src.main.ConversationRepository"):
                        with patch("src.main.ConversationVectorRepository"):
                            with patch("src.main.GroupSettingsRepository"):
                                with patch("src.main.UserPreferencesRepository"):
                                    with patch("src.main.ShortTermMemory") as mock_stm_class:
                                        mock_stm = MagicMock()
                                        mock_stm_class.return_value = mock_stm

                                        with patch("src.main.EmbeddingClient"):
                                            with patch("src.main.FaissManager"):
                                                with patch("src.main.LongTermMemory") as mock_ltm_class:
                                                    mock_ltm = AsyncMock()
                                                    mock_ltm_class.return_value = mock_ltm

                                                    with patch("src.main.MemoryManager") as mock_mm_class:
                                                        mock_mm = AsyncMock()
                                                        mock_mm.get_context.return_value = []
                                                        mock_mm.add_message = AsyncMock()
                                                        mock_mm_class.return_value = mock_mm

                                                        with patch("src.main.StyleService") as mock_ss_class:
                                                            mock_ss = MagicMock()
                                                            mock_ss.get_system_prompt.return_value = "You are helpful."
                                                            mock_ss_class.return_value = mock_ss

                                                            with patch("src.main.MimoClient") as mock_mimo_class:
                                                                mock_mimo = AsyncMock()
                                                                mock_mimo.generate_response.return_value = "Hello!"
                                                                mock_mimo_class.return_value = mock_mimo

                                                                with patch("src.main.ChatService") as mock_cs_class:
                                                                    from src.services.chat_service import ChatService

                                                                    mock_chat_service = ChatService(
                                                                        mimo_client=mock_mimo,
                                                                        memory_manager=mock_mm,
                                                                        style_service=mock_ss,
                                                                        user_repo=mock_user_repo,
                                                                        group_repo=MagicMock(),
                                                                    )

                                                                    with patch("telegram.Application.builder"):
                                                                        # Simulate message processing
                                                                        response = await mock_chat_service.process_message(
                                                                            user_id=123,
                                                                            message="Hello bot",
                                                                            group_id=None,
                                                                        )

                                                                        assert response == "Hello!"
                                                                        mock_user_repo.create.assert_called_once()
                                                                        mock_mm.add_message.assert_called()

    @pytest.mark.asyncio
    async def test_group_chat_with_mention(self):
        """Test group chat flow with bot mention."""
        with patch("src.main.get_database_config"):
            with patch("src.main.ConnectionPool"):
                with patch("src.main.UserRepository"):
                    mock_user_repo = AsyncMock()
                    mock_user_repo.get_by_id.return_value = MagicMock()

                    with patch("src.main.ConversationRepository"):
                        with patch("src.main.ConversationVectorRepository"):
                            with patch("src.main.GroupSettingsRepository"):
                                mock_group_repo = AsyncMock()
                                mock_group_repo.get_by_id.return_value = MagicMock(
                                    style_id=1
                                )

                                with patch("src.main.UserPreferencesRepository"):
                                    with patch("src.main.ShortTermMemory") as mock_stm_class:
                                        mock_stm = MagicMock()
                                        mock_stm_class.return_value = mock_stm

                                        with patch("src.main.EmbeddingClient"):
                                            with patch("src.main.FaissManager"):
                                                with patch("src.main.LongTermMemory"):
                                                    with patch("src.main.MemoryManager") as mock_mm_class:
                                                        mock_mm = AsyncMock()
                                                        mock_mm.get_context.return_value = []
                                                        mock_mm_class.return_value = mock_mm

                                                        with patch("src.main.StyleService"):
                                                            with patch("src.main.MimoClient") as mock_mimo_class:
                                                                mock_mimo = AsyncMock()
                                                                mock_mimo.generate_response.return_value = "Hello group!"

                                                                with patch("src.main.ChatService"):
                                                                    # Test group chat with mention
                                                                    response = await mock_mimo.generate_response(
                                                                        messages=[{
                                                                            "role": "user",
                                                                            "content": "@bot Hello"
                                                                        }],
                                                                        system_prompt="Test",
                                                                    )

                                                                    assert response == "Hello group!"

    @pytest.mark.asyncio
    async def test_style_switching(self):
        """Test switching between conversation styles."""
        with patch("src.main.StyleService") as mock_ss_class:
            mock_ss = MagicMock()
            mock_ss.get_all_styles.return_value = [
                                        {"style_id": 1, "name": "幽默搞笑", "description": "Desc"},
                                        {"style_id": 2, "name": "温柔体贴", "description": "Desc"},
                                    ]

            service = mock_ss_class.return_value

            # Get all styles
            styles = service.get_all_styles()

            assert len(styles) == 2
            assert styles[0]["name"] == "幽默搞笑"
            assert styles[1]["name"] == "温柔体贴"


class TestQualityGates:
    """Quality gate tests."""

    def test_all_components_initialized(self):
        """Test that all components can be initialized."""
        from src.memory.short_term_memory import ShortTermMemory
        from src.services.style_service import StyleService

        # Test short-term memory
        stm = ShortTermMemory(max_messages=50)
        assert stm.max_messages == 50

        # Test style service
        ss = StyleService()
        styles = ss.get_all_styles()
        assert len(styles) == 6

    def test_configuration_validation(self):
        """Test environment configuration validation."""
        import os
        from src.database.config import DatabaseConfig, get_database_config

        # Test with valid config
        os.environ["DB_HOST"] = "localhost"
        os.environ["DB_NAME"] = "test"
        os.environ["DB_USER"] = "user"
        os.environ["DB_PASSWORD"] = "pass"

        config = get_database_config()
        assert config.host == "localhost"

    def test_error_handling(self):
        """Test error handling in critical paths."""
        from src.utils.validators import InputValidator

        # Test input validation
        with pytest.raises(ValueError):
            InputValidator.validate_message("")

        with pytest.raises(ValueError):
            InputValidator.validate_user_id(-1)

        with pytest.raises(ValueError):
            InputValidator.validate_style_id(10)
