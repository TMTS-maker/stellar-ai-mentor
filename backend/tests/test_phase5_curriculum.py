"""
Phase 5 Curriculum Tests

Tests for curriculum providers, curriculum service, and integration
"""

import pytest
from app.curriculum.providers import (
    IndianCBSEProvider,
    UKNationalProvider,
    USCommonCoreProvider,
    get_curriculum_provider,
    list_available_curricula,
)


class TestCurriculumProviders:
    """Test curriculum provider functionality"""

    def test_indian_cbse_provider_initialization(self):
        """Test CBSE provider initializes correctly"""
        provider = IndianCBSEProvider()
        assert provider.curriculum_type == "INDIAN_CBSE"
        assert provider.country == "India"
        assert provider.board == "CBSE"
        assert len(provider.objectives) > 0

    def test_uk_national_provider_initialization(self):
        """Test UK National provider initializes correctly"""
        provider = UKNationalProvider(variant="NATIONAL")
        assert provider.curriculum_type == "UK_NATIONAL"
        assert provider.country == "United Kingdom"
        assert len(provider.objectives) > 0

    def test_uk_igcse_provider_initialization(self):
        """Test UK IGCSE provider initializes correctly"""
        provider = UKNationalProvider(variant="IGCSE")
        assert provider.curriculum_type == "UK_IGCSE"
        assert provider.country == "United Kingdom"
        assert len(provider.objectives) > 0

    def test_us_common_core_provider_initialization(self):
        """Test US Common Core provider initializes correctly"""
        provider = USCommonCoreProvider()
        assert provider.curriculum_type == "US_COMMON_CORE"
        assert provider.country == "United States"
        assert len(provider.objectives) > 0

    def test_get_objectives_for_grade_subject(self):
        """Test getting objectives by grade and subject"""
        provider = IndianCBSEProvider()
        math_objectives = provider.get_objectives_for_grade_subject(10, "MATH")

        assert len(math_objectives) > 0
        for obj in math_objectives:
            assert obj.grade_level == 10
            assert obj.subject == "MATH"

    def test_get_objective_by_code(self):
        """Test getting specific objective by code"""
        provider = IndianCBSEProvider()
        obj = provider.get_objective_by_code("CBSE_MATH_10_ALG_001")

        assert obj is not None
        assert obj.objective_code == "CBSE_MATH_10_ALG_001"
        assert obj.subject == "MATH"
        assert obj.grade_level == 10

    def test_get_prerequisite_chain(self):
        """Test prerequisite chain calculation"""
        provider = IndianCBSEProvider()
        prereqs = provider.get_prerequisite_chain("CBSE_MATH_10_ALG_001")

        assert isinstance(prereqs, list)
        # Should include prerequisites if defined
        if len(prereqs) > 0:
            assert all(isinstance(p, str) for p in prereqs)

    def test_get_next_objectives(self):
        """Test getting next objectives"""
        provider = IndianCBSEProvider()
        # This might be empty for sample data
        next_objs = provider.get_next_objectives("CBSE_MATH_9_ALG_003")

        assert isinstance(next_objs, list)

    def test_search_objectives(self):
        """Test searching objectives"""
        provider = IndianCBSEProvider()
        results = provider.search_objectives("quadratic")

        assert isinstance(results, list)
        if len(results) > 0:
            assert any("quadratic" in obj.objective_text.lower() for obj in results)

    def test_search_objectives_with_filters(self):
        """Test searching with subject and grade filters"""
        provider = IndianCBSEProvider()
        results = provider.search_objectives("quadratic", subject="MATH", grade_level=10)

        assert isinstance(results, list)
        for obj in results:
            assert obj.subject == "MATH"
            assert obj.grade_level == 10

    def test_get_supported_subjects(self):
        """Test getting supported subjects"""
        provider = IndianCBSEProvider()
        subjects = provider.get_supported_subjects()

        assert isinstance(subjects, list)
        assert "MATH" in subjects
        assert "PHYSICS" in subjects
        assert "CHEMISTRY" in subjects

    def test_get_supported_grades(self):
        """Test getting supported grades"""
        provider = IndianCBSEProvider()
        grades = provider.get_supported_grades()

        assert isinstance(grades, list)
        assert 1 in grades
        assert 10 in grades
        assert 12 in grades

    def test_bloom_levels(self):
        """Test Bloom's taxonomy levels"""
        provider = IndianCBSEProvider()
        bloom_levels = provider.get_bloom_levels()

        assert isinstance(bloom_levels, list)
        assert "Remember" in bloom_levels
        assert "Understand" in bloom_levels
        assert "Apply" in bloom_levels
        assert "Create" in bloom_levels

    def test_validate_objective_code(self):
        """Test objective code validation"""
        provider = IndianCBSEProvider()

        assert provider.validate_objective_code("CBSE_MATH_10_ALG_001") is True
        assert provider.validate_objective_code("INVALID") is False
        assert provider.validate_objective_code("CBSE_MATH") is False


class TestCurriculumRegistry:
    """Test curriculum provider registry"""

    def test_list_available_curricula(self):
        """Test listing available curricula"""
        curricula = list_available_curricula()

        assert isinstance(curricula, list)
        assert "INDIAN_CBSE" in curricula
        assert "UK_NATIONAL" in curricula
        assert "UK_IGCSE" in curricula
        assert "US_COMMON_CORE" in curricula

    def test_get_curriculum_provider_cbse(self):
        """Test getting CBSE provider"""
        provider = get_curriculum_provider("INDIAN_CBSE")

        assert isinstance(provider, IndianCBSEProvider)
        assert provider.curriculum_type == "INDIAN_CBSE"

    def test_get_curriculum_provider_uk_national(self):
        """Test getting UK National provider"""
        provider = get_curriculum_provider("UK_NATIONAL")

        assert provider.curriculum_type == "UK_NATIONAL"

    def test_get_curriculum_provider_uk_igcse(self):
        """Test getting UK IGCSE provider"""
        provider = get_curriculum_provider("UK_IGCSE")

        assert provider.curriculum_type == "UK_IGCSE"

    def test_get_curriculum_provider_us_common_core(self):
        """Test getting US Common Core provider"""
        provider = get_curriculum_provider("US_COMMON_CORE")

        assert isinstance(provider, USCommonCoreProvider)
        assert provider.curriculum_type == "US_COMMON_CORE"

    def test_get_curriculum_provider_invalid(self):
        """Test getting invalid provider raises error"""
        with pytest.raises(KeyError):
            get_curriculum_provider("INVALID_CURRICULUM")


class TestCurriculumObjectiveData:
    """Test curriculum objective data structures"""

    def test_objective_has_required_fields(self):
        """Test that objectives have all required fields"""
        provider = IndianCBSEProvider()
        obj = provider.get_objective_by_code("CBSE_MATH_10_ALG_001")

        assert hasattr(obj, "objective_code")
        assert hasattr(obj, "objective_text")
        assert hasattr(obj, "subject")
        assert hasattr(obj, "grade_level")
        assert hasattr(obj, "topic")
        assert hasattr(obj, "difficulty_level")
        assert hasattr(obj, "blooms_level")
        assert hasattr(obj, "example_questions")
        assert hasattr(obj, "prerequisite_codes")

    def test_objective_difficulty_in_range(self):
        """Test that difficulty levels are in valid range"""
        provider = IndianCBSEProvider()
        min_diff, max_diff = provider.get_difficulty_range()

        for obj in provider.objectives.values():
            assert min_diff <= obj.difficulty_level <= max_diff

    def test_objective_blooms_level_valid(self):
        """Test that Bloom's levels are valid"""
        provider = IndianCBSEProvider()
        valid_blooms = provider.get_bloom_levels()

        for obj in provider.objectives.values():
            assert obj.blooms_level in valid_blooms


class TestMultipleCurricula:
    """Test comparing across different curricula"""

    def test_all_providers_have_math(self):
        """Test that all providers have math objectives"""
        providers = [
            IndianCBSEProvider(),
            UKNationalProvider(variant="NATIONAL"),
            USCommonCoreProvider(),
        ]

        for provider in providers:
            math_objs = [obj for obj in provider.objectives.values() if obj.subject == "MATH"]
            assert len(math_objs) > 0, f"{provider.curriculum_type} should have MATH objectives"

    def test_different_objective_code_formats(self):
        """Test that different curricula use different code formats"""
        cbse = IndianCBSEProvider()
        uk = UKNationalProvider(variant="NATIONAL")
        us = USCommonCoreProvider()

        # Get first objective from each
        cbse_code = list(cbse.objectives.keys())[0]
        uk_code = list(uk.objectives.keys())[0]
        us_code = list(us.objectives.keys())[0]

        assert cbse_code.startswith("CBSE_")
        assert uk_code.startswith("UKNAT_")
        assert us_code.startswith("CCSS_") or us_code.startswith("NGSS_")


# Test results summary
def test_summary():
    """Print test summary"""
    print("\n" + "=" * 70)
    print("✅ Phase 5 Curriculum Tests Complete")
    print("=" * 70)
    print("Providers tested:")
    print("  - Indian CBSE")
    print("  - UK National Curriculum")
    print("  - UK IGCSE")
    print("  - US Common Core")
    print("\nFunctionality tested:")
    print("  - Provider initialization")
    print("  - Objective retrieval (by grade/subject/code)")
    print("  - Prerequisite chain calculation")
    print("  - Search functionality")
    print("  - Curriculum registry")
    print("  - Data structure validation")
    print("=" * 70)
