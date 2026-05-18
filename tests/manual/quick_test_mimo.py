"""Quick test for MiMo API."""

import asyncio
import os
from dotenv import load_dotenv
from src.integrations.mimo_client import MimoClient

load_dotenv()


async def quick_test():
    """Quick test of MiMo API."""
    print("=" * 60)
    print("MiMo API Quick Test")
    print("=" * 60)

    # Get configuration
    api_key = os.getenv("MIMO_API_KEY")
    base_url = os.getenv("MIMO_API_BASE_URL")
    model = os.getenv("MIMO_MODEL")
    proxy_url = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")

    print(f"\n[Configuration]")
    print(f"API Key: {api_key[:20]}...")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print(f"Proxy: {proxy_url}")

    # Create client
    client = MimoClient(
        api_key=api_key,
        base_url=base_url,
        model=model,
        proxy_url=proxy_url,
    )

    print("\n[Test 1] Simple conversation")
    try:
        response = await client.generate_response(
            messages=[{"role": "user", "content": "Hello, please respond with 'API OK'"}],
            system_prompt="You are a helpful assistant.",
            temperature=0.7,
            max_tokens=50,
        )
        print(f"[SUCCESS] Response: {response}")
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

    print("\n[Test 2] Chinese conversation")
    try:
        response = await client.generate_response(
            messages=[{"role": "user", "content": "你好"}],
            system_prompt="你是一个友好的AI助手。",
            temperature=0.7,
            max_tokens=100,
        )
        print(f"[SUCCESS] Response: {response[:100]}...")
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

    print("\n[Test 3] Coding question")
    try:
        response = await client.generate_response(
            messages=[{"role": "user", "content": "What is Python?"}],
            system_prompt="You are a programming expert.",
            temperature=0.5,
            max_tokens=200,
        )
        print(f"[SUCCESS] Response: {response[:150]}...")
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

    print("\n" + "=" * 60)
    print("[SUCCESS] All tests passed! MiMo API is working perfectly!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = asyncio.run(quick_test())
    exit(0 if success else 1)
