"""
Stellecta LucidAI Backend - Multi-LLM Router

CORE INNOVATION: Intelligent Multi-LLM orchestration and routing.

Based on Architecture Document Section 3 & 6:
- Multi-LLM Router / Orchestrator
- Intelligent request routing
- Response orchestration (single/dual/hybrid modes)
- Evaluation and selection
- Training data logging integration

The Router is the central abstraction that:
1. Receives requests from agents (Supervisor/Mentors)
2. Decides which LLM(s) to use (via RoutingPolicyEngine)
3. Calls one or more LLM providers
4. Evaluates responses (via EvaluationService)
5. Returns best response + metadata
6. Logs interactions for training

CRITICAL: This replaces direct LLM calls throughout the system.
All agents call router.generate() instead of calling LLMs directly.
"""

import time
from typing import Optional, Dict, Any, List
import structlog

from app.llm.base import BaseLLMClient, LLMError, LLMUnavailableError
from app.llm.schemas import (
    LLMRequest,
    LLMResponse,
    RouterResponse,
    RoutingHints,
    RoutingDecision,
)
from app.llm.providers import (
    LucidAIProvider,
    GeminiProvider,
    OpenAIProvider,
    ClaudeProvider,
)
from app.llm.policies import RoutingPolicyEngine
from app.llm.evaluation import EvaluationService

logger = structlog.get_logger()


class MultiLLMRouter:
    """
    Multi-LLM Router and Orchestrator.

    Central abstraction for all LLM interactions in Stellecta.

    Responsibilities:
    1. Route requests to appropriate LLM(s)
    2. Handle single/dual/hybrid execution modes
    3. Evaluate and select best responses
    4. Provide fallback and error handling
    5. Log all interactions for training
    6. Return responses with full metadata

    Usage (by agents):
        router = MultiLLMRouter()
        response = await router.generate(request, context)
    """

    def __init__(self):
        """Initialize Multi-LLM Router."""

        # Initialize LLM providers
        self.providers: Dict[str, BaseLLMClient] = {
            "lucidai": LucidAIProvider(),
            "gemini": GeminiProvider(),
            "openai": OpenAIProvider(),
            "claude": ClaudeProvider(),
        }

        # Initialize routing policy engine
        self.policy_engine = RoutingPolicyEngine()

        # Initialize evaluation service
        self.evaluation_service = EvaluationService()

        logger.info("MultiLLMRouter initialized", providers=list(self.providers.keys()))

    async def generate(
        self,
        request: LLMRequest,
        context: Optional[Dict[str, Any]] = None,
    ) -> RouterResponse:
        """
        Generate response using intelligent multi-LLM routing.

        This is the main entry point for all LLM interactions.

        Args:
            request: Standardized LLM request
            context: Optional context (student, mentor, task info)

        Returns:
            RouterResponse with selected response and full metadata

        Raises:
            LLMError: If all LLMs fail
        """

        start_time = time.time()

        try:
            # Step 1: Check LLM availability
            llm_availability = await self._check_availability()

            # Step 2: Make routing decision
            routing_decision = await self.policy_engine.decide_routing(
                hints=request.routing_hints,
                context=context,
                llm_availability=llm_availability,
            )

            logger.info(
                "Routing decision made",
                primary_llm=routing_decision.primary_llm,
                policy=routing_decision.policy_applied,
                reason=routing_decision.reason,
            )

            # Step 3: Execute based on mode
            if routing_decision.validate_with:
                # Hybrid mode: Query multiple LLMs and compare
                response, evaluation = await self._execute_hybrid_mode(
                    request,
                    routing_decision,
                    context,
                )
            else:
                # Single mode: Query primary LLM (with fallback if needed)
                response, evaluation = await self._execute_single_mode(
                    request,
                    routing_decision,
                    context,
                )

            # Step 4: Build router response
            router_response = RouterResponse(
                response=response,
                routing_decision=routing_decision,
                evaluation=evaluation,
                metadata={
                    "total_time_ms": int((time.time() - start_time) * 1000),
                    "context_provided": context is not None,
                }
            )

            # Step 5: Log interaction (for training data pipeline)
            # TODO: Implement in training pipeline
            # await self.log_interaction(router_response, context)

            logger.info(
                "Router generation complete",
                llm_used=response.llm_provider,
                composite_score=evaluation.composite_score if evaluation else None,
                total_time_ms=router_response.metadata["total_time_ms"],
            )

            return router_response

        except Exception as e:
            logger.error("Router generation failed", error=str(e))
            raise LLMError(f"Multi-LLM Router failed: {e}")

    async def _execute_single_mode(
        self,
        request: LLMRequest,
        routing_decision: RoutingDecision,
        context: Optional[Dict[str, Any]],
    ) -> tuple[LLMResponse, Optional[Any]]:
        """
        Execute single-LLM mode (with fallback).

        Tries primary LLM, falls back to fallback LLM if primary fails.

        Args:
            request: LLM request
            routing_decision: Routing decision
            context: Optional context

        Returns:
            tuple: (LLMResponse, EvaluationResult or None)

        Raises:
            LLMError: If both primary and fallback fail
        """

        primary_llm = routing_decision.primary_llm
        fallback_llm = routing_decision.fallback_llm

        # Try primary LLM
        try:
            provider = self.providers.get(primary_llm)
            if not provider:
                raise LLMError(f"Provider {primary_llm} not available")

            response = await provider.generate(request)

            # Evaluate response
            evaluation = await self.evaluation_service.evaluate_single(response, context)

            # Check if response is acceptable
            if evaluation.composite_score >= 0.6 and not evaluation.flag_for_review:
                return response, evaluation

            # Low quality: Try fallback if available
            if fallback_llm:
                logger.warning(
                    "Primary LLM response low quality, trying fallback",
                    primary_llm=primary_llm,
                    fallback_llm=fallback_llm,
                    composite_score=evaluation.composite_score,
                )
                # Continue to fallback below
            else:
                # No fallback: Return what we have (may be flagged for review)
                return response, evaluation

        except Exception as e:
            logger.warning(f"Primary LLM {primary_llm} failed", error=str(e))

            # Continue to fallback if available
            if not fallback_llm:
                raise LLMError(f"Primary LLM {primary_llm} failed and no fallback configured")

        # Try fallback LLM
        if fallback_llm:
            try:
                provider = self.providers.get(fallback_llm)
                if not provider:
                    raise LLMError(f"Fallback provider {fallback_llm} not available")

                response = await provider.generate(request)

                # Evaluate fallback response
                evaluation = await self.evaluation_service.evaluate_single(response, context)

                return response, evaluation

            except Exception as e:
                logger.error(f"Fallback LLM {fallback_llm} also failed", error=str(e))
                raise LLMError(f"Both primary ({primary_llm}) and fallback ({fallback_llm}) LLMs failed")

    async def _execute_hybrid_mode(
        self,
        request: LLMRequest,
        routing_decision: RoutingDecision,
        context: Optional[Dict[str, Any]],
    ) -> tuple[LLMResponse, Any]:
        """
        Execute hybrid mode: Query multiple LLMs and compare.

        Queries both primary and validate_with LLMs in parallel,
        then uses EvaluationService to select best.

        Args:
            request: LLM request
            routing_decision: Routing decision
            context: Optional context

        Returns:
            tuple: (Best LLMResponse, EvaluationResult)

        Raises:
            LLMError: If both LLMs fail
        """

        primary_llm = routing_decision.primary_llm
        validate_llm = routing_decision.validate_with

        responses: List[LLMResponse] = []
        errors = []

        # Query primary LLM
        try:
            provider = self.providers.get(primary_llm)
            if provider:
                response = await provider.generate(request)
                responses.append(response)
            else:
                errors.append(f"Provider {primary_llm} not available")
        except Exception as e:
            logger.warning(f"Primary LLM {primary_llm} failed in hybrid mode", error=str(e))
            errors.append(str(e))

        # Query validation LLM
        try:
            provider = self.providers.get(validate_llm)
            if provider:
                response = await provider.generate(request)
                responses.append(response)
            else:
                errors.append(f"Provider {validate_llm} not available")
        except Exception as e:
            logger.warning(f"Validation LLM {validate_llm} failed in hybrid mode", error=str(e))
            errors.append(str(e))

        # Check if we got at least one response
        if not responses:
            raise LLMError(f"Hybrid mode failed: {'; '.join(errors)}")

        # Compare and select best response
        evaluation = await self.evaluation_service.compare_responses(responses, context)

        logger.info(
            "Hybrid mode complete",
            responses_compared=len(responses),
            best_llm=evaluation.selected_response.llm_provider,
            composite_score=evaluation.composite_score,
        )

        return evaluation.selected_response, evaluation

    async def _check_availability(self) -> Dict[str, bool]:
        """
        Check availability of all LLM providers.

        Returns:
            Dict[str, bool]: {provider_name: is_available}
        """

        availability = {}

        for name, provider in self.providers.items():
            try:
                is_available = await provider.is_available()
                availability[name] = is_available
            except Exception as e:
                logger.warning(f"Failed to check availability for {name}", error=str(e))
                availability[name] = False

        logger.debug("LLM availability check", availability=availability)

        return availability

    def get_provider_metrics(self) -> Dict[str, Dict]:
        """
        Get metrics for all providers.

        Returns:
            Dict: {provider_name: metrics_dict}
        """

        metrics = {}
        for name, provider in self.providers.items():
            metrics[name] = provider.get_metrics()

        return metrics

    def reset_provider_metrics(self):
        """Reset metrics for all providers."""

        for provider in self.providers.values():
            provider.reset_metrics()

        logger.info("Provider metrics reset")
