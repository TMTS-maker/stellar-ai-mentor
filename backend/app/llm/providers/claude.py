"""
Stellecta LucidAI Backend - Anthropic Claude Provider

Claude 3.5 Sonnet integration.
"""

from anthropic import AsyncAnthropic
import time
from typing import Optional

from app.llm.base import BaseLLMClient, LLMProviderError, LLMUnavailableError
from app.llm.schemas import LLMRequest, LLMResponse
from app.config import settings


class ClaudeProvider(BaseLLMClient):
    """
    Anthropic Claude LLM Provider.

    Supports: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku
    """

    def __init__(self, model_name: Optional[str] = None):
        super().__init__(model_name or settings.anthropic_model)

        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response from Claude."""

        if not await self.is_available():
            raise LLMUnavailableError("Anthropic API key is not configured.")

        start_time = time.time()

        try:
            # Build messages
            messages = self._build_messages(request)

            # Call Claude API
            response = await self.client.messages.create(
                model=self.model_name,
                system=request.system_prompt,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            inference_time_ms = int((time.time() - start_time) * 1000)

            # Extract response
            response_text = response.content[0].text if response.content else ""

            # Get token counts
            tokens_input = response.usage.input_tokens if response.usage else 0
            tokens_output = response.usage.output_tokens if response.usage else 0

            # Calculate cost
            cost_usd = self._calculate_cost(tokens_input, tokens_output)

            llm_response = LLMResponse(
                content=response_text,
                llm_provider="claude",
                model_version=self.model_name,
                confidence_score=None,  # Claude doesn't provide confidence
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                inference_time_ms=inference_time_ms,
                cost_usd=cost_usd,
                metadata={
                    "stop_reason": response.stop_reason,
                }
            )

            self._record_metrics(llm_response)
            return llm_response

        except Exception as e:
            raise LLMProviderError(f"Claude generation failed: {e}")

    def _build_messages(self, request: LLMRequest) -> list:
        """Build Claude messages format."""

        messages = []

        # Conversation history
        for msg in request.conversation_history:
            messages.append(msg)

        # Current user message
        messages.append({"role": "user", "content": request.user_message})

        return messages

    def _calculate_cost(self, tokens_input: int, tokens_output: int) -> float:
        """
        Calculate cost based on Claude pricing.

        Claude 3.5 Sonnet (approximate):
        - Input: $0.003 / 1K tokens
        - Output: $0.015 / 1K tokens
        """

        input_cost = (tokens_input / 1000) * 0.003
        output_cost = (tokens_output / 1000) * 0.015

        return input_cost + output_cost

    def get_provider_name(self) -> str:
        return "claude"

    async def is_available(self) -> bool:
        """Check if Claude is configured."""

        if settings.anthropic_api_key == "__ANTHROPIC_API_KEY__":
            return False

        return bool(settings.anthropic_api_key)
