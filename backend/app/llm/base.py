"""
Stellecta LucidAI Backend - BaseLLMClient

Abstract base class for all LLM providers.

CRITICAL: This is the vendor-agnostic abstraction that enables the Multi-LLM
architecture. All LLM providers (LucidAI, Gemini, OpenAI, Claude, etc.) must
implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Optional
import time

from app.llm.schemas import LLMRequest, LLMResponse


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM providers.

    All concrete LLM providers must implement:
    - generate(): Generate a response from the LLM
    - get_provider_name(): Return the provider identifier
    - is_available(): Check if the provider is configured and reachable

    This abstraction ensures:
    - Vendor independence (easy to swap/add providers)
    - Consistent interface across all LLMs
    - Testability (mock implementations)
    """

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize LLM client.

        Args:
            model_name: Specific model to use (e.g., "gpt-4-turbo-preview")
                       If None, uses provider's default model.
        """
        self.model_name = model_name
        self._metrics = {
            "total_requests": 0,
            "total_tokens_input": 0,
            "total_tokens_output": 0,
            "total_cost_usd": 0.0,
            "total_inference_time_ms": 0,
        }

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a response from the LLM.

        This is the core method that all providers must implement.

        Args:
            request: Standardized LLM request

        Returns:
            LLMResponse: Standardized LLM response

        Raises:
            LLMProviderError: If the LLM request fails
            LLMUnavailableError: If the LLM is unavailable
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the provider identifier.

        Returns:
            str: Provider name (e.g., "lucidai", "gemini", "openai")
        """
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """
        Check if the LLM provider is configured and reachable.

        Returns:
            bool: True if provider is available, False otherwise
        """
        pass

    def _record_metrics(self, response: LLMResponse):
        """
        Record metrics for monitoring and cost tracking.

        Args:
            response: LLM response with metrics
        """
        self._metrics["total_requests"] += 1

        if response.tokens_input:
            self._metrics["total_tokens_input"] += response.tokens_input

        if response.tokens_output:
            self._metrics["total_tokens_output"] += response.tokens_output

        if response.cost_usd:
            self._metrics["total_cost_usd"] += response.cost_usd

        if response.inference_time_ms:
            self._metrics["total_inference_time_ms"] += response.inference_time_ms

    def get_metrics(self) -> dict:
        """
        Get accumulated metrics for this provider.

        Returns:
            dict: Metrics dictionary
        """
        return self._metrics.copy()

    def reset_metrics(self):
        """Reset accumulated metrics."""
        self._metrics = {
            "total_requests": 0,
            "total_tokens_input": 0,
            "total_tokens_output": 0,
            "total_cost_usd": 0.0,
            "total_inference_time_ms": 0,
        }


# ============================================================================
# EXCEPTIONS
# ============================================================================

class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass


class LLMProviderError(LLMError):
    """LLM provider encountered an error during generation."""
    pass


class LLMUnavailableError(LLMError):
    """LLM provider is not configured or unreachable."""
    pass


class LLMRateLimitError(LLMError):
    """LLM provider rate limit exceeded."""
    pass


class LLMTimeoutError(LLMError):
    """LLM provider request timed out."""
    pass
