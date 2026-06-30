"""
AgenticMarketingPro — Minimax API Client
========================================
Anthropic-compatible API client for Minimax M3 (MiniMax-M3) model.
Uses the Anthropic Messages API format via Minimax's Anthropic compatibility layer.

Usage:
    from api_client.minimax import MinimaxClient
    client = MinimaxClient()
    response = client.chat(
        model="MiniMax-M3",
        system="You are a marketing expert.",
        messages=[{"role": "user", "content": "Write a blog post about SEO."}],
        max_tokens=2000,
    )
    print(response.content)

Setup:
    pip install anthropic
    MINIMAX_API_KEY=sk-...  (in .env)

Docs: https://platform.minimax.io/docs/api-reference/text-anthropic-api
"""

import json
import logging
from typing import List, Dict, Optional, Iterator, Any
from dataclasses import dataclass

from config import Config

logger = logging.getLogger("amp.minimax")


@dataclass
class ChatResponse:
    """Unified chat response from Minimax M3."""
    content: str
    reasoning: Optional[str] = None
    tokens_in: int = 0
    tokens_out: int = 0
    model: str = ""
    finish_reason: Optional[str] = None


class MinimaxClient:
    """Minimax API client via Anthropic SDK compatibility layer."""

    BASE_URL = "https://api.minimax.io/anthropic"
    DEFAULT_MODEL = "MiniMax-M3"
    TIMEOUT = 120.0

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or Config.MINIMAX_API_KEY
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.model = model or Config.DEFAULT_LLM_MODEL if hasattr(Config, "DEFAULT_LLM_MODEL") else self.DEFAULT_MODEL

        if not self.api_key:
            raise ValueError("Minimax API key not configured. Set MINIMAX_API_KEY in .env")

        # Initialize Anthropic SDK with Minimax base URL
        try:
            from anthropic import Anthropic
            self._client = Anthropic(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.TIMEOUT,
            )
            logger.info(f"Minimax client initialized (model: {self.model})")
        except ImportError:
            logger.error("anthropic SDK not installed. Run: pip install anthropic")
            raise

    def chat(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = 4096,
        top_p: float = 0.95,
        thinking: Optional[Dict[str, str]] = None,
        stream: bool = False,
    ) -> ChatResponse:
        """
        Send a chat completion request using Anthropic Messages API format.

        Args:
            messages: List of {"role": "user"|"assistant", "content": "..."}
            system: System prompt
            model: Model name (default: MiniMax-M3)
            temperature: Sampling temperature [0, 2], recommended: 1.0
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling [0, 1]
            thinking: {"type": "adaptive"} to enable reasoning for M3
            stream: Whether to stream response

        Returns:
            ChatResponse with content, tokens, reasoning
        """
        # Convert messages to Anthropic format (content blocks)
        anthropic_messages = []
        for msg in messages:
            content = msg.get("content", "")
            anthropic_messages.append({
                "role": msg["role"],
                "content": [{"type": "text", "text": content}],
            })

        params = {
            "model": model or self.model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens or 4096,
            "temperature": temperature,
            "top_p": top_p,
        }

        if system:
            params["system"] = system

        if thinking:
            params["thinking"] = thinking

        try:
            if stream:
                return self._stream_chat(params)
            else:
                return self._sync_chat(params)
        except Exception as e:
            logger.error(f"Minimax chat error: {e}")
            raise MinimaxAPIError(str(e))

    def _sync_chat(self, params: Dict) -> ChatResponse:
        """Synchronous chat request."""
        response = self._client.messages.create(**params)

        # Extract text content
        text_content = ""
        reasoning = ""
        for block in response.content:
            if block.type == "text":
                text_content += block.text
            elif block.type == "thinking":
                reasoning += block.thinking

        return ChatResponse(
            content=text_content,
            reasoning=reasoning if reasoning else None,
            tokens_in=response.usage.input_tokens if hasattr(response, "usage") else 0,
            tokens_out=response.usage.output_tokens if hasattr(response, "usage") else 0,
            model=response.model,
            finish_reason=response.stop_reason if hasattr(response, "stop_reason") else None,
        )

    def _stream_chat(self, params: Dict) -> ChatResponse:
        """Stream chat and collect full response."""
        text_buffer = ""
        reasoning_buffer = ""

        with self._client.messages.create(**params, stream=True) as stream:
            for chunk in stream:
                if chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, "text") and chunk.delta.text:
                        text_buffer += chunk.delta.text
                    elif hasattr(chunk.delta, "thinking") and chunk.delta.thinking:
                        reasoning_buffer += chunk.delta.thinking

        return ChatResponse(
            content=text_buffer,
            reasoning=reasoning_buffer if reasoning_buffer else None,
            tokens_in=0,  # Usage not available in stream mode
            tokens_out=0,
            model=params["model"],
        )

    def chat_simple(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = 4096,
        thinking: bool = False,
    ) -> str:
        """
        Simple chat with system + user message. Returns just the assistant text.
        """
        messages = [{"role": "user", "content": user_prompt}]
        thinking_cfg = {"type": "adaptive"} if thinking else None

        response = self.chat(
            messages=messages,
            system=system_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            thinking=thinking_cfg,
        )
        return response.content

    def chat_with_reasoning(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = 4096,
    ) -> ChatResponse:
        """
        Chat with reasoning enabled. Returns full response with reasoning.
        """
        messages = [{"role": "user", "content": user_prompt}]

        return self.chat(
            messages=messages,
            system=system_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
        )

    def count_tokens(self, text: str) -> int:
        """
        Rough token count. For exact count, use Minimax's token count endpoint.
        """
        import re
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        rest = len(re.sub(r'[\u4e00-\u9fff]', '', text))
        english_words = len(text.split()) if rest > 0 else 0
        return chinese_chars + int(english_words * 1.3)

    def health_check(self) -> Dict[str, Any]:
        """Check Minimax API connectivity."""
        try:
            import time
            start = time.time()

            response = self._client.messages.create(
                model=self.model,
                max_tokens=1,
                messages=[{"role": "user", "content": [{"type": "text", "text": "Hi"}]}],
                timeout=15.0,
            )
            latency = round((time.time() - start) * 1000, 2)

            return {
                "name": "minimax",
                "status": "healthy",
                "latency_ms": latency,
                "model": self.model,
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
        """Close the Anthropic client."""
        # Anthropic client doesn't need explicit close
        pass


class MinimaxAPIError(Exception):
    """Raised when Minimax API returns an error."""
    pass


# ── Convenience function for skill execution ──────────────────────────

def generate_with_minimax(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 1.0,
    max_tokens: int = 4096,
    model: str = "MiniMax-M3",
    thinking: bool = False,
) -> Dict[str, Any]:
    """
    One-shot generation with Minimax M3. Returns dict with content, tokens, cost.
    """
    client = MinimaxClient()
    try:
        if thinking:
            response = client.chat_with_reasoning(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            response = client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system=system_prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        # Estimate tokens if not available
        tokens_in = response.tokens_in or client.count_tokens(system_prompt + user_prompt)
        tokens_out = response.tokens_out or client.count_tokens(response.content)

        return {
            "content": response.content,
            "reasoning": response.reasoning,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "model": model,
            "provider": "minimax",
        }
    finally:
        client.close()


def generate_with_openai(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    One-shot generation with OpenAI. Returns dict with content, tokens, cost.
    """
    from openai import OpenAI
    from config import Config
    import tiktoken

    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content

        # Count tokens using tiktoken
        try:
            encoding = tiktoken.encoding_for_model(model)
            tokens_in = len(encoding.encode(system_prompt + user_prompt))
            tokens_out = len(encoding.encode(content))
        except KeyError:
            # Fallback for unknown models
            tokens_in = len((system_prompt + user_prompt).split()) * 1.3
            tokens_out = len(content.split()) * 1.3

        return {
            "content": content,
            "tokens_in": int(tokens_in),
            "tokens_out": int(tokens_out),
            "model": model,
            "provider": "openai",
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
