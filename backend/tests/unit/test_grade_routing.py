"""
Unit tests for grade-aware routing system.

Tests:
- Grade-to-age mapping
- Grade field validation
- Mentor recommendations by grade
- Grade band detection
"""
import pytest
from app.agents.schemas import (
    StudentContext,
    grade_to_age,
    age_to_grade_range
)
from app.agents.config.mentor_grade_profiles import (
    get_grade_band_for_grade,
    get_recommended_mentors_for_grade,
    get_mentor_grade_profile,
    get_topics_for_grade_band
)
from app.agents.personas import MENTOR_PERSONAS


class TestGradeToAgeMapping:
    """Test grade-to-age conversion functions."""

    def test_grade_to_age_valid_grades(self):
        """Test grade_to_age for all valid grades."""
        assert grade_to_age(1) == 6
        assert grade_to_age(2) == 7
        assert grade_to_age(6) == 11
        assert grade_to_age(12) == 17

    def test_grade_to_age_invalid_grades(self):
        """Test grade_to_age with invalid grades."""
        with pytest.raises(ValueError):
            grade_to_age(0)

        with pytest.raises(ValueError):
            grade_to_age(13)

        with pytest.raises(ValueError):
            grade_to_age(-1)

    def test_age_to_grade_range(self):
        """Test age_to_grade_range mapping."""
        assert age_to_grade_range(6) == (1, 2)
        assert age_to_grade_range(7) == (2, 3)
        assert age_to_grade_range(10) == (5, 6)
        assert age_to_grade_range(17) == (12, 12)

    def test_age_to_grade_range_edge_cases(self):
        """Test age_to_grade_range with edge cases."""
        # Too young
        assert age_to_grade_range(5) == (1, 1)
        assert age_to_grade_range(3) == (1, 1)

        # Too old
        assert age_to_grade_range(18) == (12, 12)
        assert age_to_grade_range(20) == (12, 12)


class TestStudentContextWithGrade:
    """Test StudentContext with grade field."""

    def test_student_context_with_grade(self):
        """Test creating StudentContext with valid grade."""
        context = StudentContext(grade=5, age=10)
        assert context.grade == 5
        assert context.age == 10

    def test_student_context_grade_validation(self):
        """Test that invalid grades are rejected."""
        # Valid grades should work
        context1 = StudentContext(grade=1)
        assert context1.grade == 1

        context12 = StudentContext(grade=12)
        assert context12.grade == 12

        # Invalid grades should raise validation error
        with pytest.raises(Exception):  # Pydantic ValidationError
            StudentContext(grade=0)

        with pytest.raises(Exception):
            StudentContext(grade=13)

    def test_get_effective_age(self):
        """Test get_effective_age method."""
        # With grade only
        context1 = StudentContext(grade=3)
        assert context1.get_effective_age() == 8  # Grade 3 → age 8

        # With age only
        context2 = StudentContext(age=15)
        assert context2.get_effective_age() == 15

        # With both (grade takes priority)
        context3 = StudentContext(grade=5, age=12)
        assert context3.get_effective_age() == 10  # Grade 5 → age 10

        # With neither
        context4 = StudentContext()
        assert context4.get_effective_age() is None


class TestGradeBandDetection:
    """Test grade band classification."""

    def test_grade_band_for_grade(self):
        """Test get_grade_band_for_grade function."""
        assert get_grade_band_for_grade(1) == "G1-2"
        assert get_grade_band_for_grade(2) == "G1-2"
        assert get_grade_band_for_grade(3) == "G3-4"
        assert get_grade_band_for_grade(4) == "G3-4"
        assert get_grade_band_for_grade(5) == "G5-8"
        assert get_grade_band_for_grade(8) == "G5-8"
        assert get_grade_band_for_grade(9) == "G9-12"
        assert get_grade_band_for_grade(12) == "G9-12"

    def test_grade_band_invalid_grade(self):
        """Test grade band with invalid grade."""
        with pytest.raises(ValueError):
            get_grade_band_for_grade(0)

        with pytest.raises(ValueError):
            get_grade_band_for_grade(13)


class TestMentorGradeProfiles:
    """Test mentor grade profile configuration."""

    def test_all_mentors_have_profiles(self):
        """Test that all 8 mentors have grade profiles."""
        expected_mentors = ["stella", "max", "nova", "darwin", "lexis", "neo", "luna", "atlas"]

        for mentor_id in expected_mentors:
            profile = get_mentor_grade_profile(mentor_id)
            assert profile is not None, f"{mentor_id} should have a grade profile"
            assert "supported_grades" in profile
            assert "grade_bands" in profile

    def test_mentor_grade_ranges(self):
        """Test that mentors have correct grade ranges."""
        # G1-12 mentors
        for mentor_id in ["stella", "lexis", "luna"]:
            profile = get_mentor_grade_profile(mentor_id)
            supported = list(profile["supported_grades"])
            assert min(supported) == 1
            assert max(supported) == 12

        # G3-12 mentors
        for mentor_id in ["darwin", "atlas"]:
            profile = get_mentor_grade_profile(mentor_id)
            supported = list(profile["supported_grades"])
            assert min(supported) == 3
            assert max(supported) == 12

        # G5-12 mentors
        for mentor_id in ["max", "nova", "neo"]:
            profile = get_mentor_grade_profile(mentor_id)
            supported = list(profile["supported_grades"])
            assert min(supported) == 5
            assert max(supported) == 12

    def test_grade_band_topics(self):
        """Test that each grade band has topics defined."""
        # Stella should have topics for all 4 bands
        stella_profile = get_mentor_grade_profile("stella")
        grade_bands = stella_profile["grade_bands"]

        assert "G1-2" in grade_bands
        assert "G3-4" in grade_bands
        assert "G5-8" in grade_bands
        assert "G9-12" in grade_bands

        # Each band should have topics
        for band_name, band_info in grade_bands.items():
            assert "topics" in band_info
            assert len(band_info["topics"]) > 0
            assert "difficulty" in band_info
            assert "didactic_notes" in band_info

    def test_get_topics_for_grade_band(self):
        """Test retrieving topics for a specific grade band."""
        # Stella G1-2 topics
        topics_g1_2 = get_topics_for_grade_band("stella", "G1-2")
        assert topics_g1_2 is not None
        assert len(topics_g1_2) > 0
        assert any("addition" in topic.lower() for topic in topics_g1_2)

        # Stella G9-12 topics
        topics_g9_12 = get_topics_for_grade_band("stella", "G9-12")
        assert topics_g9_12 is not None
        assert any("calculus" in topic.lower() or "algebra" in topic.lower() for topic in topics_g9_12)

        # Non-existent band
        topics_none = get_topics_for_grade_band("stella", "G99-100")
        assert topics_none is None


class TestMentorRecommendations:
    """Test grade-aware mentor recommendations."""

    def test_recommendations_grade_1(self):
        """Test mentor recommendations for Grade 1."""
        # Grade 1 math
        recommended = get_recommended_mentors_for_grade(1, "math")
        assert "stella" in recommended
        assert "luna" in recommended or "lexis" in recommended

        # Grade 1 reading
        recommended = get_recommended_mentors_for_grade(1, "reading")
        assert "lexis" in recommended

        # Grade 1 art
        recommended = get_recommended_mentors_for_grade(1, "art")
        assert "luna" in recommended

    def test_recommendations_grade_5(self):
        """Test mentor recommendations for Grade 5 (middle school)."""
        # Grade 5 physics
        recommended = get_recommended_mentors_for_grade(5, "physics")
        assert "max" in recommended

        # Grade 5 coding
        recommended = get_recommended_mentors_for_grade(5, "coding")
        assert "neo" in recommended

    def test_recommendations_grade_10(self):
        """Test mentor recommendations for Grade 10 (high school)."""
        # All mentors should be available for high school
        recommended = get_recommended_mentors_for_grade(10)
        assert len(recommended) >= 6  # Most mentors support G9-12

    def test_recommendations_no_subject_filter(self):
        """Test recommendations without subject filter."""
        # Grade 1 without subject
        recommended_g1 = get_recommended_mentors_for_grade(1)
        assert len(recommended_g1) >= 2  # At least Luna, Lexis, Stella

        # Grade 8 without subject
        recommended_g8 = get_recommended_mentors_for_grade(8)
        assert len(recommended_g8) >= 6  # Most mentors by middle school


class TestMentorPersonaGradeFields:
    """Test that MentorPersona models have grade fields."""

    def test_all_mentors_have_grade_fields(self):
        """Test that all mentors have grade_min and grade_max."""
        for mentor_id, mentor in MENTOR_PERSONAS.items():
            assert hasattr(mentor, "grade_min"), f"{mentor_id} missing grade_min"
            assert hasattr(mentor, "grade_max"), f"{mentor_id} missing grade_max"
            assert mentor.grade_min >= 1
            assert mentor.grade_max <= 12
            assert mentor.grade_max >= mentor.grade_min

    def test_grade_ranges_match_profiles(self):
        """Test that MentorPersona grade ranges match grade profiles."""
        for mentor_id, mentor in MENTOR_PERSONAS.items():
            profile = get_mentor_grade_profile(mentor_id)
            supported_grades = list(profile["supported_grades"])

            assert min(supported_grades) == mentor.grade_min
            assert max(supported_grades) == mentor.grade_max


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
