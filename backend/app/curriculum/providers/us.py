"""
US Curriculum Provider

Supports:
- Common Core State Standards (CCSS)
- Next Generation Science Standards (NGSS)

Data source: Static JSON files (can be replaced with API/MCP)
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from .base import BaseCurriculumProvider, CurriculumData


class USCurriculumProvider(BaseCurriculumProvider):
    """
    Provider for US curricula.

    Currently supports:
    - Common Core State Standards (CCSS)
    - Next Generation Science Standards (NGSS)

    Data source: Static JSON files (can be replaced with state APIs)
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.provider_type = "us"
        self.supported_curricula = ["COMMON_CORE", "NGSS"]
        self.data_path = Path(config.get("data_path", "data/curricula/us"))

    async def fetch_curriculum(
        self,
        curriculum_code: str,
        version_code: Optional[str] = None
    ) -> CurriculumData:
        """Fetch US curriculum from static files or API."""

        if curriculum_code not in self.supported_curricula:
            raise ValueError(
                f"Unsupported curriculum: {curriculum_code}. "
                f"Supported: {', '.join(self.supported_curricula)}"
            )

        # For now, load from JSON files
        # In production, this could call Common Core or NGSS APIs
        file_path = self.data_path / f"{curriculum_code.lower()}.json"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Curriculum data file not found: {file_path}"
            )

        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        return self._parse_us_curriculum(raw_data, curriculum_code, version_code)

    def _parse_us_curriculum(
        self,
        raw_data: Dict[str, Any],
        curriculum_code: str,
        version_code: Optional[str]
    ) -> CurriculumData:
        """Parse US curriculum JSON into standardized format."""

        # Extract version (default to latest)
        version = version_code or raw_data.get("current_version", "2010")

        # Parse grade bands (US: K-12 system)
        # Elementary: K-5, Middle: 6-8, High: 9-12
        grade_bands = raw_data.get("grade_bands", [
            {
                "name": "Elementary School",
                "grade_min": 1,
                "grade_max": 5,
                "description": "Elementary education (Grades K-5, Ages 5-11)"
            },
            {
                "name": "Middle School",
                "grade_min": 6,
                "grade_max": 8,
                "description": "Middle school education (Grades 6-8, Ages 11-14)"
            },
            {
                "name": "High School",
                "grade_min": 9,
                "grade_max": 12,
                "description": "High school education (Grades 9-12, Ages 14-18)"
            }
        ])

        # Parse subjects, units, topics, objectives
        subjects = self._extract_subjects(raw_data)
        units = self._extract_units(raw_data)
        topics = self._extract_topics(raw_data)
        objectives = self._extract_objectives(raw_data)

        return CurriculumData(
            curriculum_code=curriculum_code,
            curriculum_name=raw_data.get("name", f"{curriculum_code} Curriculum"),
            country_code="USA",
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
        """Extract units (called 'Domains' in Common Core)."""
        return data.get("units", [])

    def _extract_topics(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract topics from raw data."""
        return data.get("topics", [])

    def _extract_objectives(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract learning objectives (called 'Standards' in Common Core).

        Format: CCSS.MATH.CONTENT.3.OA.A.1
        """
        return data.get("learning_objectives", [])

    async def validate_curriculum_structure(self, data: CurriculumData) -> bool:
        """Validate that curriculum data meets US curriculum requirements."""

        # Validate grade bands
        if len(data.grade_bands) < 3:
            return False

        # Validate required subjects exist
        subject_codes = [s.get("code") for s in data.subjects]

        if data.curriculum_code == "COMMON_CORE":
            required_subjects = ["MATH", "LANGUAGE_ARTS"]
        elif data.curriculum_code == "NGSS":
            required_subjects = ["SCIENCE"]
        else:
            required_subjects = []

        if not all(subj in subject_codes for subj in required_subjects):
            return False

        # Validate all objectives have proper codes
        for obj in data.objectives:
            if not obj.get("code") or not obj.get("code").startswith(data.curriculum_code):
                return False

        return True

    async def get_available_curricula(self) -> List[Dict[str, str]]:
        """Get list of available US curricula."""
        return [
            {
                "code": "COMMON_CORE",
                "name": "Common Core State Standards",
                "country_code": "USA",
                "description": "National standards for Mathematics and English Language Arts"
            },
            {
                "code": "NGSS",
                "name": "Next Generation Science Standards",
                "country_code": "USA",
                "description": "National science education standards"
            }
        ]
