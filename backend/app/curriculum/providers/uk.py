"""
UK Curriculum Provider

Supports:
- UK National Curriculum (England)
- IGCSE (International General Certificate of Secondary Education)
- A-Level (Advanced Level)

Data source: Static JSON files (can be replaced with API/MCP)
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from .base import BaseCurriculumProvider, CurriculumData


class UKCurriculumProvider(BaseCurriculumProvider):
    """
    Provider for UK curricula.

    Currently supports:
    - UK National Curriculum (England)
    - IGCSE
    - A-Level

    Data source: Static JSON files (can be replaced with DfE API)
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.provider_type = "uk"
        self.supported_curricula = ["UK_NATIONAL", "IGCSE", "A_LEVEL"]
        self.data_path = Path(config.get("data_path", "data/curricula/uk"))

    async def fetch_curriculum(
        self,
        curriculum_code: str,
        version_code: Optional[str] = None
    ) -> CurriculumData:
        """Fetch UK curriculum from static files or API."""

        if curriculum_code not in self.supported_curricula:
            raise ValueError(
                f"Unsupported curriculum: {curriculum_code}. "
                f"Supported: {', '.join(self.supported_curricula)}"
            )

        # For now, load from JSON files
        # In production, this could call DfE (Department for Education) APIs
        file_path = self.data_path / f"{curriculum_code.lower()}.json"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Curriculum data file not found: {file_path}"
            )

        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        return self._parse_uk_curriculum(raw_data, curriculum_code, version_code)

    def _parse_uk_curriculum(
        self,
        raw_data: Dict[str, Any],
        curriculum_code: str,
        version_code: Optional[str]
    ) -> CurriculumData:
        """Parse UK curriculum JSON into standardized format."""

        # Extract version (default to latest)
        version = version_code or raw_data.get("current_version", "2014")

        # Parse grade bands (UK: Key Stages)
        # KS1: Years 1-2 (Grades 1-2), KS2: Years 3-6 (Grades 3-6)
        # KS3: Years 7-9 (Grades 7-9), KS4: Years 10-11 (Grades 10-11)
        # KS5: Years 12-13 (Grades 12-13) - A-Level
        grade_bands = raw_data.get("grade_bands", [
            {
                "name": "Key Stage 1",
                "grade_min": 1,
                "grade_max": 2,
                "description": "Early foundational learning (Years 1-2, Ages 5-7)"
            },
            {
                "name": "Key Stage 2",
                "grade_min": 3,
                "grade_max": 6,
                "description": "Primary education (Years 3-6, Ages 7-11)"
            },
            {
                "name": "Key Stage 3",
                "grade_min": 7,
                "grade_max": 9,
                "description": "Lower secondary education (Years 7-9, Ages 11-14)"
            },
            {
                "name": "Key Stage 4",
                "grade_min": 10,
                "grade_max": 11,
                "description": "Upper secondary, GCSE preparation (Years 10-11, Ages 14-16)"
            },
            {
                "name": "Key Stage 5",
                "grade_min": 12,
                "grade_max": 13,
                "description": "Post-16 education, A-Level (Years 12-13, Ages 16-18)"
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
            country_code="GBR",
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
        """Extract units (called 'Programmes of Study' in UK curriculum)."""
        return data.get("units", [])

    def _extract_topics(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract topics from raw data."""
        return data.get("topics", [])

    def _extract_objectives(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract learning objectives (called 'Attainment Targets' in UK)."""
        return data.get("learning_objectives", [])

    async def validate_curriculum_structure(self, data: CurriculumData) -> bool:
        """Validate that curriculum data meets UK curriculum requirements."""

        # Validate grade bands (should have Key Stages)
        if len(data.grade_bands) < 4:
            return False

        # Validate required subjects exist
        subject_codes = [s.get("code") for s in data.subjects]
        required_subjects = ["MATH", "ENGLISH", "SCIENCE"]

        if not all(subj in subject_codes for subj in required_subjects):
            return False

        # Validate all objectives have proper codes
        for obj in data.objectives:
            if not obj.get("code") or not obj.get("code").startswith(data.curriculum_code):
                return False

        return True

    async def get_available_curricula(self) -> List[Dict[str, str]]:
        """Get list of available UK curricula."""
        return [
            {
                "code": "UK_NATIONAL",
                "name": "UK National Curriculum (England)",
                "country_code": "GBR",
                "description": "Statutory curriculum for state schools in England"
            },
            {
                "code": "IGCSE",
                "name": "International GCSE",
                "country_code": "GBR",
                "description": "International version of GCSE, widely recognized globally"
            },
            {
                "code": "A_LEVEL",
                "name": "A-Level",
                "country_code": "GBR",
                "description": "Advanced Level qualifications for ages 16-18"
            }
        ]
