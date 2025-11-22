"""
Base Curriculum Provider

Abstract base class for curriculum providers.
Implementations can fetch from:
- REST APIs
- MCP servers
- Static JSON files
- CSV/Excel files
- Database imports
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel


class CurriculumData(BaseModel):
    """Standardized curriculum data structure."""

    curriculum_code: str
    curriculum_name: str
    country_code: str
    version_code: str
    grade_bands: List[Dict[str, Any]]
    subjects: List[Dict[str, Any]]
    units: List[Dict[str, Any]]
    topics: List[Dict[str, Any]]
    objectives: List[Dict[str, Any]]

    class Config:
        arbitrary_types_allowed = True


class BaseCurriculumProvider(ABC):
    """
    Abstract base class for curriculum providers.

    Implementations can fetch from:
    - REST APIs
    - MCP servers
    - Static JSON files
    - CSV/Excel files
    - Database imports
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider_type: str = "base"
        self.supported_curricula: List[str] = []

    @abstractmethod
    async def fetch_curriculum(
        self,
        curriculum_code: str,
        version_code: Optional[str] = None
    ) -> CurriculumData:
        """
        Fetch curriculum data from the provider.

        Args:
            curriculum_code: Curriculum identifier (e.g., "CBSE", "UK_NATIONAL")
            version_code: Optional version (defaults to latest)

        Returns:
            Standardized CurriculumData object
        """
        pass

    @abstractmethod
    async def validate_curriculum_structure(self, data: CurriculumData) -> bool:
        """Validate that curriculum data meets requirements."""
        pass

    @abstractmethod
    async def get_available_curricula(self) -> List[Dict[str, str]]:
        """Get list of available curricula from this provider."""
        pass

    def map_to_mentor(self, subject_code: str) -> Optional[str]:
        """
        Map subject to recommended Stellecta mentor.

        Args:
            subject_code: Subject code (e.g., "MATH", "PHYSICS")

        Returns:
            Mentor ID (e.g., "stella", "max") or None
        """
        subject_mentor_map = {
            "MATH": "stella",
            "MATHEMATICS": "stella",
            "PHYSICS": "max",
            "CHEMISTRY": "nova",
            "SCIENCE": "nova",
            "BIOLOGY": "darwin",
            "LIFE_SCIENCE": "darwin",
            "ENGLISH": "lexis",
            "LANGUAGE_ARTS": "lexis",
            "LITERATURE": "lexis",
            "COMPUTER_SCIENCE": "neo",
            "COMPUTING": "neo",
            "ICT": "neo",
            "ART": "luna",
            "ARTS": "luna",
            "MUSIC": "luna",
            "GEOGRAPHY": "atlas",
            "HISTORY": "atlas",
            "SOCIAL_STUDIES": "atlas",
            "SOCIAL_SCIENCE": "atlas",
            "CIVICS": "atlas"
        }
        return subject_mentor_map.get(subject_code.upper())

    def _validate_required_fields(
        self,
        data: Dict[str, Any],
        required_fields: List[str]
    ) -> bool:
        """Helper method to validate required fields in data."""
        return all(field in data and data[field] for field in required_fields)
