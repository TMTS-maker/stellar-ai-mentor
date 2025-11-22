"""
Stellecta LucidAI Backend - Google Gemini Provider

Active provider for Phase 0.

Uses Google's Gemini API (gemini-2.5-flash by default).
"""

import google.generativeai as genai
import time
from typing import Optional

from app.llm.base import BaseLLMClient, LLMProviderError, LLMUnavailableError
from app.llm.schemas import LLMRequest, LLMResponse
from app.config import settings


class GeminiProvider(BaseLLMClient):
    """
    Google Gemini LLM Provider.

    Default LLM for Phase 0 (before LucidAI is production-ready).

    Model: gemini-2.5-flash (fast, cost-effective)
    Fallback: gemini-pro
    """

    def __init__(self, model_name: Optional[str] = None):
        super().__init__(model_name or settings.gemini_model)

        # Configure Gemini API
        genai.configure(api_key=settings.gemini_api_key)

        self._model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize Gemini model instance."""
        try:
            self._model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={
                    "max_output_tokens": settings.gemini_max_tokens,
                }
            )
        except Exception as e:
            raise LLMProviderError(f"Failed to initialize Gemini model: {e}")

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate response from Gemini.

        Args:
            request: LLM request with prompts and configuration

        Returns:
            LLMResponse: Gemini response

        Raises:
            LLMProviderError: If generation fails
            LLMUnavailableError: If API is unavailable
        """

        if not await self.is_available():
            raise LLMUnavailableError("Gemini API key is not configured.")

        start_time = time.time()

        try:
            # Build conversation context
            conversation_context = self._build_context(request)

            # Generate response
            # Note: Gemini SDK is synchronous, but we wrap it for consistency
            response = self._model.generate_content(
                conversation_context,
                generation_config=genai.GenerationConfig(
                    temperature=request.temperature,
                    max_output_tokens=request.max_tokens,
                )
            )

            inference_time_ms = int((time.time() - start_time) * 1000)

            # Extract response text
            response_text = response.text if response.text else ""

            # Estimate tokens (Gemini API doesn't always return token counts)
            tokens_input = self._estimate_tokens(conversation_context)
            tokens_output = self._estimate_tokens(response_text)

            # Estimate cost (approximate, based on Gemini pricing)
            cost_usd = self._estimate_cost(tokens_input, tokens_output)

            llm_response = LLMResponse(
                content=response_text,
                llm_provider="gemini",
                model_version=self.model_name,
                confidence_score=None,  # Gemini doesn't provide confidence
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                inference_time_ms=inference_time_ms,
                cost_usd=cost_usd,
                metadata={
                    "finish_reason": response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN",
                    "safety_ratings": [
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name
                        }
                        for rating in response.candidates[0].safety_ratings
                    ] if response.candidates else []
                }
            )

            self._record_metrics(llm_response)
            return llm_response

        except Exception as e:
            raise LLMProviderError(f"Gemini generation failed: {e}")

    def _build_context(self, request: LLMRequest) -> str:
        """
        Build conversation context for Gemini.

        Gemini doesn't have a separate system prompt in the same way as OpenAI,
        so we prepend it to the conversation.
        """

        context_parts = []

        # Add system prompt
        if request.system_prompt:
            context_parts.append(f"System Instructions:\n{request.system_prompt}\n")

        # Add conversation history
        if request.conversation_history:
            context_parts.append("Previous Conversation:")
            for msg in request.conversation_history:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                context_parts.append(f"{role.capitalize()}: {content}")
            context_parts.append("")

        # Add current user message
        context_parts.append(f"User: {request.user_message}")
        context_parts.append("Assistant:")

        return "\n".join(context_parts)

    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count.

        Rough estimate: ~4 characters per token.
        """
        return max(1, len(text) // 4)

    def _estimate_cost(self, tokens_input: int, tokens_output: int) -> float:
        """
        Estimate cost in USD.

        Gemini pricing (approximate, as of 2024):
        - Input: $0.00025 / 1K tokens
        - Output: $0.0005 / 1K tokens
        """

        input_cost = (tokens_input / 1000) * 0.00025
        output_cost = (tokens_output / 1000) * 0.0005

        return input_cost + output_cost

    def get_provider_name(self) -> str:
        """Get provider name."""
        return "gemini"

    async def is_available(self) -> bool:
        """
        Check if Gemini is configured and reachable.

        Returns:
            bool: True if API key is configured
        """

        # Check if API key is not placeholder
        if settings.gemini_api_key == "__GEMINI_API_KEY__":
            return False

        # Basic check: API key exists
        if not settings.gemini_api_key:
            return False

        # TODO: Optionally add a ping/health check to Gemini API
        # For now, just check configuration

        return True
