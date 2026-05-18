"""Test script to check network connectivity for Telegram bot."""

import os
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_telegram_api():
    """Test connection to Telegram API."""
    try:
        from telegram import Bot
        from telegram.error import TelegramError

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            print("[ERROR] TELEGRAM_BOT_TOKEN not found in .env file")
            return False

        # Configure proxy if available
        proxy_url = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")

        print("[INFO] Testing Telegram API connection...")
        print(f"[INFO] Bot token: {bot_token[:20]}...")

        # Create bot (proxy is configured later via Application.builder)
        bot = Bot(token=bot_token)

        if proxy_url:
            print(f"[INFO] Using proxy: {proxy_url}")

        print("[INFO] Fetching bot info...")
        bot_info = await bot.get_me()

        print(f"[SUCCESS] Bot connected successfully!")
        print(f"  - Bot ID: {bot_info.id}")
        print(f"  - Bot Name: @{bot_info.username}")
        print(f"  - Bot Display Name: {bot_info.first_name}")

        await bot.shutdown()
        return True

    except TelegramError as e:
        print(f"[ERROR] Telegram API Error: {e}")
        print("\nPossible solutions:")
        print("1. Configure proxy in .env file (HTTP_PROXY or HTTPS_PROXY)")
        print("2. Check if your bot token is correct")
        print("3. Increase timeout values in .env file")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

async def test_database():
    """Test database connection."""
    try:
        from src.database.connection_pool import ConnectionPool
        from src.database.config import get_database_config

        print("\n[INFO] Testing database connection...")

        db_config = get_database_config()
        print(f"[INFO] Database: {db_config.database}@{db_config.host}:{db_config.port}")

        pool = ConnectionPool(db_config)
        await pool.initialize()

        conn = await pool.acquire()
        try:
            result = await conn.execute("SELECT 1")
            print("[SUCCESS] Database connection working!")
        finally:
            await pool.release(conn)

        await pool.close()
        return True

    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        print("\nPossible solutions:")
        print("1. Make sure MySQL service is running")
        print("2. Check database credentials in .env file")
        print("3. Verify the database 'telegram_chatbot' exists")
        return False

async def test_local_model():
    """Test local embedding model."""
    try:
        from src.memory.local_embedding_client import LocalEmbeddingClient

        print("\n[INFO] Testing local embedding model...")

        # Set HuggingFace mirror
        hf_endpoint = os.getenv("HF_ENDPOINT")
        if hf_endpoint:
            import os as os_module
            os_module.environ["HF_ENDPOINT"] = hf_endpoint
            print(f"[INFO] Using HuggingFace mirror: {hf_endpoint}")

        model_name = os.getenv("LOCAL_EMBEDDING_MODEL", "moka-ai/m3e-base")
        print(f"[INFO] Loading model: {model_name}")

        client = LocalEmbeddingClient(
            model_name=model_name,
            dimensions=768,
            device="cpu"
        )

        # Test embedding
        text = "Hello, world!"
        embedding = await client.generate_embedding(text)

        print(f"[SUCCESS] Model loaded successfully!")
        print(f"  - Model: {model_name}")
        print(f"  - Dimensions: {len(embedding)}")
        print(f"  - Test embedding shape: {embedding.shape}")

        return True

    except Exception as e:
        print(f"[ERROR] Model loading failed: {e}")
        print("\nPossible solutions:")
        print("1. Make sure you have internet connection for first-time download")
        print("2. Set HF_ENDPOINT=https://hf-mirror.com in .env file")
        print("3. Be patient, model download takes time (400MB)")
        return False

async def main():
    """Run all tests."""
    print("=" * 50)
    print("Telegram Bot Network Diagnostic Tool")
    print("=" * 50)
    print()

    results = {
        "Telegram API": await test_telegram_api(),
        "Database": await test_database(),
        "Local Model": await test_local_model(),
    }

    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)

    for component, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {component}")

    all_passed = all(results.values())

    if all_passed:
        print("\n[SUCCESS] All tests passed! Your bot should work correctly.")
        print("\nYou can now start the bot with:")
        print("  uv run python -m src.main")
        print("  or")
        print("  start_bot_with_proxy.bat")
    else:
        print("\n[WARNING] Some tests failed. Please fix the issues above before starting the bot.")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
