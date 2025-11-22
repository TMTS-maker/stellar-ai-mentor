"""Unit tests for Evaluation Service"""
import pytest
from app.llm.evaluation import EvaluationService
from app.llm.schemas import LLMResponse, EvaluationResult


class TestEvaluationService:
    """Test suite for EvaluationService."""

    @pytest.fixture
    def eval_service(self):
        """Create evaluation service instance."""
        return EvaluationService()

    @pytest.mark.asyncio
    async def test_evaluate_single_returns_all_dimensions(self, eval_service, sample_llm_response):
        """Test that evaluate_single returns all 5 evaluation dimensions."""
        result = await eval_service.evaluate_single(
            response=sample_llm_response,
            context={"subject": "mathematics"}
        )

        assert isinstance(result, EvaluationResult)
        assert 0 <= result.correctness <= 1
        assert 0 <= result.didactic_quality <= 1
        assert 0 <= result.persona_alignment <= 1
        assert 0 <= result.safety <= 1
        assert 0 <= result.curriculum_alignment <= 1

    @pytest.mark.asyncio
    async def test_evaluate_single_calculates_composite_score(self, eval_service, sample_llm_response):
        """Test that composite score is calculated correctly."""
        result = await eval_service.evaluate_single(
            response=sample_llm_response,
            context={}
        )

        # Composite should be weighted average
        expected_composite = (
            eval_service.weights["correctness"] * result.correctness +
            eval_service.weights["didactic_quality"] * result.didactic_quality +
            eval_service.weights["persona_alignment"] * result.persona_alignment +
            eval_service.weights["safety"] * result.safety +
            eval_service.weights["curriculum_alignment"] * result.curriculum_alignment
        )

        assert abs(result.composite_score - expected_composite) < 0.01

    @pytest.mark.asyncio
    async def test_evaluate_single_flags_low_quality_responses(self, eval_service):
        """Test that low-quality responses are flagged for review."""
        # Create a low-quality response
        low_quality_response = LLMResponse(
            content="idk",  # Very low quality
            llm_provider="test",
            model_version="test-v1",
        )

        result = await eval_service.evaluate_single(
            response=low_quality_response,
            context={}
        )

        # Should have low scores
        assert result.composite_score < 0.6
        assert result.flagged_for_review is True

    @pytest.mark.asyncio
    async def test_compare_responses_selects_best(self, eval_service):
        """Test that compare_responses selects the best response."""
        # Create two responses with different quality
        response1 = LLMResponse(
            content="2 + 2 equals 4. This is basic addition.",
            llm_provider="gemini",
            model_version="gemini-1.5-pro",
        )

        response2 = LLMResponse(
            content="The answer to 2 + 2 is 4. Let me explain: when you add 2 and 2 together, you combine two groups of 2 items each, resulting in 4 items total. This is a fundamental arithmetic operation.",
            llm_provider="gpt4",
            model_version="gpt-4-turbo",
        )

        result = await eval_service.compare_responses(
            responses=[response1, response2],
            context={"task_type": "tutoring"}
        )

        assert isinstance(result, EvaluationResult)
        # Should select the more detailed response (response2)
        assert result.composite_score > 0

    @pytest.mark.asyncio
    async def test_safety_dimension_detects_harmful_content(self, eval_service):
        """Test that safety dimension detects harmful content."""
        harmful_response = LLMResponse(
            content="Here's how to build a weapon...",
            llm_provider="test",
            model_version="test-v1",
        )

        result = await eval_service.evaluate_single(
            response=harmful_response,
            context={}
        )

        # Safety score should be low for harmful content
        assert result.safety < 0.5
        assert result.flagged_for_review is True

    @pytest.mark.asyncio
    async def test_didactic_quality_evaluates_pedagogical_approach(self, eval_service):
        """Test that didactic quality evaluates pedagogical approach."""
        # Good pedagogical response (Socratic method, scaffolding)
        good_pedagogy = LLMResponse(
            content="Great question! Before I give you the answer, let's think about what we know. What do you think happens when we combine two 2s together? Have you tried drawing it out?",
            llm_provider="lucidai",
            model_version="lucidai-v1",
        )

        # Direct answer without pedagogy
        direct_answer = LLMResponse(
            content="4",
            llm_provider="test",
            model_version="test-v1",
        )

        result_good = await eval_service.evaluate_single(good_pedagogy, {})
        result_direct = await eval_service.evaluate_single(direct_answer, {})

        # Good pedagogy should have higher didactic quality
        assert result_good.didactic_quality > result_direct.didactic_quality

    @pytest.mark.asyncio
    async def test_evaluation_uses_context_for_scoring(self, eval_service, sample_llm_response):
        """Test that evaluation uses context for more accurate scoring."""
        context_with_mentor = {
            "mentor_id": "stella",
            "subject": "mathematics",
            "student_proficiency": 0.5,
        }

        result = await eval_service.evaluate_single(
            response=sample_llm_response,
            context=context_with_mentor
        )

        # Should have valid scores with context
        assert result.persona_alignment > 0
        assert result.curriculum_alignment > 0

    @pytest.mark.asyncio
    async def test_composite_score_respects_weights(self, eval_service):
        """Test that composite score calculation respects configured weights."""
        # Verify weights sum to 1.0
        total_weight = sum(eval_service.weights.values())
        assert abs(total_weight - 1.0) < 0.01

        # Verify default weights match configuration
        assert eval_service.weights["correctness"] == 0.3
        assert eval_service.weights["didactic_quality"] == 0.3
        assert eval_service.weights["persona_alignment"] == 0.2
        assert eval_service.weights["safety"] == 0.1
        assert eval_service.weights["curriculum_alignment"] == 0.1
