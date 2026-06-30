"""
AgenticMarketingPro — Minimax API Client
========================================
OpenAI-compatible API client for Minimax M3 (MiniMax-Text-01) model.
Supports chat completions, streaming, and cost tracking.

Usage:
    from api_client.minimax import MinimaxClient
    client = MinimaxClient()
    response = client.chat(
        model="MiniMax-Text-01",
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.7,
    )
"""

import json
import logging
from typing import List, Dict, Optional, Iterator, Any
import httpx

from config import Config

logger = logging.getLogger("amp.minimax")


class MinimaxClient:
    """Minimax API client (OpenAI-compatible)."""

    BASE_URL = "https://api.minimaxi.chat/v1"
    DEFAULT_MODEL = "MiniMax-Text-01"
    TIMEOUT = 120.0

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or Config.MINIMAX_API_KEY
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.model = Config.DEFAULT_LLM_MODEL if hasattr(Config, "DEFAULT_LLM_MODEL") else self.DEFAULT_MODEL

        if not self.api_key:
            raise ValueError("Minimax API key not configured. Set MINIMAX_API_KEY in .env")

        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=self.TIMEOUT,
        )

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,
        top_p: float = 0.95,
        stream: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a chat completion request.

        Args:
            messages: List of {"role": "system"|"user"|"assistant", "content": "..."}
            model: Model name (default: MiniMax-Text-01)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            stream: Whether to stream the response
            tools: Optional function calling tools
            tool_choice: Optional tool choice strategy

        Returns:
            API response dict with "choices", "usage", etc.
        """
        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if tools:
            payload["tools"] = tools
        if tool_choice:
            payload["tool_choice"] = tool_choice

        try:
            response = self._client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Minimax API error: {e.response.status_code} - {e.response.text}")
            raise MinimaxAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Minimax request failed: {e}")
            raise MinimaxAPIError(f"Request failed: {e}")

    def chat_simple(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,
    ) -> str:
        """
        Simple chat with system + user message. Returns just the assistant content.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = self.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected response format: {response}")
            raise MinimaxAPIError(f"Invalid response format: {e}")

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,
    ) -> Iterator[str]:
        """
        Stream chat response as text chunks.
        """
        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        try:
            with self._client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload,
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"]
                            if "content" in delta:
                                yield delta["content"]
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
        except httpx.HTTPStatusError as e:
            logger.error(f"Minimax streaming error: {e.response.status_code}")
            raise MinimaxAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Minimax stream request failed: {e}")
            raise MinimaxAPIError(f"Request failed: {e}")

    def count_tokens(self, text: str) -> int:
        """
        Rough token count (Chinese chars ~1 token, English words ~1.3 tokens).
        Minimax doesn't provide a tokenizer, so we estimate.
        """
        import re
        # Chinese characters
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        # English words and other characters
        rest = len(re.sub(r'[\u4e00-\u9fff]', '', text))
        english_words = len(text.split()) if rest > 0 else 0
        # Rough estimate: Chinese chars + English words * 1.3
        return chinese_chars + int(english_words * 1.3)

    def health_check(self) -> Dict[str, Any]:
        """Check Minimax API connectivity."""
        try:
            start = __import__("time").time()
            response = self._client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "Hi"}],
                    "max_tokens": 1,
                },
                timeout=15.0,
            )
            latency = round((__import__("time").time() - start) * 1000, 2)
            if response.status_code == 200:
                return {
                    "name": "minimax",
                    "status": "healthy",
                    "latency_ms": latency,
                    "model": self.model,
                    "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
                }
            else:
                return {
                    "name": "minimax",
                    "status": "error",
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
                }
        except Exception as e:
            return {
                "name": "minimax",
                "status": "error",
                "error": str(e),
                "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            }

    def close(self):
        """Close the HTTP client."""
        self._client.close()


class MinimaxAPIError(Exception):
    """Raised when Minimax API returns an error."""
    pass


# ── Convenience function for skill execution ──────────────────────────

def generate_with_minimax(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    model: str = "MiniMax-Text-01",
) -> Dict[str, Any]:
    """
    One-shot generation with Minimax. Returns dict with content, tokens, cost.
    """
    client = MinimaxClient()
    try:
        response = client.chat_simple(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Estimate tokens
        tokens_in = client.count_tokens(system_prompt + user_prompt)
        tokens_out = client.count_tokens(response)

        return {
            "content": response,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "model": model,
            "provider": "minimax",
        }
    finally:
        client.close()


if __name__ == "__main__":
    # Test
    import logging
    logging.basicConfig(level=logging.INFO)

    client = MinimaxClient()
    print("Health check:", client.health_check())

    result = client.chat_simple(
        system_prompt="You are a helpful marketing assistant.",
        user_prompt="Write a 50-word product description for a cloud security SaaS.",
    )
    print("Response:", result)
    client.close()
