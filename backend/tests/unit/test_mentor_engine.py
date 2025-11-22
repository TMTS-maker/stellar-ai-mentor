"""Unit tests for Mentor Engine"""
import pytest
from app.agents.mentor_engine import MentorEngine
from app.agents.personas import get_all_mentors, get_mentor_by_id


class TestMentorEngine:
    """Test suite for MentorEngine."""

    @pytest.fixture
    def mentor_engine(self):
        """Create mentor engine instance."""
        return MentorEngine()

    def test_all_mentors_are_defined(self):
        """Test that all 8 mentors are defined."""
        mentors = get_all_mentors()
        assert len(mentors) == 8

        # Verify all expected mentors exist
        mentor_ids = [m.id for m in mentors]
        expected = ["stella", "max", "nova", "darwin", "lexis", "neo", "luna", "atlas"]
        for mentor_id in expected:
            assert mentor_id in mentor_ids

    def test_get_mentor_by_id_returns_correct_mentor(self):
        """Test that get_mentor_by_id returns the correct mentor."""
        stella = get_mentor_by_id("stella")
        assert stella is not None
        assert stella.id == "stella"
        assert stella.name == "Stella"
        assert stella.subject == "Mathematics"

    def test_mentor_personas_have_required_attributes(self):
        """Test that all mentor personas have required attributes."""
        mentors = get_all_mentors()
        for mentor in mentors:
            assert hasattr(mentor, 'id')
            assert hasattr(mentor, 'name')
            assert hasattr(mentor, 'subject')
            assert hasattr(mentor, 'personality')
            assert hasattr(mentor, 'expertise')
            assert hasattr(mentor, 'teaching_style')
            assert hasattr(mentor, 'system_prompt_template')
            assert hasattr(mentor, 'target_age_range')

    def test_mentor_system_prompts_include_placeholders(self):
        """Test that system prompts include context placeholders."""
        stella = get_mentor_by_id("stella")
        template = stella.system_prompt_template

        # Should have placeholders for context injection
        assert "{student_context}" in template or "student" in template.lower()

    @pytest.mark.asyncio
    async def test_mentor_engine_builds_system_prompt_with_context(
        self, mentor_engine, sample_student_context, sample_conversation_context
    ):
        """Test that mentor engine builds system prompts with student context."""
        mentor = get_mentor_by_id("stella")

        system_prompt = mentor_engine._build_system_prompt(
            mentor=mentor,
            student_context=sample_student_context,
            conversation_context=sample_conversation_context
        )

        # Should include student information
        assert isinstance(system_prompt, str)
        assert len(system_prompt) > 100  # Should be detailed

        # Should mention student proficiency
        assert "proficiency" in system_prompt.lower() or str(sample_student_context["h_pem_proficiency"]) in system_prompt

        # Should mention weak skills
        assert any(skill in system_prompt for skill in sample_student_context["weak_skills"])

    @pytest.mark.asyncio
    async def test_mentor_engine_builds_routing_hints(self, mentor_engine, sample_student_context):
        """Test that mentor engine builds routing hints."""
        mentor = get_mentor_by_id("stella")

        routing_hints = mentor_engine._build_routing_hints(
            mentor=mentor,
            task_type="tutoring",
            student_context=sample_student_context
        )

        # Should include task type and subject
        assert routing_hints.task_type == "tutoring"
        assert routing_hints.subject == mentor.subject.lower().replace(" ", "_")

    @pytest.mark.asyncio
    async def test_mentor_engine_generate_response_returns_valid_format(
        self, mentor_engine, sample_student_context, sample_conversation_context
    ):
        """Test that generate_response returns expected format."""
        result = await mentor_engine.generate_response(
            mentor_id="stella",
            user_message="How do I solve 2x + 3 = 7?",
            student_context=sample_student_context,
            conversation_context=sample_conversation_context
        )

        # Should return dict with expected keys
        assert isinstance(result, dict)
        assert "message" in result
        assert "mentor_id" in result
        assert "llm_used" in result

        # Mentor ID should match
        assert result["mentor_id"] == "stella"

    @pytest.mark.asyncio
    async def test_mentor_engine_handles_invalid_mentor_id(self, mentor_engine, sample_student_context):
        """Test that mentor engine handles invalid mentor IDs gracefully."""
        with pytest.raises(ValueError) as exc_info:
            await mentor_engine.generate_response(
                mentor_id="invalid_mentor",
                user_message="Test message",
                student_context=sample_student_context,
                conversation_context=[]
            )

        assert "not found" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()

    def test_each_mentor_has_unique_subject_expertise(self):
        """Test that each mentor has distinct subject expertise."""
        mentors = get_all_mentors()
        subjects = [m.subject for m in mentors]

        # All subjects should be unique (no duplicate expertise)
        assert len(subjects) == len(set(subjects))

    def test_mentor_personalities_are_diverse(self):
        """Test that mentors have diverse personalities."""
        mentors = get_all_mentors()

        # Collect all personality traits
        all_traits = []
        for mentor in mentors:
            all_traits.extend(mentor.personality)

        # Should have variety (more traits than mentors)
        unique_traits = set(all_traits)
        assert len(unique_traits) > len(mentors)

    @pytest.mark.asyncio
    async def test_mentor_engine_adapts_to_student_proficiency(self, mentor_engine):
        """Test that mentor responses adapt to student proficiency level."""
        # Low proficiency student
        low_proficiency_context = {
            "student_id": "test-1",
            "age": 12,
            "grade_level": 6,
            "h_pem_proficiency": 0.3,
            "weak_skills": ["fractions"],
        }

        # High proficiency student
        high_proficiency_context = {
            "student_id": "test-2",
            "age": 15,
            "grade_level": 9,
            "h_pem_proficiency": 0.9,
            "weak_skills": [],
        }

        # Build prompts for both
        stella = get_mentor_by_id("stella")
        prompt_low = mentor_engine._build_system_prompt(stella, low_proficiency_context, [])
        prompt_high = mentor_engine._build_system_prompt(stella, high_proficiency_context, [])

        # Should mention proficiency levels
        assert "0.3" in prompt_low or "low" in prompt_low.lower()
        assert "0.9" in prompt_high or "high" in prompt_high.lower()

    @pytest.mark.asyncio
    async def test_mentor_engine_includes_conversation_history(self, mentor_engine, sample_student_context):
        """Test that mentor engine includes conversation history in context."""
        conversation = [
            {"role": "user", "content": "I'm stuck on this problem."},
            {"role": "assistant", "content": "Let's work through it together!"},
        ]

        stella = get_mentor_by_id("stella")
        system_prompt = mentor_engine._build_system_prompt(
            stella, sample_student_context, conversation
        )

        # Should reference or include conversation history
        assert "stuck" in system_prompt or "conversation" in system_prompt.lower()
