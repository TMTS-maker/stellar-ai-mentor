"""
Multi-LLM Router - Central orchestration for vendor-agnostic LLM access.
"""
from typing import Optional, Dict
from .providers.base import BaseLLMClient, Message, LLMResponse
from .providers.openai import OpenAIClient
from .providers.anthropic import AnthropicClient
from .providers.gemini import GeminiClient
from .providers.lucidai import LucidAIClient
from ..config import settings


class LLMRouter:
    """
    Routes LLM requests to the appropriate provider.

    Supports: OpenAI, Anthropic, Google Gemini, LucidAI (stub).
    """

    def __init__(self):
        self.providers: Dict[str, BaseLLMClient] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all available LLM providers based on configuration."""
        if settings.openai_api_key:
            self.providers["openai"] = OpenAIClient(
                api_key=settings.openai_api_key,
                default_model="gpt-4-turbo-preview"
            )

        if settings.anthropic_api_key:
            self.providers["anthropic"] = AnthropicClient(
                api_key=settings.anthropic_api_key,
                default_model="claude-3-5-sonnet-20241022"
            )

        if settings.google_api_key:
            self.providers["gemini"] = GeminiClient(
                api_key=settings.google_api_key,
                default_model="gemini-1.5-pro"
            )

        if settings.lucidai_api_key:
            self.providers["lucidai"] = LucidAIClient(
                api_key=settings.lucidai_api_key,
                default_model="lucidai-v1"
            )

    def get_provider(self, provider_name: Optional[str] = None) -> BaseLLMClient:
        """
        Get a specific LLM provider client.

        Args:
            provider_name: Name of provider ("openai", "anthropic", "gemini", "lucidai")
                          If None, uses default from settings

        Returns:
            BaseLLMClient instance

        Raises:
            ValueError: If provider not found or not configured
        """
        provider = provider_name or settings.default_llm_provider

        if provider not in self.providers:
            available = ", ".join(self.providers.keys())
            raise ValueError(
                f"Provider '{provider}' not available. "
                f"Available providers: {available}. "
                f"Check API keys in .env file."
            )

        return self.providers[provider]

    async def complete(
        self,
        messages: list,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a completion using the specified provider.

        Args:
            messages: List of Message objects or dicts
            provider: Provider name (uses default if None)
            model: Model name (uses provider default if None)
            temperature: Sampling temperature
            max_tokens: Max tokens to generate
            **kwargs: Provider-specific parameters

        Returns:
            LLMResponse with generated content
        """
        client = self.get_provider(provider)

        # Convert dict messages to Message objects if needed
        message_objects = []
        for msg in messages:
            if isinstance(msg, dict):
                message_objects.append(Message(**msg))
            else:
                message_objects.append(msg)

        return await client.complete(
            messages=message_objects,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    async def stream_complete(
        self,
        messages: list,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        Stream a completion using the specified provider.

        Yields chunks of text as they're generated.
        """
        client = self.get_provider(provider)

        # Convert dict messages to Message objects if needed
        message_objects = []
        for msg in messages:
            if isinstance(msg, dict):
                message_objects.append(Message(**msg))
            else:
                message_objects.append(msg)

        async for chunk in client.stream_complete(
            messages=message_objects,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        ):
            yield chunk


# Global router instance
_llm_router: Optional[LLMRouter] = None


def get_llm_router() -> LLMRouter:
    """
    Get the global LLM router instance (singleton pattern).

    Returns:
        LLMRouter instance
    """
    global _llm_router
    if _llm_router is None:
        _llm_router = LLMRouter()
    return _llm_router
