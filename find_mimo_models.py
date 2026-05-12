"""Find correct model names for XiaoMi MiMo API."""

import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv()


async def find_correct_model():
    """Find the correct model name for MiMo API."""
    print("=" * 60)
    print("MiMo API - Finding Correct Model Name")
    print("=" * 60)

    api_key = os.getenv("MIMO_API_KEY")
    base_url = os.getenv("MIMO_API_BASE_URL", "https://api.xiaomimimo.com")
    proxy_url = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")

    # Common model names to try
    model_names = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "claude-3-5-sonnet-20240620",
        "claude-3-5-haiku-20241022",
        "mimo",
        "mimo-pro",
        "mimo-turbo",
        "xiaomimimo",
        "mi-mimo-pro",
        "mi-mimo-turbo",
        "qwen-turbo",
        "qwen-plus",
        "qwen-max",
    ]

    url = f"{base_url}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ],
        "temperature": 0.7,
        "max_tokens": 10,
    }

    print("\n[Testing] Different model names...\n")

    working_models = []

    for model_name in model_names:
        data["model"] = model_name

        try:
            async with httpx.AsyncClient(proxy=proxy_url, timeout=30.0) as client:
                response = await client.post(url, json=data, headers=headers)

                if response.status_code == 200:
                    print(f"[SUCCESS] {model_name:30} - Working!")
                    working_models.append(model_name)
                elif response.status_code == 400:
                    error = response.json()
                    error_msg = error.get("error", {}).get("message", "Unknown error")
                    if "Not supported model" in error_msg:
                        print(f"[FAIL]    {model_name:30} - Model not supported")
                    else:
                        print(f"[ERROR]   {model_name:30} - {error_msg}")
                else:
                    print(f"[ERROR]   {model_name:30} - Status {response.status_code}")

        except Exception as e:
            print(f"[ERROR]   {model_name:30} - {e}")

    print(f"\n{'=' * 60}")
    print("Results Summary")
    print(f"{'=' * 60}")

    if working_models:
        print(f"\n[SUCCESS] Found {len(working_models)} working model(s):")
        for model in working_models:
            print(f"  - {model}")

        # Test the first working model with a real conversation
        print(f"\n[Testing] Real conversation with {working_models[0]}...")

        data = {
            "model": working_models[0],
            "messages": [
                {"role": "system", "content": "你是一个友好的AI助手。"},
                {"role": "user", "content": "你好，请用一句话介绍你自己。"}
            ],
            "temperature": 0.7,
            "max_tokens": 100,
        }

        try:
            async with httpx.AsyncClient(proxy=proxy_url, timeout=30.0) as client:
                response = await client.post(url, json=data, headers=headers)

                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"\n[Response] {content}")
                    print(f"\n[SUCCESS] MiMo API is working correctly!")
                    print(f"\nPlease update your .env file:")
                    print(f"  MIMO_MODEL={working_models[0]}")
                    return True
        except Exception as e:
            print(f"[ERROR] Conversation test failed: {e}")
    else:
        print("\n[ERROR] No working models found!")
        print("\nPossible issues:")
        print("1. Your API key might not have access to these models")
        print("2. The model names might be different")
        print("3. Check the MiMo API documentation for available models")
        print("\nSuggestion:")
        print("Please check the XiaoMi MiMo API documentation or contact")
        print("their support to get the correct model name for your API key.")

    return False


if __name__ == "__main__":
    success = asyncio.run(find_correct_model())
    exit(0 if success else 1)
