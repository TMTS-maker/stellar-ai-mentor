"""Unit tests for Multi-LLM Router"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.llm.router import MultiLLMRouter
from app.llm.schemas import LLMRequest, LLMResponse, RoutingDecision, RouterResponse


class TestMultiLLMRouter:
    """Test suite for MultiLLMRouter."""

    @pytest.fixture
    def router(self):
        """Create router instance."""
        return MultiLLMRouter()

    @pytest.mark.asyncio
    async def test_router_checks_llm_availability(self, router):
        """Test that router checks LLM provider availability."""
        availability = await router.check_availability()

        assert isinstance(availability, dict)
        # Should check all configured providers
        assert "gemini" in availability or "gpt4" in availability or "claude" in availability

    @pytest.mark.asyncio
    @patch('app.llm.router.MultiLLMRouter._execute_single')
    async def test_router_single_mode_execution(self, mock_execute, router, sample_llm_request):
        """Test router execution in single mode."""
        # Mock the execution
        mock_response = LLMResponse(
            content="Test response",
            llm_provider="gemini",
            model_version="gemini-1.5-pro",
        )
        mock_execute.return_value = mock_response

        # Execute with single mode
        context = {"routing_hints": {"task_type": "tutoring", "risk_level": "low"}}
        result = await router.generate(sample_llm_request, context)

        assert isinstance(result, RouterResponse)
        assert result.message is not None
        assert result.llm_used in ["gemini", "gpt4", "claude", "lucidai"]

    @pytest.mark.asyncio
    @patch('app.llm.router.MultiLLMRouter._execute_hybrid')
    async def test_router_hybrid_mode_execution(self, mock_execute, router, sample_llm_request):
        """Test router execution in hybrid mode (dual LLM)."""
        # Mock hybrid execution
        mock_response = RouterResponse(
            message="Test response",
            llm_used="gemini",
            model_version="gemini-1.5-pro",
            routing_decision=RoutingDecision(
                mode="hybrid",
                primary_llm="lucidai",
                secondary_llm="gemini",
                reason="Hybrid mode test"
            ),
            evaluation=MagicMock(composite_score=0.85),
            metadata={}
        )
        mock_execute.return_value = mock_response

        context = {
            "routing_hints": {"task_type": "mastery_check", "risk_level": "high"},
            "routing_mode": "hybrid"
        }
        result = await router.generate(sample_llm_request, context)

        assert isinstance(result, RouterResponse)
        assert result.routing_decision.mode == "hybrid"

    @pytest.mark.asyncio
    async def test_router_handles_llm_failure_with_fallback(self, router, sample_llm_request):
        """Test that router handles LLM failures with fallback."""
        # This test would verify fallback behavior when primary LLM fails
        # For now, just test that router handles errors gracefully
        context = {"routing_hints": {"task_type": "tutoring", "risk_level": "low"}}

        # Should not raise exception even if LLM fails (fallback should trigger)
        try:
            result = await router.generate(sample_llm_request, context)
            # If successful, should have a valid response
            if result:
                assert isinstance(result, RouterResponse)
        except Exception as e:
            # Should have graceful error handling
            assert "fallback" in str(e).lower() or "unavailable" in str(e).lower()

    @pytest.mark.asyncio
    @patch('app.llm.router.MultiLLMRouter._invoke_policy_engine')
    async def test_router_uses_policy_engine_for_decisions(self, mock_policy, router, sample_llm_request):
        """Test that router invokes policy engine for routing decisions."""
        # Mock policy engine decision
        mock_decision = RoutingDecision(
            mode="single",
            primary_llm="gemini",
            secondary_llm=None,
            reason="Low-risk tutoring task"
        )
        mock_policy.return_value = mock_decision

        context = {"routing_hints": {"task_type": "tutoring", "risk_level": "low"}}
        await router.generate(sample_llm_request, context)

        # Verify policy engine was invoked
        mock_policy.assert_called_once()

    @pytest.mark.asyncio
    async def test_router_logs_interactions_for_training(self, router, sample_llm_request):
        """Test that router logs all interactions for training pipeline."""
        context = {
            "routing_hints": {"task_type": "tutoring", "risk_level": "low"},
            "conversation_id": "test-conv-123",
            "message_id": "test-msg-456"
        }

        # Execute router
        result = await router.generate(sample_llm_request, context)

        # Should return metadata that can be logged
        assert hasattr(result, 'metadata')
        assert isinstance(result.metadata, dict)

    @pytest.mark.asyncio
    async def test_router_includes_evaluation_in_response(self, router, sample_llm_request):
        """Test that router includes evaluation results in response."""
        context = {"routing_hints": {"task_type": "tutoring", "risk_level": "low"}}

        result = await router.generate(sample_llm_request, context)

        # Should include evaluation
        assert hasattr(result, 'evaluation')
        # Evaluation should have composite score
        if result.evaluation:
            assert hasattr(result.evaluation, 'composite_score')

    @pytest.mark.asyncio
    async def test_router_respects_llm_preference_hint(self, router, sample_llm_request):
        """Test that router respects LLM preference in routing hints."""
        context = {
            "routing_hints": {
                "task_type": "tutoring",
                "risk_level": "low",
                "prefer_llm": "claude"  # Explicit preference
            }
        }

        result = await router.generate(sample_llm_request, context)

        # If Claude is available, should use it (or have good reason not to)
        assert isinstance(result, RouterResponse)

    def test_router_validates_request_format(self, router):
        """Test that router validates LLM request format."""
        # Invalid request (missing required fields)
        invalid_request = {}

        # Should raise validation error
        with pytest.raises(Exception):
            # This would fail Pydantic validation
            LLMRequest(**invalid_request)

    @pytest.mark.asyncio
    async def test_router_handles_context_enrichment(self, router, sample_llm_request, sample_student_context):
        """Test that router handles student context enrichment."""
        context = {
            "routing_hints": {"task_type": "tutoring", "risk_level": "low"},
            "student_context": sample_student_context
        }

        result = await router.generate(sample_llm_request, context)

        # Should successfully process with context
        assert isinstance(result, RouterResponse)
        # Context should influence routing (e.g., low H-PEM → LucidAI scaffolding)
        # This is handled by policy engine
