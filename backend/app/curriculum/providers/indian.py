"""
Indian Curriculum Provider

Supports:
- CBSE (Central Board of Secondary Education)
- ICSE (Indian Certificate of Secondary Education)

Data source: Static JSON files (can be replaced with API/MCP)
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import os

from .base import BaseCurriculumProvider, CurriculumData


class IndianCurriculumProvider(BaseCurriculumProvider):
    """
    Provider for Indian curricula (CBSE, ICSE, State Boards).

    Currently supports:
    - CBSE (Central Board of Secondary Education)
    - ICSE (Indian Certificate of Secondary Education)

    Data source: Static JSON files (can be replaced with API)
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.provider_type = "indian"
        self.supported_curricula = ["CBSE", "ICSE"]
        self.data_path = Path(config.get("data_path", "data/curricula/indian"))

    async def fetch_curriculum(
        self,
        curriculum_code: str,
        version_code: Optional[str] = None
    ) -> CurriculumData:
        """Fetch Indian curriculum from static files or API."""

        if curriculum_code not in self.supported_curricula:
            raise ValueError(
                f"Unsupported curriculum: {curriculum_code}. "
                f"Supported: {', '.join(self.supported_curricula)}"
            )

        # For now, load from JSON files
        # In production, this could call NCERT/CBSE APIs
        file_path = self.data_path / f"{curriculum_code.lower()}.json"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Curriculum data file not found: {file_path}"
            )

        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        return self._parse_indian_curriculum(raw_data, curriculum_code, version_code)

    def _parse_indian_curriculum(
        self,
        raw_data: Dict[str, Any],
        curriculum_code: str,
        version_code: Optional[str]
    ) -> CurriculumData:
        """Parse Indian curriculum JSON into standardized format."""

        # Extract version (default to latest)
        version = version_code or raw_data.get("current_version", "2023-24")

        # Parse grade bands (CBSE: Primary 1-5, Upper Primary 6-8, Secondary 9-10, Senior 11-12)
        grade_bands = raw_data.get("grade_bands", [
            {
                "name": "Primary",
                "grade_min": 1,
                "grade_max": 5,
                "description": "Foundational stage focusing on basic literacy, numeracy, and play-based learning"
            },
            {
                "name": "Upper Primary",
                "grade_min": 6,
                "grade_max": 8,
                "description": "Middle school stage with subject-specific learning"
            },
            {
                "name": "Secondary",
                "grade_min": 9,
                "grade_max": 10,
                "description": "Secondary stage culminating in board examinations"
            },
            {
                "name": "Senior Secondary",
                "grade_min": 11,
                "grade_max": 12,
                "description": "Higher secondary stage with stream specialization (Science/Commerce/Arts)"
            }
        ])

        # Parse subjects, units, topics, objectives from raw data
        subjects = self._extract_subjects(raw_data)
        units = self._extract_units(raw_data)
        topics = self._extract_topics(raw_data)
        objectives = self._extract_objectives(raw_data)

        return CurriculumData(
            curriculum_code=curriculum_code,
            curriculum_name=raw_data.get("name", f"{curriculum_code} Curriculum"),
            country_code="IND",
            version_code=version,
            grade_bands=grade_bands,
            subjects=subjects,
            units=units,
            topics=topics,
            objectives=objectives
        )

    def _extract_subjects(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract subjects from raw data."""
        subjects = data.get("subjects", [])

        # Add mentor mapping
        for subject in subjects:
            if "code" in subject:
                subject["recommended_mentor_id"] = self.map_to_mentor(subject["code"])

        return subjects

    def _extract_units(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract units from raw data."""
        return data.get("units", [])

    def _extract_topics(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract topics from raw data."""
        return data.get("topics", [])

    def _extract_objectives(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract learning objectives from raw data."""
        return data.get("learning_objectives", [])

    async def validate_curriculum_structure(self, data: CurriculumData) -> bool:
        """Validate that curriculum data meets Indian curriculum requirements."""

        # Validate grade bands
        if len(data.grade_bands) != 4:
            return False

        # Validate required subjects exist
        subject_codes = [s.get("code") for s in data.subjects]
        required_subjects = ["MATH", "SCIENCE", "ENGLISH", "SOCIAL_SCIENCE"]

        if not all(subj in subject_codes for subj in required_subjects):
            return False

        # Validate all objectives have proper codes (format: CBSE.G9.MATH.ALG.LO.001)
        for obj in data.objectives:
            if not obj.get("code") or not obj.get("code").startswith(data.curriculum_code):
                return False

        return True

    async def get_available_curricula(self) -> List[Dict[str, str]]:
        """Get list of available Indian curricula."""
        return [
            {
                "code": "CBSE",
                "name": "Central Board of Secondary Education",
                "country_code": "IND",
                "description": "National curriculum board in India, widely adopted across the country"
            },
            {
                "code": "ICSE",
                "name": "Indian Certificate of Secondary Education",
                "country_code": "IND",
                "description": "Private board curriculum emphasizing comprehensive education"
            }
        ]
