"""
Curriculum Service

Handles curriculum ingestion, CRUD operations, and student curriculum tracking.
Integrates with providers and database models.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from ..database.models import (
    Curriculum, CurriculumVersion, School, Student,
    GradeBand, Subject, Unit, Topic, LearningObjective,
    CompetencyRecord
)
from .providers.base import BaseCurriculumProvider, CurriculumData
from .providers.indian import IndianCurriculumProvider
from .providers.uk import UKCurriculumProvider
from .providers.us import USCurriculumProvider


class CurriculumService:
    """Service for curriculum management and ingestion."""

    def __init__(self, db: Session):
        self.db = db
        self.providers: Dict[str, BaseCurriculumProvider] = {}
        self._register_providers()

    def _register_providers(self):
        """Register all curriculum providers."""
        self.providers["indian"] = IndianCurriculumProvider(
            {"data_path": "data/curricula/indian"}
        )
        self.providers["uk"] = UKCurriculumProvider(
            {"data_path": "data/curricula/uk"}
        )
        self.providers["us"] = USCurriculumProvider(
            {"data_path": "data/curricula/us"}
        )

    async def ingest_curriculum(
        self,
        provider_type: str,
        curriculum_code: str,
        version_code: Optional[str] = None
    ) -> Curriculum:
        """
        Ingest curriculum from a provider into the database.

        Args:
            provider_type: "indian", "uk", "us"
            curriculum_code: "CBSE", "UK_NATIONAL", "COMMON_CORE"
            version_code: Optional version identifier

        Returns:
            Created Curriculum object
        """
        provider = self.providers.get(provider_type)
        if not provider:
            raise ValueError(f"Unknown provider: {provider_type}")

        # Fetch curriculum data
        data = await provider.fetch_curriculum(curriculum_code, version_code)

        # Validate structure
        is_valid = await provider.validate_curriculum_structure(data)
        if not is_valid:
            raise ValueError(f"Invalid curriculum structure for {curriculum_code}")

        # Create or update curriculum
        curriculum = self._upsert_curriculum(data, provider_type)

        # Create curriculum version
        version = self._upsert_curriculum_version(curriculum, data)

        # Ingest structure
        self._ingest_grade_bands(version, data.grade_bands)
        self._ingest_subjects(version, data.subjects)
        self._ingest_units(data.units)
        self._ingest_topics(data.topics)
        self._ingest_objectives(data.objectives)

        self.db.commit()
        return curriculum

    def _upsert_curriculum(
        self,
        data: CurriculumData,
        provider_type: str
    ) -> Curriculum:
        """Create or update curriculum."""
        curriculum = self.db.query(Curriculum).filter(
            Curriculum.code == data.curriculum_code
        ).first()

        if curriculum:
            # Update existing
            curriculum.name = data.curriculum_name
            curriculum.country_code = data.country_code
            curriculum.provider_type = provider_type
            curriculum.updated_at = datetime.utcnow()
        else:
            # Create new
            curriculum = Curriculum(
                code=data.curriculum_code,
                name=data.curriculum_name,
                country_code=data.country_code,
                provider_type=provider_type,
                description=f"{data.curriculum_name} curriculum"
            )
            self.db.add(curriculum)
            self.db.flush()  # Get ID

        return curriculum

    def _upsert_curriculum_version(
        self,
        curriculum: Curriculum,
        data: CurriculumData
    ) -> CurriculumVersion:
        """Create or update curriculum version."""
        version = self.db.query(CurriculumVersion).filter(
            and_(
                CurriculumVersion.curriculum_id == curriculum.id,
                CurriculumVersion.version_code == data.version_code
            )
        ).first()

        if version:
            # Update existing
            version.version_name = f"{curriculum.name} {data.version_code}"
            version.is_current = True
        else:
            # Mark other versions as not current
            self.db.query(CurriculumVersion).filter(
                CurriculumVersion.curriculum_id == curriculum.id
            ).update({"is_current": False})

            # Create new
            version = CurriculumVersion(
                curriculum_id=curriculum.id,
                version_code=data.version_code,
                version_name=f"{curriculum.name} {data.version_code}",
                effective_from=datetime.utcnow(),
                is_current=True
            )
            self.db.add(version)
            self.db.flush()

        return version

    def _ingest_grade_bands(
        self,
        version: CurriculumVersion,
        grade_bands: List[Dict[str, Any]]
    ):
        """Ingest grade bands."""
        for gb_data in grade_bands:
            existing = self.db.query(GradeBand).filter(
                and_(
                    GradeBand.curriculum_version_id == version.id,
                    GradeBand.name == gb_data["name"]
                )
            ).first()

            if not existing:
                grade_band = GradeBand(
                    curriculum_version_id=version.id,
                    name=gb_data["name"],
                    grade_min=gb_data["grade_min"],
                    grade_max=gb_data["grade_max"],
                    description=gb_data.get("description")
                )
                self.db.add(grade_band)
                self.db.flush()

    def _ingest_subjects(
        self,
        version: CurriculumVersion,
        subjects: List[Dict[str, Any]]
    ):
        """Ingest subjects."""
        for subj_data in subjects:
            # Find the appropriate grade band
            grade_band = self.db.query(GradeBand).filter(
                and_(
                    GradeBand.curriculum_version_id == version.id,
                    GradeBand.grade_min <= subj_data.get("grade_min", 1),
                    GradeBand.grade_max >= subj_data.get("grade_max", 12)
                )
            ).first()

            if not grade_band:
                # Default to first grade band
                grade_band = self.db.query(GradeBand).filter(
                    GradeBand.curriculum_version_id == version.id
                ).first()

            if grade_band:
                existing = self.db.query(Subject).filter(
                    and_(
                        Subject.grade_band_id == grade_band.id,
                        Subject.code == subj_data["code"]
                    )
                ).first()

                if not existing:
                    subject = Subject(
                        grade_band_id=grade_band.id,
                        code=subj_data["code"],
                        name=subj_data["name"],
                        description=subj_data.get("description"),
                        recommended_mentor_id=subj_data.get("recommended_mentor_id")
                    )
                    self.db.add(subject)
                    self.db.flush()

    def _ingest_units(self, units: List[Dict[str, Any]]):
        """Ingest units."""
        for unit_data in units:
            # Find subject by code
            subject = self.db.query(Subject).filter(
                Subject.code == unit_data.get("subject_code")
            ).first()

            if subject:
                existing = self.db.query(Unit).filter(
                    and_(
                        Unit.subject_id == subject.id,
                        Unit.code == unit_data.get("code")
                    )
                ).first()

                if not existing:
                    unit = Unit(
                        subject_id=subject.id,
                        code=unit_data.get("code"),
                        name=unit_data["name"],
                        sequence_number=unit_data.get("sequence_number"),
                        description=unit_data.get("description"),
                        estimated_hours=unit_data.get("estimated_hours")
                    )
                    self.db.add(unit)
                    self.db.flush()

    def _ingest_topics(self, topics: List[Dict[str, Any]]):
        """Ingest topics."""
        for topic_data in topics:
            # Find unit by code
            unit = self.db.query(Unit).filter(
                Unit.code == topic_data.get("unit_code")
            ).first()

            if unit:
                existing = self.db.query(Topic).filter(
                    and_(
                        Topic.unit_id == unit.id,
                        Topic.code == topic_data.get("code")
                    )
                ).first()

                if not existing:
                    topic = Topic(
                        unit_id=unit.id,
                        code=topic_data.get("code"),
                        name=topic_data["name"],
                        sequence_number=topic_data.get("sequence_number"),
                        description=topic_data.get("description"),
                        difficulty_level=topic_data.get("difficulty_level"),
                        prerequisite_topic_ids=topic_data.get("prerequisite_topic_ids", [])
                    )
                    self.db.add(topic)
                    self.db.flush()

    def _ingest_objectives(self, objectives: List[Dict[str, Any]]):
        """Ingest learning objectives."""
        for obj_data in objectives:
            # Check if objective already exists
            existing = self.db.query(LearningObjective).filter(
                LearningObjective.code == obj_data["code"]
            ).first()

            if not existing:
                # Find topic by code
                topic = self.db.query(Topic).filter(
                    Topic.code == obj_data.get("topic_code")
                ).first()

                if topic:
                    objective = LearningObjective(
                        topic_id=topic.id,
                        code=obj_data["code"],
                        description=obj_data["description"],
                        cognitive_level=obj_data.get("cognitive_level"),
                        lvo_phase_emphasis=obj_data.get("lvo_phase_emphasis", "learn")
                    )
                    self.db.add(objective)
                    self.db.flush()

    def get_curriculum_for_student(self, student_id: int) -> Optional[Curriculum]:
        """Get the curriculum assigned to a student via their school."""
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student or not student.school:
            return None
        return student.school.curriculum

    def get_objectives_for_grade_subject(
        self,
        curriculum_id: int,
        grade: int,
        subject_code: str
    ) -> List[LearningObjective]:
        """Get all learning objectives for a grade/subject combination."""
        # Complex join to get objectives for specific grade and subject
        objectives = (
            self.db.query(LearningObjective)
            .join(Topic)
            .join(Unit)
            .join(Subject)
            .join(GradeBand)
            .join(CurriculumVersion)
            .filter(
                and_(
                    CurriculumVersion.curriculum_id == curriculum_id,
                    CurriculumVersion.is_current == True,
                    Subject.code == subject_code,
                    GradeBand.grade_min <= grade,
                    GradeBand.grade_max >= grade
                )
            )
            .all()
        )
        return objectives

    def get_all_curricula(self) -> List[Curriculum]:
        """Get all curricula in the database."""
        return self.db.query(Curriculum).all()

    def get_curriculum_by_code(self, curriculum_code: str) -> Optional[Curriculum]:
        """Get curriculum by code."""
        return self.db.query(Curriculum).filter(
            Curriculum.code == curriculum_code
        ).first()

    def list_available_providers(self) -> List[str]:
        """List available curriculum provider types."""
        return list(self.providers.keys())
