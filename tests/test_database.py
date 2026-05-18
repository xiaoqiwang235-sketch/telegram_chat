"""Test database functionality for both MySQL and SQLite."""

import asyncio
import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_sqlite():
    """Test SQLite database operations."""
    print("=" * 50)
    print("Testing SQLite Database")
    print("=" * 50)

    # Set SQLite configuration
    os.environ["DB_TYPE"] = "sqlite"
    os.environ["DB_PATH"] = "test_data/test.db"

    from src.database.config import get_database_config, _config_instance
    from src.database.connection_pool import ConnectionPool, _pool_instance
    from src.repositories.user_repository import UserRepository
    from src.repositories.conversation_repository import ConversationRepository
    from src.models.user import User
    from src.models.conversation import Conversation
    from datetime import datetime

    # Reset singletons
    global _config_instance, _pool_instance
    _config_instance = None
    _pool_instance = None

    try:
        # Get configuration
        config = get_database_config()
        print(f"✓ Config loaded: DB_TYPE={config.db_type}, DB_PATH={config.db_path}")

        # Ensure test directory exists
        os.makedirs("test_data", exist_ok=True)

        # Create pool
        pool = ConnectionPool(config)
        await pool.initialize()
        print("✓ Connection pool initialized")

        # Initialize database tables
        import aiosqlite
        async with aiosqlite.connect(config.db_path) as conn:
            # Create users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT NOT NULL,
                    last_name TEXT,
                    language_code TEXT,
                    is_bot INTEGER DEFAULT 0,
                    is_premium INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Create conversations table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    group_id INTEGER,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    message_id INTEGER,
                    style_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            await conn.commit()
        print("✓ Tables created")

        # Test UserRepository
        user_repo = UserRepository(pool)

        # Create user
        test_user = User(
            user_id=123456,
            username="testuser",
            first_name="Test",
            last_name="User",
            language_code="en",
            is_bot=False,
            is_premium=False,
        )
        await user_repo.create(test_user)
        print("✓ User created")

        # Get user
        retrieved_user = await user_repo.get_by_id(123456)
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        print(f"✓ User retrieved: {retrieved_user.username}")

        # Update user
        retrieved_user.username = "updateduser"
        await user_repo.update(retrieved_user)
        print("✓ User updated")

        # Check exists
        assert await user_repo.exists(123456)
        print("✓ User exists check passed")

        # Count users
        count = await user_repo.count()
        assert count == 1
        print(f"✓ User count: {count}")

        # Test ConversationRepository
        conv_repo = ConversationRepository(pool)

        # Create conversation
        test_conv = Conversation(
            user_id=123456,
            group_id=None,
            role="user",
            content="Hello, world!",
            timestamp=datetime.now(),
            message_id=1,
            style_id=1,
        )
        created_conv = await conv_repo.create(test_conv)
        assert created_conv.conversation_id is not None
        print(f"✓ Conversation created with ID: {created_conv.conversation_id}")

        # Get conversation
        retrieved_conv = await conv_repo.get_by_id(created_conv.conversation_id)
        assert retrieved_conv is not None
        assert retrieved_conv.content == "Hello, world!"
        print(f"✓ Conversation retrieved: {retrieved_conv.content}")

        # Get by user
        user_convs = await conv_repo.get_by_user_id(123456)
        assert len(user_convs) == 1
        print(f"✓ User conversations: {len(user_convs)}")

        # Count by user
        user_conv_count = await conv_repo.count_by_user(123456)
        assert user_conv_count == 1
        print(f"✓ User conversation count: {user_conv_count}")

        # Delete conversation
        await conv_repo.delete(created_conv.conversation_id)
        print("✓ Conversation deleted")

        # Cleanup
        await pool.close()
        print("✓ Connection pool closed")

        # Clean up test database
        import shutil
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        print("✓ Test database cleaned up")

        print("\n" + "=" * 50)
        print("All SQLite tests passed! ✓")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"\n✗ SQLite test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_base_repository():
    """Test BaseRepository query formatting."""
    print("\n" + "=" * 50)
    print("Testing BaseRepository Query Formatting")
    print("=" * 50)

    os.environ["DB_TYPE"] = "sqlite"
    os.environ["DB_PATH"] = "test_data/test.db"

    from src.database.config import get_database_config, _config_instance
    from src.database.connection_pool import ConnectionPool, _pool_instance
    from src.repositories.base_repository import BaseRepository

    # Reset singletons
    import src.database.config as config_module
    import src.database.connection_pool as pool_module
    config_module._config_instance = None
    pool_module._pool_instance = None

    try:
        config = get_database_config()
        pool = ConnectionPool(config)
        await pool.initialize()

        repo = BaseRepository(pool)

        # Test query formatting
        mysql_query = "SELECT * FROM users WHERE user_id = %s AND username = %s"
        formatted = repo._format_query(mysql_query)
        expected = "SELECT * FROM users WHERE user_id = ? AND username = ?"
        assert formatted == expected, f"Expected '{expected}', got '{formatted}'"
        print(f"✓ Query formatting: {formatted}")

        await pool.close()

        import shutil
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")

        print("\n" + "=" * 50)
        print("All BaseRepository tests passed! ✓")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"\n✗ BaseRepository test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all database tests."""
    results = []

    # Test base repository
    results.append(await test_base_repository())

    # Test SQLite
    results.append(await test_sqlite())

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print(f"Passed: {sum(results)}/{len(results)}")
    if all(results):
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
