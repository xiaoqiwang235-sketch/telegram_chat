"""Test script for XiaoMi MiMo API integration."""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.integrations.mimo_client import MimoClient


async def test_basic_connection():
    """Test basic API connectivity."""
    print("=" * 60)
    print("测试 1: 基本 API 连接")
    print("=" * 60)

    try:
        # Get configuration
        api_key = os.getenv("MIMO_API_KEY")
        base_url = os.getenv("MIMO_API_BASE_URL", "https://api.xiaomimimo.com")
        model = os.getenv("MIMO_MODEL", "mi-mimo-model")

        if not api_key:
            print("[ERROR] MIMO_API_KEY not found in .env file")
            return False

        print(f"[INFO] API Key: {api_key[:20]}...")
        print(f"[INFO] Base URL: {base_url}")
        print(f"[INFO] Model: {model}")

        # Create client
        client = MimoClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout=30.0,
        )

        print("[SUCCESS] MimoClient created successfully")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to create client: {e}")
        return False


async def test_simple_conversation():
    """Test simple conversation."""
    print("\n" + "=" * 60)
    print("测试 2: 简单对话")
    print("=" * 60)

    try:
        # Create client
        api_key = os.getenv("MIMO_API_KEY")
        base_url = os.getenv("MIMO_API_BASE_URL", "https://api.xiaomimimo.com")
        model = os.getenv("MIMO_MODEL", "mi-mimo-model")

        client = MimoClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout=30.0,
        )

        # Prepare messages
        messages = [
            {"role": "user", "content": "你好，请简单介绍一下你自己。"}
        ]
        system_prompt = "你是一个友好的AI助手，请用中文回答。"

        print(f"[INFO] 发送消息: {messages[0]['content']}")
        print("[INFO] 等待响应...")

        # Generate response
        response = await client.generate_response(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=500,
        )

        print(f"\n[SUCCESS] 收到回复:")
        print(f"{'-' * 60}")
        print(response)
        print(f"{'-' * 60}")
        print(f"回复长度: {len(response)} 字符")
        return True

    except Exception as e:
        print(f"[ERROR] 对话失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_multi_turn_conversation():
    """Test multi-turn conversation."""
    print("\n" + "=" * 60)
    print("测试 3: 多轮对话")
    print("=" * 60)

    try:
        # Create client
        api_key = os.getenv("MIMO_API_KEY")
        base_url = os.getenv("MIMO_API_BASE_URL", "https://api.xiaomimimo.com")
        model = os.getenv("MIMO_MODEL", "mi-mimo-model")

        client = MimoClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout=30.0,
        )

        # Multi-turn conversation
        messages = [
            {"role": "user", "content": "我喜欢编程，特别是Python。"},
        ]
        system_prompt = "你是一个友好的AI助手。"

        print(f"[第1轮] 用户: {messages[0]['content']}")

        response1 = await client.generate_response(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=200,
        )

        print(f"[第1轮] AI: {response1}")

        # Second turn
        messages.append({"role": "assistant", "content": response1})
        messages.append({"role": "user", "content": "有什么推荐的Python学习资源吗？"})

        print(f"\n[第2轮] 用户: {messages[-1]['content']}")

        response2 = await client.generate_response(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=300,
        )

        print(f"[第2轮] AI: {response2}")

        print("\n[SUCCESS] 多轮对话测试完成")
        return True

    except Exception as e:
        print(f"[ERROR] 多轮对话失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_different_parameters():
    """Test with different parameters."""
    print("\n" + "=" * 60)
    print("测试 4: 不同参数测试")
    print("=" * 60)

    try:
        # Create client
        api_key = os.getenv("MIMO_API_KEY")
        base_url = os.getenv("MIMO_API_BASE_URL", "https://api.xiaomimimo.com")
        model = os.getenv("MIMO_MODEL", "mi-mimo-model")

        client = MimoClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout=30.0,
        )

        test_message = {"role": "user", "content": "请用一句话解释什么是机器学习。"}

        # Test with low temperature (more focused)
        print("[测试] Temperature = 0.3 (更专注)")
        response1 = await client.generate_response(
            messages=[test_message],
            system_prompt="你是一个专业的AI助手。",
            temperature=0.3,
            max_tokens=100,
        )
        print(f"回复: {response1}")

        # Test with high temperature (more creative)
        print("\n[测试] Temperature = 0.9 (更有创意)")
        response2 = await client.generate_response(
            messages=[test_message],
            system_prompt="你是一个专业的AI助手。",
            temperature=0.9,
            max_tokens=100,
        )
        print(f"回复: {response2}")

        print("\n[SUCCESS] 参数测试完成")
        return True

    except Exception as e:
        print(f"[ERROR] 参数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_error_handling():
    """Test error handling."""
    print("\n" + "=" * 60)
    print("测试 5: 错误处理")
    print("=" * 60)

    try:
        # Test with empty messages
        print("[测试] 空消息列表...")
        client = MimoClient(
            api_key=os.getenv("MIMO_API_KEY"),
            base_url=os.getenv("MIMO_API_BASE_URL"),
            model=os.getenv("MIMO_MODEL"),
        )

        try:
            await client.generate_response(
                messages=[],
                system_prompt="Test",
            )
            print("[ERROR] 应该抛出异常但没有")
            return False
        except ValueError as e:
            print(f"[SUCCESS] 正确捕获空消息异常: {e}")

        # Test with invalid API key
        print("\n[测试] 无效的 API Key...")
        invalid_client = MimoClient(
            api_key="invalid_key_test",
            base_url=os.getenv("MIMO_API_BASE_URL"),
            model=os.getenv("MIMO_MODEL"),
            timeout=10.0,
        )

        try:
            await invalid_client.generate_response(
                messages=[{"role": "user", "content": "Hello"}],
                system_prompt="Test",
            )
            print("[WARNING] 应该抛出异常但没有")
            # Some APIs might not validate keys, so this is not necessarily an error
        except Exception as e:
            print(f"[SUCCESS] 正确捕获无效API密钥异常: {e}")

        print("\n[SUCCESS] 错误处理测试完成")
        return True

    except Exception as e:
        print(f"[ERROR] 错误处理测试失败: {e}")
        return False


async def test_performance():
    """Test API performance."""
    print("\n" + "=" * 60)
    print("测试 6: 性能测试")
    print("=" * 60)

    try:
        import time

        # Create client
        api_key = os.getenv("MIMO_API_KEY")
        base_url = os.getenv("MIMO_API_BASE_URL", "https://api.xiaomimimo.com")
        model = os.getenv("MIMO_MODEL", "mi-mimo-model")

        client = MimoClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout=30.0,
        )

        test_message = {"role": "user", "content": "写一首关于春天的短诗。"}

        times = []
        for i in range(3):
            print(f"[请求 {i+1}/3] 发送...")

            start_time = time.time()
            response = await client.generate_response(
                messages=[test_message],
                system_prompt="你是一个诗人。",
                temperature=0.8,
                max_tokens=200,
            )
            elapsed = time.time() - start_time

            times.append(elapsed)
            print(f"[请求 {i+1}/3] 完成 - 用时: {elapsed:.2f}秒")
            print(f"回复: {response[:50]}...")

        avg_time = sum(times) / len(times)
        print(f"\n[统计] 平均响应时间: {avg_time:.2f}秒")
        print(f"[统计] 最快: {min(times):.2f}秒, 最慢: {max(times):.2f}秒")

        print("\n[SUCCESS] 性能测试完成")
        return True

    except Exception as e:
        print(f"[ERROR] 性能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("XiaoMi MiMo API Test Suite")
    print("=" * 60 + "\n")

    results = {
        "基本连接": await test_basic_connection(),
        "简单对话": await test_simple_conversation(),
        "多轮对话": await test_multi_turn_conversation(),
        "参数测试": await test_different_parameters(),
        "错误处理": await test_error_handling(),
        "性能测试": await test_performance(),
    }

    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)

    for test_name, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} - {test_name}")

    all_passed = all(results.values())

    if all_passed:
        print("\n[SUCCESS] All tests passed! XiaoMi MiMo API is working!")
        print("\nYour configuration:")
        print(f"  - API URL: {os.getenv('MIMO_API_BASE_URL')}")
        print(f"  - Model: {os.getenv('MIMO_MODEL')}")
        print(f"  - API Key: {os.getenv('MIMO_API_KEY')[:20]}...")
        return 0
    else:
        print("\n[WARNING] Some tests failed, please check configuration and network")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
