"""
Curriculum Models

Implements the comprehensive curriculum system for Indian (CBSE/ICSE), UK, and US curricula
"""
from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, ForeignKey, Text, JSON, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
from datetime import datetime


class Curriculum(Base):
    """Top-level curriculum (e.g., CBSE, IGCSE, Common Core)"""
    __tablename__ = "curricula"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    curriculum_type = Column(String(50), nullable=False, unique=True)  # INDIAN_CBSE, UK_IGCSE, etc.
    curriculum_name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    board = Column(String(100), nullable=True)  # CBSE, ICSE, etc.
    description = Column(Text, nullable=True)

    # Metadata
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    objectives = relationship("CurriculumObjective", back_populates="curriculum")
    students = relationship("Student", back_populates="curriculum")


class CurriculumObjective(Base):
    """Learning objectives/standards for each curriculum"""
    __tablename__ = "curriculum_objectives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    curriculum_id = Column(UUID(as_uuid=True), ForeignKey("curricula.id"), nullable=False)

    # Objective identification
    objective_code = Column(String(100), nullable=False, index=True)  # e.g., "CBSE_MATH_10_ALG_001"
    objective_text = Column(Text, nullable=False)

    # Classification
    subject = Column(String(50), nullable=False, index=True)  # MATH, PHYSICS, etc.
    grade_level = Column(Integer, nullable=False, index=True)
    topic = Column(String(255), nullable=True)
    subtopic = Column(String(255), nullable=True)

    # Difficulty & Prerequisites
    difficulty_level = Column(Integer, nullable=False)  # 1-10
    prerequisite_objective_ids = Column(ARRAY(String), default=list)

    # Bloom's Taxonomy
    blooms_level = Column(String(50), nullable=True)  # Remember, Understand, Apply, Analyze, Evaluate, Create

    # Metadata
    description = Column(Text, nullable=True)
    example_questions = Column(JSON, nullable=True)
    resources = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    curriculum = relationship("Curriculum", back_populates="objectives")
    skills = relationship("Skill", back_populates="objective")


class Skill(Base):
    """Skills derived from curriculum objectives"""
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective_id = Column(UUID(as_uuid=True), ForeignKey("curriculum_objectives.id"), nullable=False)

    skill_name = Column(String(255), nullable=False)
    skill_description = Column(Text, nullable=True)

    # LVO Framework
    learn_criteria = Column(JSON, nullable=True)  # Criteria for "Learn" phase
    verify_criteria = Column(JSON, nullable=True)  # Criteria for "Verify" phase
    own_criteria = Column(JSON, nullable=True)  # Criteria for "Own" phase

    # Metadata
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    objective = relationship("CurriculumObjective", back_populates="skills")
    student_progress = relationship("StudentSkillProgress", back_populates="skill")


class StudentSkillProgress(Base):
    """Track student progress on specific skills (LVO framework)"""
    __tablename__ = "student_skill_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    objective_id = Column(UUID(as_uuid=True), ForeignKey("curriculum_objectives.id"), nullable=False)

    # LVO Progress (0.0 to 1.0)
    learn_progress = Column(Float, default=0.0)
    verify_progress = Column(Float, default=0.0)
    own_progress = Column(Float, default=0.0)

    # Overall mastery (weighted average of LVO)
    mastery_score = Column(Float, default=0.0)

    # H-PEM specific
    h_pem_score = Column(Float, default=0.0)

    # Activity tracking
    attempts_count = Column(Integer, default=0)
    last_practiced = Column(TIMESTAMP, nullable=True)

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="skill_progress")
    skill = relationship("Skill", back_populates="student_progress")
    objective = relationship("CurriculumObjective")
