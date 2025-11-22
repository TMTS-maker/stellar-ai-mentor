"""
Database models (SQLAlchemy).

Includes:
- User model
- Conversation model
- Message model
- Progress tracking
- Gamification data (XP, achievements)
- LVO phase tracking
- Curriculum integration (School, Student, Curriculum, etc.)
- LCT (Learning Competency Trajectories)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model (stub)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    active = Column(Boolean, default=True)

    # Relationships
    conversations = relationship("Conversation", back_populates="user")


class Conversation(Base):
    """Conversation model (stub)."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentor_id = Column(String(50), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    lvo_phase = Column(String(20), default="learn")

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    """Message model (stub)."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    provider = Column(String(50))
    model = Column(String(100))

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Achievement(Base):
    """Achievement model (stub)."""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_name = Column(String(100), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)
    xp_awarded = Column(Integer, default=0)


# ============================================================================
# CURRICULUM INTEGRATION MODELS
# ============================================================================


class Curriculum(Base):
    """Curriculum family (e.g., CBSE, ICSE, UK National, Common Core)."""
    __tablename__ = "curricula"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # "CBSE", "ICSE", "UK_NATIONAL"
    name = Column(String(255), nullable=False)
    country_code = Column(String(3), nullable=False)  # "IND", "GBR", "USA"
    description = Column(Text)
    provider_type = Column(String(50), nullable=False)  # "indian", "uk", "us"

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    versions = relationship("CurriculumVersion", back_populates="curriculum")
    schools = relationship("School", back_populates="curriculum")


class CurriculumVersion(Base):
    """Curriculum version (e.g., CBSE 2023-24, Common Core 2010)."""
    __tablename__ = "curriculum_versions"

    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curricula.id"), nullable=False)
    version_code = Column(String(50), nullable=False)  # "2023-24", "2010"
    version_name = Column(String(255))
    effective_from = Column(DateTime)
    effective_to = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    curriculum = relationship("Curriculum", back_populates="versions")
    grade_bands = relationship("GradeBand", back_populates="curriculum_version")


class School(Base):
    """School/Institution model."""
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    country_code = Column(String(3), nullable=False)  # IND, GBR, USA
    curriculum_id = Column(Integer, ForeignKey("curricula.id"))
    curriculum_version_id = Column(Integer, ForeignKey("curriculum_versions.id"))
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    # Relationships
    curriculum = relationship("Curriculum", back_populates="schools")
    curriculum_version = relationship("CurriculumVersion")
    students = relationship("Student", back_populates="school")


class Student(Base):
    """Student model (extends User concept with academic tracking)."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"))
    grade = Column(Integer, nullable=False)  # 1-12
    section = Column(String(10))  # e.g., "A", "B"

    # Curriculum tracking (JSON arrays of IDs)
    current_subjects = Column(JSON, default=list)  # List of subject IDs
    mastered_objectives = Column(JSON, default=list)  # List of objective IDs
    in_progress_objectives = Column(JSON, default=list)  # List of objective IDs

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")
    school = relationship("School", back_populates="students")
    competency_records = relationship("CompetencyRecord", back_populates="student")


class GradeBand(Base):
    """Grade band within a curriculum version (e.g., Primary 1-5, Middle 6-8)."""
    __tablename__ = "grade_bands"

    id = Column(Integer, primary_key=True, index=True)
    curriculum_version_id = Column(Integer, ForeignKey("curriculum_versions.id"), nullable=False)
    name = Column(String(100), nullable=False)  # "Primary", "Middle School"
    grade_min = Column(Integer, nullable=False)
    grade_max = Column(Integer, nullable=False)
    description = Column(Text)

    # Relationships
    curriculum_version = relationship("CurriculumVersion", back_populates="grade_bands")
    subjects = relationship("Subject", back_populates="grade_band")


class Subject(Base):
    """Subject within a grade band (e.g., Mathematics, Science)."""
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    grade_band_id = Column(Integer, ForeignKey("grade_bands.id"), nullable=False)
    code = Column(String(50), nullable=False, index=True)  # "MATH", "SCI", "ENG"
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Mentor mapping
    recommended_mentor_id = Column(String(50))  # Maps to mentor persona ID (stella, max, etc.)

    # Relationships
    grade_band = relationship("GradeBand", back_populates="subjects")
    units = relationship("Unit", back_populates="subject")


class Unit(Base):
    """Unit/Chapter within a subject (e.g., "Algebra", "Cell Biology")."""
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    code = Column(String(50))
    name = Column(String(255), nullable=False)
    sequence_number = Column(Integer)  # Ordering within subject
    description = Column(Text)
    estimated_hours = Column(Integer)  # Teaching time estimate

    # Relationships
    subject = relationship("Subject", back_populates="units")
    topics = relationship("Topic", back_populates="unit")


class Topic(Base):
    """Topic within a unit (e.g., "Linear Equations", "Photosynthesis")."""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    code = Column(String(50))
    name = Column(String(255), nullable=False)
    sequence_number = Column(Integer)
    description = Column(Text)

    # Difficulty/prerequisite tracking
    difficulty_level = Column(String(20))  # "foundational", "intermediate", "advanced"
    prerequisite_topic_ids = Column(JSON, default=list)  # List of topic IDs that must be mastered first

    # Relationships
    unit = relationship("Unit", back_populates="topics")
    learning_objectives = relationship("LearningObjective", back_populates="topic")


class LearningObjective(Base):
    """Specific learning objective/standard (e.g., "Solve 2-variable linear equations")."""
    __tablename__ = "learning_objectives"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    code = Column(String(100), unique=True, nullable=False, index=True)  # e.g., "CBSE.G9.MATH.ALG.LO.001"
    description = Column(Text, nullable=False)

    # Bloom's taxonomy level
    cognitive_level = Column(String(20))  # "remember", "understand", "apply", "analyze", "evaluate", "create"

    # LVO mapping
    lvo_phase_emphasis = Column(String(20))  # "learn", "verify", "own"

    # Relationships
    topic = relationship("Topic", back_populates="learning_objectives")
    competency_records = relationship("CompetencyRecord", back_populates="objective")


class CompetencyRecord(Base):
    """LCT - Student competency tracking for learning objectives."""
    __tablename__ = "competency_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    objective_id = Column(Integer, ForeignKey("learning_objectives.id"), nullable=False)

    # Competency status
    status = Column(String(20), nullable=False)  # "not_started", "in_progress", "mastered", "needs_review"
    mastery_level = Column(Integer, default=0)  # 0-100 percentage

    # H-PEM tracking
    practice_count = Column(Integer, default=0)
    last_practiced_at = Column(DateTime)
    evaluation_score = Column(Integer)  # Last assessment score (0-100)

    # Timestamps
    started_at = Column(DateTime)
    mastered_at = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="competency_records")
    objective = relationship("LearningObjective", back_populates="competency_records")
