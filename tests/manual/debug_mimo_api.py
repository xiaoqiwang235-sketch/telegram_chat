"""Debug script for XiaoMi MiMo API."""

import asyncio
import os
import sys
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()


async def debug_mimo_api():
    """Debug MiMo API connection."""
    print("=" * 60)
    print("MiMo API Debug Tool")
    print("=" * 60)

    # Get configuration
    api_key = os.getenv("MIMO_API_KEY")
    base_url = os.getenv("MIMO_API_BASE_URL", "https://api.xiaomimimo.com")
    model = os.getenv("MIMO_MODEL", "mi-mimo-model")

    print(f"\n[Configuration]")
    print(f"API Key: {api_key[:20]}...")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")

    # Test different endpoints
    endpoints = [
        "/v1/chat",
        "/chat/completions",
        "/v1/chat/completions",
        "/api/v1/chat",
    ]

    for endpoint in endpoints:
        print(f"\n{'=' * 60}")
        print(f"[Testing] Endpoint: {endpoint}")
        print(f"{'=' * 60}")

        url = f"{base_url}{endpoint}"
        print(f"Full URL: {url}")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, please respond with 'OK' if you receive this."}
            ],
            "temperature": 0.7,
            "max_tokens": 50,
        }

        try:
            # Test without proxy first
            print("\n[Attempt 1] Direct connection (no proxy)")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=data, headers=headers)
                print(f"Status Code: {response.status_code}")
                print(f"Headers: {dict(response.headers)}")
                print(f"Response Body: {response.text[:500]}")

                if response.status_code == 200:
                    try:
                        result = response.json()
                        print(f"[SUCCESS] JSON Response received!")
                        if "choices" in result and len(result["choices"]) > 0:
                            content = result["choices"][0]["message"]["content"]
                            print(f"Content: {content}")
                            return True
                    except Exception as e:
                        print(f"[ERROR] JSON parsing failed: {e}")

        except Exception as e:
            print(f"[ERROR] Direct connection failed: {e}")

        # Try with proxy
        proxy_url = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
        if proxy_url:
            print(f"\n[Attempt 2] With proxy: {proxy_url}")
            try:
                async with httpx.AsyncClient(proxy=proxy_url, timeout=30.0) as client:
                    response = await client.post(url, json=data, headers=headers)
                    print(f"Status Code: {response.status_code}")
                    print(f"Response Body: {response.text[:500]}")

                    if response.status_code == 200:
                        try:
                            result = response.json()
                            print(f"[SUCCESS] JSON Response received via proxy!")
                            if "choices" in result and len(result["choices"]) > 0:
                                content = result["choices"][0]["message"]["content"]
                                print(f"Content: {content}")
                                return True
                        except Exception as e:
                            print(f"[ERROR] JSON parsing failed: {e}")

            except Exception as e:
                print(f"[ERROR] Proxy connection failed: {e}")

    # Test basic connectivity to the base URL
    print(f"\n{'=' * 60}")
    print("[Testing] Basic connectivity to base URL")
    print(f"{'=' * 60}")

    try:
        proxy_url = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
        async with httpx.AsyncClient(proxy=proxy_url, timeout=10.0) as client:
            response = await client.get(base_url)
            print(f"GET {base_url}")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"[ERROR] Base URL connection failed: {e}")

    print(f"\n{'=' * 60}")
    print("[Debug] Common Issues and Solutions")
    print(f"{'=' * 60}")
    print("""
1. Wrong Endpoint URL:
   - Check the API documentation for the correct endpoint
   - Common patterns: /v1/chat/completions, /chat/completions

2. Authentication Issues:
   - Verify your API key is correct
   - Check if the key format is Bearer <token>

3. Network Issues:
   - Try with proxy if you're in China
   - Check if the API server is accessible

4. Model Name Issues:
   - Verify the model name is correct
   - Check if the model is available

5. Request Format:
   - The API might expect different request format
   - Check the API documentation for expected JSON structure
    """)

    return False


if __name__ == "__main__":
    success = asyncio.run(debug_mimo_api())
    sys.exit(0 if success else 1)
