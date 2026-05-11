"""XiaoMi MiMo API client for LLM integration."""

import asyncio
from typing import List, Dict, Optional
import httpx


class MimoClient:
    """Client for XiaoMi MiMo API (OpenAI-compatible).

    Attributes:
        api_key: API key for authentication
        base_url: Base URL for API endpoint
        model: Model name to use
        timeout: Request timeout in seconds
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.xiaomimimo.com",
        model: str = "mi-mimo-model",
        timeout: float = 30.0,
    ) -> None:
        """Initialize Mimo client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for API endpoint
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        max_retries: int = 3,
    ) -> str:
        """Generate chat response using Mimo API.

        Args:
            messages: List of conversation messages
            system_prompt: System prompt for the model
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            max_retries: Maximum number of retries on failure

        Returns:
            Generated response text

        Raises:
            ValueError: If messages list is empty
            Exception: If API request fails after retries
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Prepare messages with system prompt
        all_messages = [{"role": "system", "content": system_prompt}] + messages

        data = {
            "model": self.model,
            "messages": all_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        last_error = None
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, json=data, headers=headers)

                    if response.status_code == 200:
                        result = response.json()
                        content = result["choices"][0]["message"]["content"]
                        return content
                    else:
                        error_info = response.json()
                        last_error = Exception(
                            f"API request failed: {error_info.get('error', {}).get('message', 'Unknown error')}"
                        )

            except Exception as e:
                last_error = e

            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        raise Exception(f"Failed to generate response after {max_retries} attempts: {last_error}")

    async def generate_response_stream(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Generate streaming chat response.

        Args:
            messages: List of conversation messages
            system_prompt: System prompt for the model
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Raises:
            NotImplementedError: Streaming not currently supported
        """
        raise NotImplementedError("Streaming not currently supported")
