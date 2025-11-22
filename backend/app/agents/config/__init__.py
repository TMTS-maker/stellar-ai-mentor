"""
Agent configuration module.

Contains grade-based mentor profiles and topic mappings.
"""
from .mentor_grade_profiles import (
    GRADE_BAND_PROFILES,
    get_mentor_grade_profile,
    get_topics_for_grade_band,
    get_recommended_mentors_for_grade
)

__all__ = [
    "GRADE_BAND_PROFILES",
    "get_mentor_grade_profile",
    "get_topics_for_grade_band",
    "get_recommended_mentors_for_grade"
]
