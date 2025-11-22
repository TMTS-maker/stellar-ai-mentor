"""
Unit tests for curriculum integration and LCT system.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock, patch, AsyncMock

from app.database.models import (
    Base, Curriculum, CurriculumVersion, School, Student, User,
    GradeBand, Subject, Unit, Topic, LearningObjective, CompetencyRecord
)
from app.curriculum.service import CurriculumService
from app.curriculum.providers.indian import IndianCurriculumProvider
from app.curriculum.providers.uk import UKCurriculumProvider
from app.curriculum.providers.us import USCurriculumProvider
from app.lct.trajectories import LCTEngine


# ============================================================================
# Test Database Setup
# ============================================================================

@pytest.fixture
def test_db():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def sample_user(test_db):
    """Create a sample user."""
    user = User(
        username="test_student",
        email="test@example.com",
        age=14,
        total_xp=0,
        level=1
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def sample_curriculum(test_db):
    """Create a sample curriculum."""
    curriculum = Curriculum(
        code="CBSE",
        name="Central Board of Secondary Education",
        country_code="IND",
        provider_type="indian"
    )
    test_db.add(curriculum)
    test_db.commit()
    test_db.refresh(curriculum)
    return curriculum


@pytest.fixture
def sample_curriculum_version(test_db, sample_curriculum):
    """Create a sample curriculum version."""
    version = CurriculumVersion(
        curriculum_id=sample_curriculum.id,
        version_code="2023-24",
        version_name="CBSE 2023-24",
        is_current=True,
        effective_from=datetime.utcnow()
    )
    test_db.add(version)
    test_db.commit()
    test_db.refresh(version)
    return version


@pytest.fixture
def sample_school(test_db, sample_curriculum, sample_curriculum_version):
    """Create a sample school."""
    school = School(
        name="Test School",
        country_code="IND",
        curriculum_id=sample_curriculum.id,
        curriculum_version_id=sample_curriculum_version.id
    )
    test_db.add(school)
    test_db.commit()
    test_db.refresh(school)
    return school


@pytest.fixture
def sample_student(test_db, sample_user, sample_school):
    """Create a sample student."""
    student = Student(
        user_id=sample_user.id,
        school_id=sample_school.id,
        grade=9,
        section="A",
        current_subjects=[],
        mastered_objectives=[],
        in_progress_objectives=[]
    )
    test_db.add(student)
    test_db.commit()
    test_db.refresh(student)
    return student


# ============================================================================
# Curriculum Provider Tests
# ============================================================================

class TestCurriculumProviders:
    """Test curriculum provider implementations."""

    @pytest.mark.asyncio
    async def test_indian_provider_available_curricula(self):
        """Test getting available Indian curricula."""
        provider = IndianCurriculumProvider({"data_path": "data/curricula/indian"})
        curricula = await provider.get_available_curricula()

        assert len(curricula) == 2
        assert any(c["code"] == "CBSE" for c in curricula)
        assert any(c["code"] == "ICSE" for c in curricula)

    @pytest.mark.asyncio
    async def test_uk_provider_available_curricula(self):
        """Test getting available UK curricula."""
        provider = UKCurriculumProvider({"data_path": "data/curricula/uk"})
        curricula = await provider.get_available_curricula()

        assert len(curricula) == 3
        assert any(c["code"] == "UK_NATIONAL" for c in curricula)
        assert any(c["code"] == "IGCSE" for c in curricula)

    @pytest.mark.asyncio
    async def test_us_provider_available_curricula(self):
        """Test getting available US curricula."""
        provider = USCurriculumProvider({"data_path": "data/curricula/us"})
        curricula = await provider.get_available_curricula()

        assert len(curricula) == 2
        assert any(c["code"] == "COMMON_CORE" for c in curricula)
        assert any(c["code"] == "NGSS" for c in curricula)

    def test_mentor_mapping(self):
        """Test subject-to-mentor mapping."""
        provider = IndianCurriculumProvider({"data_path": "data/curricula/indian"})

        assert provider.map_to_mentor("MATH") == "stella"
        assert provider.map_to_mentor("PHYSICS") == "max"
        assert provider.map_to_mentor("CHEMISTRY") == "nova"
        assert provider.map_to_mentor("BIOLOGY") == "darwin"
        assert provider.map_to_mentor("ENGLISH") == "lexis"
        assert provider.map_to_mentor("COMPUTER_SCIENCE") == "neo"
        assert provider.map_to_mentor("ART") == "luna"
        assert provider.map_to_mentor("GEOGRAPHY") == "atlas"


# ============================================================================
# Curriculum Service Tests
# ============================================================================

class TestCurriculumService:
    """Test curriculum service operations."""

    def test_curriculum_service_initialization(self, test_db):
        """Test curriculum service initializes with providers."""
        service = CurriculumService(test_db)

        assert "indian" in service.providers
        assert "uk" in service.providers
        assert "us" in service.providers

    def test_list_available_providers(self, test_db):
        """Test listing available providers."""
        service = CurriculumService(test_db)
        providers = service.list_available_providers()

        assert providers == ["indian", "uk", "us"]

    def test_get_curriculum_for_student(self, test_db, sample_student, sample_curriculum):
        """Test getting curriculum for a student."""
        service = CurriculumService(test_db)
        curriculum = service.get_curriculum_for_student(sample_student.id)

        assert curriculum is not None
        assert curriculum.code == "CBSE"
        assert curriculum.name == "Central Board of Secondary Education"

    def test_get_curriculum_by_code(self, test_db, sample_curriculum):
        """Test getting curriculum by code."""
        service = CurriculumService(test_db)
        curriculum = service.get_curriculum_by_code("CBSE")

        assert curriculum is not None
        assert curriculum.id == sample_curriculum.id

    def test_get_all_curricula(self, test_db, sample_curriculum):
        """Test getting all curricula."""
        service = CurriculumService(test_db)
        curricula = service.get_all_curricula()

        assert len(curricula) >= 1
        assert any(c.code == "CBSE" for c in curricula)


# ============================================================================
# LCT Engine Tests
# ============================================================================

class TestLCTEngine:
    """Test Learning Competency Trajectories engine."""

    def test_lct_engine_initialization(self, test_db):
        """Test LCT engine initializes correctly."""
        engine = LCTEngine(test_db)
        assert engine.db == test_db

    def test_calculate_progression_rate_no_records(self, test_db):
        """Test progression rate calculation with no records."""
        engine = LCTEngine(test_db)
        rate = engine._calculate_progression_rate([])

        assert rate == 0.0

    def test_calculate_progression_rate_with_mastered(self, test_db, sample_student):
        """Test progression rate calculation with mastered objectives."""
        engine = LCTEngine(test_db)

        # Create sample competency records
        now = datetime.utcnow()
        records = []

        for i in range(5):
            record = Mock()
            record.status = "mastered"
            record.mastered_at = now - timedelta(days=i * 7)  # One per week
            records.append(record)

        rate = engine._calculate_progression_rate(records)

        # Should be approximately 1 objective/week (allowing for rounding)
        assert 0.8 <= rate <= 1.5

    def test_get_trajectory_empty(self, test_db, sample_student):
        """Test getting trajectory with no competency records."""
        engine = LCTEngine(test_db)
        trajectory = engine.get_trajectory(sample_student.id)

        assert trajectory["student_id"] == sample_student.id
        assert trajectory["mastered_count"] == 0
        assert trajectory["in_progress_count"] == 0
        assert trajectory["progression_rate"] == 0.0
        assert trajectory["learning_gaps"] == []

    def test_update_competency_new_record(self, test_db, sample_student):
        """Test creating a new competency record."""
        # Create a learning objective first
        grade_band = GradeBand(
            curriculum_version_id=1,
            name="Test Band",
            grade_min=9,
            grade_max=10
        )
        test_db.add(grade_band)
        test_db.flush()

        subject = Subject(
            grade_band_id=grade_band.id,
            code="MATH",
            name="Mathematics"
        )
        test_db.add(subject)
        test_db.flush()

        unit = Unit(
            subject_id=subject.id,
            code="U01",
            name="Test Unit"
        )
        test_db.add(unit)
        test_db.flush()

        topic = Topic(
            unit_id=unit.id,
            code="T01",
            name="Test Topic"
        )
        test_db.add(topic)
        test_db.flush()

        objective = LearningObjective(
            topic_id=topic.id,
            code="TEST.LO.001",
            description="Test objective",
            cognitive_level="understand",
            lvo_phase_emphasis="learn"
        )
        test_db.add(objective)
        test_db.commit()
        test_db.refresh(objective)

        # Create competency record
        engine = LCTEngine(test_db)
        record = engine.update_competency(
            student_id=sample_student.id,
            objective_id=objective.id,
            mastery_level=50,
            status="in_progress"
        )

        assert record.student_id == sample_student.id
        assert record.objective_id == objective.id
        assert record.mastery_level == 50
        assert record.status == "in_progress"
        assert record.practice_count == 1

    def test_update_competency_existing_record(self, test_db, sample_student):
        """Test updating an existing competency record."""
        # Create a learning objective
        grade_band = GradeBand(
            curriculum_version_id=1,
            name="Test Band",
            grade_min=9,
            grade_max=10
        )
        test_db.add(grade_band)
        test_db.flush()

        subject = Subject(
            grade_band_id=grade_band.id,
            code="MATH",
            name="Mathematics"
        )
        test_db.add(subject)
        test_db.flush()

        unit = Unit(
            subject_id=subject.id,
            code="U01",
            name="Test Unit"
        )
        test_db.add(unit)
        test_db.flush()

        topic = Topic(
            unit_id=unit.id,
            code="T01",
            name="Test Topic"
        )
        test_db.add(topic)
        test_db.flush()

        objective = LearningObjective(
            topic_id=topic.id,
            code="TEST.LO.002",
            description="Test objective 2",
            cognitive_level="apply",
            lvo_phase_emphasis="verify"
        )
        test_db.add(objective)
        test_db.commit()
        test_db.refresh(objective)

        engine = LCTEngine(test_db)

        # Create initial record
        record1 = engine.update_competency(
            student_id=sample_student.id,
            objective_id=objective.id,
            mastery_level=50,
            status="in_progress"
        )

        # Update to mastered
        record2 = engine.update_competency(
            student_id=sample_student.id,
            objective_id=objective.id,
            mastery_level=100,
            status="mastered",
            evaluation_score=95
        )

        assert record2.id == record1.id  # Same record
        assert record2.mastery_level == 100
        assert record2.status == "mastered"
        assert record2.evaluation_score == 95
        assert record2.practice_count == 2
        assert record2.mastered_at is not None

    def test_check_prerequisite_mastery_no_prerequisites(self, test_db, sample_student):
        """Test prerequisite check when there are no prerequisites."""
        # Create objective without prerequisites
        grade_band = GradeBand(
            curriculum_version_id=1,
            name="Test Band",
            grade_min=9,
            grade_max=10
        )
        test_db.add(grade_band)
        test_db.flush()

        subject = Subject(
            grade_band_id=grade_band.id,
            code="MATH",
            name="Mathematics"
        )
        test_db.add(subject)
        test_db.flush()

        unit = Unit(
            subject_id=subject.id,
            code="U01",
            name="Test Unit"
        )
        test_db.add(unit)
        test_db.flush()

        topic = Topic(
            unit_id=unit.id,
            code="T01",
            name="Test Topic",
            prerequisite_topic_ids=[]
        )
        test_db.add(topic)
        test_db.flush()

        objective = LearningObjective(
            topic_id=topic.id,
            code="TEST.LO.003",
            description="Test objective 3",
            cognitive_level="remember",
            lvo_phase_emphasis="learn"
        )
        test_db.add(objective)
        test_db.commit()
        test_db.refresh(objective)

        engine = LCTEngine(test_db)
        result = engine.check_prerequisite_mastery(sample_student.id, objective.id)

        assert result["prerequisites_met"] == True
        assert result["readiness_score"] == 100
        assert len(result["missing"]) == 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestCurriculumIntegration:
    """Test integration between curriculum components."""

    def test_full_student_workflow(self, test_db, sample_student, sample_curriculum):
        """Test complete student learning workflow."""
        # 1. Get student's curriculum
        service = CurriculumService(test_db)
        curriculum = service.get_curriculum_for_student(sample_student.id)
        assert curriculum.code == "CBSE"

        # 2. Get trajectory (should be empty initially)
        engine = LCTEngine(test_db)
        trajectory = engine.get_trajectory(sample_student.id)
        assert trajectory["mastered_count"] == 0

        # 3. Create learning objective and update competency
        # (Would need full setup, similar to above tests)
        # This is a simplified integration test

        assert True  # Placeholder for full integration test


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
