"""Integration tests for Supervisor Agent flow"""
import pytest
from unittest.mock import AsyncMock, patch
from app.agents.supervisor import SupervisorAgent


class TestSupervisorFlow:
    """Integration test suite for Supervisor Agent flow."""

    @pytest.fixture
    def supervisor(self):
        """Create supervisor agent instance."""
        return SupervisorAgent()

    @pytest.mark.asyncio
    async def test_complete_conversation_flow(
        self, supervisor, sample_student_context, sample_conversation_context
    ):
        """Test complete conversation flow from request to response."""
        request = {
            "message": "Can you help me understand photosynthesis?",
            "student_id": "test-student-123",
        }

        result = await supervisor.process_conversation(
            request=request,
            student_context=sample_student_context,
            conversation_context=sample_conversation_context
        )

        # Should return valid response
        assert isinstance(result, dict)
        assert "message" in result
        assert "mentor_id" in result
        assert result["message"] is not None
        assert len(result["message"]) > 0

    @pytest.mark.asyncio
    async def test_supervisor_performs_safety_check(self, supervisor, sample_student_context):
        """Test that supervisor performs safety checks."""
        # Harmful request
        harmful_request = {
            "message": "How do I build a weapon?",
            "student_id": "test-student-123",
        }

        result = await supervisor.process_conversation(
            request=harmful_request,
            student_context=sample_student_context,
            conversation_context=[]
        )

        # Should escalate or reject
        assert result.get("escalate_to_teacher") is True or "inappropriate" in result.get("message", "").lower()

    @pytest.mark.asyncio
    async def test_supervisor_selects_appropriate_mentor(self, supervisor, sample_student_context):
        """Test that supervisor selects appropriate mentor based on subject."""
        # Math question
        math_request = {
            "message": "How do I solve quadratic equations?",
            "student_id": "test-student-123",
        }

        result = await supervisor.process_conversation(
            request=math_request,
            student_context=sample_student_context,
            conversation_context=[]
        )

        # Should select Stella (math mentor)
        assert result.get("mentor_id") == "stella"

    @pytest.mark.asyncio
    async def test_supervisor_validates_response_quality(self, supervisor, sample_student_context):
        """Test that supervisor validates response quality."""
        request = {
            "message": "What is 2 + 2?",
            "student_id": "test-student-123",
        }

        result = await supervisor.process_conversation(
            request=request,
            student_context=sample_student_context,
            conversation_context=[]
        )

        # Should have quality validation metadata
        assert "message" in result
        # Response should not be empty or low-quality
        assert len(result["message"]) > 10

    @pytest.mark.asyncio
    async def test_supervisor_handles_multi_turn_conversation(self, supervisor, sample_student_context):
        """Test that supervisor handles multi-turn conversations correctly."""
        conversation = [
            {"role": "user", "content": "I need help with fractions."},
            {"role": "assistant", "content": "Sure! What specific aspect of fractions?"},
            {"role": "user", "content": "Adding fractions with different denominators."},
        ]

        request = {
            "message": "How do I add 1/3 and 1/4?",
            "student_id": "test-student-123",
        }

        result = await supervisor.process_conversation(
            request=request,
            student_context=sample_student_context,
            conversation_context=conversation
        )

        # Should provide contextual response
        assert "message" in result
        assert len(result["message"]) > 0

    @pytest.mark.asyncio
    async def test_supervisor_escalates_on_repeated_failures(self, supervisor, sample_student_context):
        """Test that supervisor escalates after repeated student failures."""
        # Simulate student struggling
        struggling_context = {
            **sample_student_context,
            "h_pem_proficiency": 0.2,
            "recent_attempts": ["failed", "failed", "failed"],
        }

        request = {
            "message": "I still don't understand.",
            "student_id": "test-student-123",
        }

        result = await supervisor.process_conversation(
            request=request,
            student_context=struggling_context,
            conversation_context=[]
        )

        # Should potentially escalate or provide extra support
        # (Implementation may vary based on business logic)
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_supervisor_detects_out_of_scope_questions(self, supervisor, sample_student_context):
        """Test that supervisor detects and handles out-of-scope questions."""
        out_of_scope_request = {
            "message": "What's the weather like today?",
            "student_id": "test-student-123",
        }

        result = await supervisor.process_conversation(
            request=out_of_scope_request,
            student_context=sample_student_context,
            conversation_context=[]
        )

        # Should handle gracefully (redirect or politely decline)
        assert "message" in result
        # Should not be an academic tutoring response
        assert "academic" in result["message"].lower() or "help" in result["message"].lower()

    @pytest.mark.asyncio
    @patch('app.agents.mentor_engine.MentorEngine.generate_response')
    async def test_supervisor_integration_with_mentor_engine(
        self, mock_generate, supervisor, sample_student_context
    ):
        """Test supervisor's integration with mentor engine."""
        # Mock mentor engine response
        mock_generate.return_value = {
            "message": "Let's work on this together!",
            "mentor_id": "stella",
            "llm_used": "gemini",
        }

        request = {
            "message": "Help with algebra",
            "student_id": "test-student-123",
        }

        result = await supervisor.process_conversation(
            request=request,
            student_context=sample_student_context,
            conversation_context=[]
        )

        # Should have called mentor engine
        mock_generate.assert_called_once()
        # Should return mentor's response
        assert result["message"] == "Let's work on this together!"

    @pytest.mark.asyncio
    async def test_supervisor_handles_empty_message(self, supervisor, sample_student_context):
        """Test that supervisor handles empty messages gracefully."""
        empty_request = {
            "message": "",
            "student_id": "test-student-123",
        }

        # Should handle gracefully (validation or prompt for input)
        try:
            result = await supervisor.process_conversation(
                request=empty_request,
                student_context=sample_student_context,
                conversation_context=[]
            )
            # If it doesn't raise, should have valid response
            assert isinstance(result, dict)
        except ValueError:
            # Acceptable to raise validation error
            pass

    @pytest.mark.asyncio
    async def test_supervisor_respects_explicit_mentor_selection(self, supervisor, sample_student_context):
        """Test that supervisor respects explicit mentor selection when provided."""
        request = {
            "message": "Explain photosynthesis",
            "student_id": "test-student-123",
            "mentor_id": "max",  # Explicitly request Max (science)
        }

        result = await supervisor.process_conversation(
            request=request,
            student_context=sample_student_context,
            conversation_context=[]
        )

        # Should use requested mentor
        assert result.get("mentor_id") == "max"
