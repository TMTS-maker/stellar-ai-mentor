"""
Unit tests for agent system.

Tests:
- Mentor persona loading
- System prompt rendering
- Prompt assembly
- Supervisor routing logic (without LLM calls)
"""
import pytest
from app.agents.personas import (
    get_mentor_by_id,
    get_supervisor,
    list_mentors,
    MENTOR_PERSONAS
)
from app.agents.schemas import StudentContext, LVOPhase, ConversationMessage
from app.agents.mentor_engine import MentorEngine


class TestMentorPersonas:
    """Test mentor persona definitions."""

    def test_all_mentors_exist(self):
        """Test that all 8 mentors are registered."""
        mentors = list_mentors()
        assert len(mentors) == 8, "Should have exactly 8 mentors"

        expected_ids = ["stella", "max", "nova", "darwin", "lexis", "neo", "luna", "atlas"]
        for mentor_id in expected_ids:
            assert mentor_id in mentors, f"Mentor {mentor_id} should exist"

    def test_mentor_by_id(self):
        """Test getting a mentor by ID."""
        stella = get_mentor_by_id("stella")
        assert stella is not None
        assert stella.id == "stella"
        assert stella.display_name == "Stella"
        assert "Mathematics" in stella.subjects

        # Test non-existent mentor
        fake = get_mentor_by_id("fake_mentor")
        assert fake is None

    def test_mentor_has_required_fields(self):
        """Test that all mentors have required fields."""
        for mentor_id, mentor in MENTOR_PERSONAS.items():
            assert mentor.id == mentor_id
            assert mentor.display_name
            assert mentor.emoji
            assert len(mentor.subjects) > 0
            assert mentor.age_min > 0
            assert mentor.age_max > mentor.age_min
            assert len(mentor.personality_traits) > 0
            assert mentor.voice_tone
            assert mentor.system_prompt_template
            assert "{age_min}" in mentor.system_prompt_template
            assert "{age_max}" in mentor.system_prompt_template
            assert "{subjects}" in mentor.system_prompt_template
            assert "{context}" in mentor.system_prompt_template

    def test_supervisor_exists(self):
        """Test that supervisor persona exists."""
        supervisor = get_supervisor()
        assert supervisor is not None
        assert supervisor.id == "supervisor"
        assert supervisor.system_prompt_template
        assert "{context}" in supervisor.system_prompt_template


class TestPromptAssembly:
    """Test prompt template rendering."""

    def test_build_system_prompt_basic(self):
        """Test basic system prompt building."""
        engine = MentorEngine()
        stella = get_mentor_by_id("stella")

        prompt = engine.build_system_prompt(stella)

        # Check that template variables were replaced
        assert "{age_min}" not in prompt
        assert "{age_max}" not in prompt
        assert "{subjects}" not in prompt
        assert "{context}" not in prompt

        # Check that actual values are present
        assert "12" in prompt  # age_min
        assert "18" in prompt  # age_max
        assert "Mathematics" in prompt  # subject

    def test_build_system_prompt_with_context(self):
        """Test system prompt with student context."""
        engine = MentorEngine()
        neo = get_mentor_by_id("neo")

        context = StudentContext(
            age=15,
            skill_level="intermediate",
            language="English",
            lvo_phase=LVOPhase.VERIFY,
            active_goals=["Learn Python", "Build AI project"]
        )

        prompt = engine.build_system_prompt(neo, context)

        # Check context information is included
        assert "Student age: 15" in prompt
        assert "intermediate" in prompt
        assert "VERIFY" in prompt
        assert "Learn Python" in prompt

    def test_assemble_messages(self):
        """Test message assembly for LLM."""
        engine = MentorEngine()

        system_prompt = "You are a helpful tutor."
        user_message = "What is algebra?"
        history = [
            ConversationMessage(role="user", content="Hello!"),
            ConversationMessage(role="assistant", content="Hi! How can I help you?")
        ]

        messages = engine.assemble_messages(system_prompt, user_message, history)

        # Should have: system + 2 history + current user = 4 messages
        assert len(messages) == 4
        assert messages[0].role == "system"
        assert messages[0].content == system_prompt
        assert messages[-1].role == "user"
        assert messages[-1].content == user_message


class TestSocraticPrinciples:
    """Test that prompts include Socratic principles."""

    def test_prompts_include_socratic_keywords(self):
        """Test that all mentor prompts include Socratic teaching language."""
        socratic_keywords = [
            "socratic",
            "ask",
            "question",
            "what do you think",
            "guide",
            "discover"
        ]

        for mentor_id, mentor in MENTOR_PERSONAS.items():
            prompt_lower = mentor.system_prompt_template.lower()

            # Each prompt should mention Socratic method
            has_socratic = any(keyword in prompt_lower for keyword in socratic_keywords)
            assert has_socratic, f"{mentor_id} prompt should include Socratic keywords"

    def test_prompts_include_pedagogical_principles(self):
        """Test that prompts include key pedagogical concepts."""
        pedagogical_keywords = [
            "growth mindset",
            "scaffold",
            "differentiat",
            "formative",
            "metacognit",
            "social-emotional",
            "sel"
        ]

        for mentor_id, mentor in MENTOR_PERSONAS.items():
            prompt_lower = mentor.system_prompt_template.lower()

            # Count how many principles are mentioned
            count = sum(1 for keyword in pedagogical_keywords if keyword in prompt_lower)
            assert count >= 3, f"{mentor_id} should mention at least 3 pedagogical principles"

    def test_prompts_include_lvo_phases(self):
        """Test that prompts reference LVO phases."""
        lvo_keywords = ["learn", "verify", "own"]

        for mentor_id, mentor in MENTOR_PERSONAS.items():
            prompt_lower = mentor.system_prompt_template.lower()

            # Should mention all three phases
            for phase in lvo_keywords:
                assert phase in prompt_lower, f"{mentor_id} prompt should mention {phase} phase"

    def test_prompts_include_safety_boundaries(self):
        """Test that prompts include safety guidelines."""
        safety_keywords = ["safety", "distress", "trusted adult", "boundary", "boundaries"]

        for mentor_id, mentor in MENTOR_PERSONAS.items():
            prompt_lower = mentor.system_prompt_template.lower()

            has_safety = any(keyword in prompt_lower for keyword in safety_keywords)
            assert has_safety, f"{mentor_id} prompt should include safety boundaries"


class TestLVOPhaseDetection:
    """Test LVO phase detection heuristics."""

    def test_lvo_phase_detection(self):
        """Test basic LVO phase detection."""
        engine = MentorEngine()

        # LEARN phase
        learn_response = "Let's explore this concept. What do you already know about it?"
        phase = engine._detect_lvo_phase("What is photosynthesis?", learn_response)
        assert phase == LVOPhase.LEARN

        # VERIFY phase
        verify_response = "Great! Now try this practice problem: Solve for x..."
        phase = engine._detect_lvo_phase("I think I understand", verify_response)
        assert phase == LVOPhase.VERIFY

        # OWN phase
        own_response = "Excellent! Now teach this concept back to me in your own words."
        phase = engine._detect_lvo_phase("I've got it now", own_response)
        assert phase == LVOPhase.OWN


class TestMentorSpecialization:
    """Test that mentors have appropriate subject specialization."""

    def test_stella_math_specialization(self):
        """Test Stella is specialized in mathematics."""
        stella = get_mentor_by_id("stella")
        assert any("math" in subj.lower() or "algebra" in subj.lower() or "calculus" in subj.lower()
                   for subj in stella.subjects)

    def test_neo_tech_specialization(self):
        """Test Neo is specialized in AI/Technology."""
        neo = get_mentor_by_id("neo")
        assert any("ai" in subj.lower() or "tech" in subj.lower() or "python" in subj.lower()
                   for subj in neo.subjects)

    def test_age_ranges_appropriate(self):
        """Test that age ranges are sensible."""
        for mentor in MENTOR_PERSONAS.values():
            assert 5 <= mentor.age_min <= 18, f"{mentor.id} age_min should be 5-18"
            assert 6 <= mentor.age_max <= 18, f"{mentor.id} age_max should be 6-18"
            assert mentor.age_max > mentor.age_min, f"{mentor.id} age_max should be > age_min"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
