"""
Base Curriculum Provider

Abstract base class for all curriculum providers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CurriculumObjectiveData:
    """Data class for curriculum objective"""
    objective_code: str
    objective_text: str
    subject: str
    grade_level: int
    topic: str
    subtopic: Optional[str]
    difficulty_level: int
    blooms_level: str
    description: Optional[str]
    example_questions: List[str]
    prerequisite_codes: List[str]


class BaseCurriculumProvider(ABC):
    """
    Abstract base class for curriculum providers

    Each curriculum system (CBSE, IGCSE, Common Core) implements this interface
    """

    def __init__(self, curriculum_type: str, curriculum_name: str, country: str, board: Optional[str] = None):
        self.curriculum_type = curriculum_type
        self.curriculum_name = curriculum_name
        self.country = country
        self.board = board

    @abstractmethod
    def get_objectives_for_grade_subject(
        self,
        grade_level: int,
        subject: str
    ) -> List[CurriculumObjectiveData]:
        """
        Get all curriculum objectives for a specific grade and subject

        Args:
            grade_level: Grade level (1-12)
            subject: Subject code (MATH, PHYSICS, etc.)

        Returns:
            List of curriculum objectives
        """
        pass

    @abstractmethod
    def get_objective_by_code(self, objective_code: str) -> Optional[CurriculumObjectiveData]:
        """
        Get a specific curriculum objective by its code

        Args:
            objective_code: Unique objective code (e.g., "CBSE_MATH_10_ALG_001")

        Returns:
            Curriculum objective or None
        """
        pass

    @abstractmethod
    def get_prerequisite_chain(self, objective_code: str) -> List[str]:
        """
        Get the prerequisite chain for an objective

        Args:
            objective_code: Objective code

        Returns:
            List of prerequisite objective codes in order
        """
        pass

    @abstractmethod
    def get_next_objectives(self, objective_code: str) -> List[str]:
        """
        Get objectives that build on this one

        Args:
            objective_code: Current objective code

        Returns:
            List of next objective codes
        """
        pass

    @abstractmethod
    def search_objectives(
        self,
        query: str,
        subject: Optional[str] = None,
        grade_level: Optional[int] = None
    ) -> List[CurriculumObjectiveData]:
        """
        Search for objectives by text query

        Args:
            query: Search query
            subject: Optional subject filter
            grade_level: Optional grade filter

        Returns:
            Matching objectives
        """
        pass

    def get_supported_subjects(self) -> List[str]:
        """Get list of supported subjects"""
        return ["MATH", "PHYSICS", "CHEMISTRY", "BIOLOGY", "LANGUAGE", "HISTORY", "TECH", "ARTS"]

    def get_supported_grades(self) -> List[int]:
        """Get list of supported grade levels"""
        return list(range(1, 13))  # Grades 1-12

    def get_bloom_levels(self) -> List[str]:
        """Get Bloom's Taxonomy levels"""
        return ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

    def validate_objective_code(self, objective_code: str) -> bool:
        """
        Validate objective code format

        Args:
            objective_code: Code to validate

        Returns:
            True if valid
        """
        parts = objective_code.split('_')
        return len(parts) >= 4  # e.g., CBSE_MATH_10_ALG_001

    def get_difficulty_range(self) -> tuple[int, int]:
        """Get min and max difficulty levels"""
        return (1, 10)
