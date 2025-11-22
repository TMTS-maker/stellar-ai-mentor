"""LucidAI provider stub implementation."""
from typing import List, Optional
from .base import BaseLLMClient, Message, LLMResponse


class LucidAIClient(BaseLLMClient):
    """
    LucidAI stub client.

    This is a placeholder for future LucidAI integration.
    Currently returns a mock response for testing purposes.
    """

    def __init__(self, api_key: str, default_model: str = "lucidai-v1"):
        super().__init__(api_key, default_model)
        self.provider_name = "lucidai"

    async def complete(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a stub completion.

        TODO: Replace with actual LucidAI API integration.
        """
        model = model or self.default_model

        # Stub response
        return LLMResponse(
            content="[LucidAI Stub] This is a placeholder response. LucidAI integration coming soon.",
            model=model,
            provider="lucidai",
            metadata={"stub": True}
        )

    async def stream_complete(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """Stream stub completion."""
        yield "[LucidAI Stub] Streaming response. "
        yield "Integration coming soon."
