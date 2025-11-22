"""Anthropic Claude provider implementation."""
from typing import List, Optional
from anthropic import AsyncAnthropic
from .base import BaseLLMClient, Message, LLMResponse


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude LLM client implementation."""

    def __init__(self, api_key: str, default_model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(api_key, default_model)
        self.client = AsyncAnthropic(api_key=api_key)

    async def complete(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Anthropic API."""
        model = model or self.default_model

        # Extract system message if present
        system_message = None
        user_messages = []
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                user_messages.append({"role": msg.role, "content": msg.content})

        response = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message,
            messages=user_messages,
            **kwargs
        )

        return LLMResponse(
            content=response.content[0].text,
            model=response.model,
            provider="anthropic",
            usage={
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
            metadata={"stop_reason": response.stop_reason}
        )

    async def stream_complete(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,
        **kwargs
    ):
        """Stream completion from Anthropic."""
        model = model or self.default_model

        # Extract system message
        system_message = None
        user_messages = []
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                user_messages.append({"role": msg.role, "content": msg.content})

        async with self.client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message,
            messages=user_messages,
            **kwargs
        ) as stream:
            async for text in stream.text_stream:
                yield text
