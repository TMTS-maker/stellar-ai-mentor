"""Unit tests for Routing Policy Engine"""
import pytest
from app.llm.policies import RoutingPolicyEngine
from app.llm.schemas import RoutingHints, RoutingDecision


class TestRoutingPolicyEngine:
    """Test suite for RoutingPolicyEngine."""

    @pytest.fixture
    def policy_engine(self):
        """Create policy engine instance."""
        return RoutingPolicyEngine()

    @pytest.mark.asyncio
    async def test_high_risk_tasks_use_dual_mode(self, policy_engine):
        """Test that high-risk tasks (mastery checks) use dual mode for validation."""
        hints = RoutingHints(
            task_type="mastery_check",
            risk_level="high",
            subject="mathematics",
        )
        context = {"h_pem_proficiency": 0.7}
        availability = {"lucidai": True, "gemini": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        assert isinstance(decision, RoutingDecision)
        # High-risk tasks should use dual mode for validation
        assert decision.mode in ["dual", "hybrid"]
        assert "validation" in decision.reason.lower() or "high-risk" in decision.reason.lower()

    @pytest.mark.asyncio
    async def test_low_proficiency_students_get_lucidai(self, policy_engine):
        """Test that struggling students (low H-PEM) get LucidAI for scaffolding."""
        hints = RoutingHints(
            task_type="tutoring",
            risk_level="low",
            subject="mathematics",
        )
        context = {"h_pem_proficiency": 0.35}  # Struggling student
        availability = {"lucidai": True, "gemini": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # Struggling students should get LucidAI (scaffolding expert)
        assert decision.primary_llm == "lucidai" or "lucidai" in decision.reason.lower()
        assert "scaffolding" in decision.reason.lower() or "struggling" in decision.reason.lower()

    @pytest.mark.asyncio
    async def test_creative_tasks_prefer_gpt4_or_claude(self, policy_engine):
        """Test that creative tasks prefer GPT-4 or Claude."""
        hints = RoutingHints(
            task_type="creative_writing",
            risk_level="low",
            subject="language_arts",
        )
        context = {"h_pem_proficiency": 0.75}
        availability = {"gpt4": True, "claude": True, "gemini": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # Creative tasks should prefer GPT-4 or Claude
        assert decision.primary_llm in ["gpt4", "claude"]
        assert "creative" in decision.reason.lower()

    @pytest.mark.asyncio
    async def test_code_generation_prefers_gpt4_or_claude(self, policy_engine):
        """Test that code generation tasks prefer GPT-4 or Claude."""
        hints = RoutingHints(
            task_type="code_generation",
            risk_level="low",
            subject="computer_science",
        )
        context = {"h_pem_proficiency": 0.8}
        availability = {"gpt4": True, "claude": True, "gemini": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # Coding tasks should prefer GPT-4 or Claude
        assert decision.primary_llm in ["gpt4", "claude"]
        assert "code" in decision.reason.lower() or "coding" in decision.reason.lower()

    @pytest.mark.asyncio
    async def test_advanced_students_get_enrichment(self, policy_engine):
        """Test that advanced students (high H-PEM) get external LLMs for enrichment."""
        hints = RoutingHints(
            task_type="tutoring",
            risk_level="low",
            subject="mathematics",
        )
        context = {"h_pem_proficiency": 0.95}  # Advanced student
        availability = {"gpt4": True, "claude": True, "gemini": True, "lucidai": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # Advanced students should get external LLMs for enrichment
        # (LucidAI focuses on struggling students)
        assert decision.primary_llm in ["gpt4", "claude", "gemini"]

    @pytest.mark.asyncio
    async def test_stem_subjects_prefer_lucidai_when_available(self, policy_engine):
        """Test that STEM subjects prefer LucidAI when available."""
        hints = RoutingHints(
            task_type="tutoring",
            risk_level="medium",
            subject="mathematics",
        )
        context = {"h_pem_proficiency": 0.6}
        availability = {"lucidai": True, "gemini": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # STEM should prefer LucidAI (domain expertise)
        assert decision.primary_llm == "lucidai" or "stem" in decision.reason.lower()

    @pytest.mark.asyncio
    async def test_fallback_when_preferred_llm_unavailable(self, policy_engine):
        """Test fallback behavior when preferred LLM is unavailable."""
        hints = RoutingHints(
            task_type="tutoring",
            risk_level="low",
            subject="mathematics",
        )
        context = {"h_pem_proficiency": 0.3}
        availability = {"lucidai": False, "gemini": True}  # LucidAI unavailable

        decision = await policy_engine.decide_routing(hints, context, availability)

        # Should fallback to available LLM
        assert decision.primary_llm == "gemini"
        assert decision.fallback_llm is None or availability.get(decision.fallback_llm, False)

    @pytest.mark.asyncio
    async def test_prefer_llm_hint_overrides_default_policy(self, policy_engine):
        """Test that explicit LLM preference overrides default policy."""
        hints = RoutingHints(
            task_type="tutoring",
            risk_level="low",
            subject="mathematics",
            prefer_llm="claude",  # Explicit preference
        )
        context = {"h_pem_proficiency": 0.5}
        availability = {"claude": True, "gemini": True, "lucidai": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # Should respect explicit preference
        assert decision.primary_llm == "claude"

    @pytest.mark.asyncio
    async def test_policy_provides_reasoning(self, policy_engine):
        """Test that all routing decisions include reasoning."""
        hints = RoutingHints(
            task_type="tutoring",
            risk_level="low",
            subject="science",
        )
        context = {"h_pem_proficiency": 0.7}
        availability = {"gemini": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # Should always provide reasoning
        assert decision.reason is not None
        assert len(decision.reason) > 0

    @pytest.mark.asyncio
    async def test_multi_factor_decision_making(self, policy_engine):
        """Test that policy engine considers multiple factors."""
        # Conflicting signals: high H-PEM (prefer external) but high-risk (prefer LucidAI)
        hints = RoutingHints(
            task_type="mastery_check",
            risk_level="high",
            subject="mathematics",
        )
        context = {"h_pem_proficiency": 0.92}  # Advanced student
        availability = {"lucidai": True, "gemini": True, "gpt4": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # High-risk should take precedence → dual mode or LucidAI
        assert decision.mode in ["dual", "hybrid"] or decision.primary_llm == "lucidai"
        # Reasoning should mention both factors
        assert len(decision.reason) > 20  # Should be detailed

    @pytest.mark.asyncio
    async def test_policy_handles_missing_context_gracefully(self, policy_engine):
        """Test that policy engine handles missing context gracefully."""
        hints = RoutingHints(
            task_type="tutoring",
            risk_level="low",
            subject="mathematics",
        )
        context = {}  # No student context
        availability = {"gemini": True}

        decision = await policy_engine.decide_routing(hints, context, availability)

        # Should still make a decision with defaults
        assert isinstance(decision, RoutingDecision)
        assert decision.primary_llm is not None
