"""
Stellecta LucidAI Backend - OpenAI Provider

OpenAI GPT-4 / GPT-3.5 integration.
"""

from openai import AsyncOpenAI
import time
from typing import Optional

from app.llm.base import BaseLLMClient, LLMProviderError, LLMUnavailableError
from app.llm.schemas import LLMRequest, LLMResponse
from app.config import settings


class OpenAIProvider(BaseLLMClient):
    """
    OpenAI LLM Provider.

    Supports: GPT-4, GPT-3.5-Turbo, GPT-4-Turbo
    """

    def __init__(self, model_name: Optional[str] = None):
        super().__init__(model_name or settings.openai_model)

        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response from OpenAI."""

        if not await self.is_available():
            raise LLMUnavailableError("OpenAI API key is not configured.")

        start_time = time.time()

        try:
            # Build messages
            messages = self._build_messages(request)

            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            inference_time_ms = int((time.time() - start_time) * 1000)

            # Extract response
            choice = response.choices[0]
            response_text = choice.message.content or ""

            # Get token counts
            tokens_input = response.usage.prompt_tokens if response.usage else 0
            tokens_output = response.usage.completion_tokens if response.usage else 0

            # Calculate cost
            cost_usd = self._calculate_cost(tokens_input, tokens_output)

            llm_response = LLMResponse(
                content=response_text,
                llm_provider="openai",
                model_version=self.model_name,
                confidence_score=None,  # OpenAI doesn't provide confidence
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                inference_time_ms=inference_time_ms,
                cost_usd=cost_usd,
                metadata={
                    "finish_reason": choice.finish_reason,
                }
            )

            self._record_metrics(llm_response)
            return llm_response

        except Exception as e:
            raise LLMProviderError(f"OpenAI generation failed: {e}")

    def _build_messages(self, request: LLMRequest) -> list:
        """Build OpenAI messages format."""

        messages = []

        # System prompt
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})

        # Conversation history
        for msg in request.conversation_history:
            messages.append(msg)

        # Current user message
        messages.append({"role": "user", "content": request.user_message})

        return messages

    def _calculate_cost(self, tokens_input: int, tokens_output: int) -> float:
        """
        Calculate cost based on OpenAI pricing.

        GPT-4 Turbo (approximate):
        - Input: $0.01 / 1K tokens
        - Output: $0.03 / 1K tokens
        """

        input_cost = (tokens_input / 1000) * 0.01
        output_cost = (tokens_output / 1000) * 0.03

        return input_cost + output_cost

    def get_provider_name(self) -> str:
        return "openai"

    async def is_available(self) -> bool:
        """Check if OpenAI is configured."""

        if settings.openai_api_key == "__OPENAI_API_KEY__":
            return False

        return bool(settings.openai_api_key)
