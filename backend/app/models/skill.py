"""
Skill and SkillScore models for the LEARN phase of LVO architecture.

Skills represent specific measurable competencies (e.g., "Reading A1", "Present Simple Tense").
SkillScores track student proficiency levels (0-100) for each skill.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, Enum, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db import Base


class SkillCategory(str, enum.Enum):
    """Categories for organizing skills."""
    LANGUAGE = "language"
    MATH = "math"
    SCIENCE = "science"
    SOCIAL_STUDIES = "social_studies"
    ART = "art"
    MUSIC = "music"
    PHYSICAL_EDUCATION = "physical_education"
    LIFE_SKILLS = "life_skills"
    CRITICAL_THINKING = "critical_thinking"
    OTHER = "other"


# Association table for many-to-many relationship between Tasks and Skills
task_skills = Table(
    "task_skills",
    Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)


class Skill(Base):
    """
    Represents a specific competency or learning objective.

    Examples:
    - "Reading Comprehension Level A1"
    - "Present Simple Tense"
    - "Basic Addition (1-10)"
    - "Identifying Emotions"
    """
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(Enum(SkillCategory), nullable=False, default=SkillCategory.OTHER, index=True)

    # Level indicates difficulty or progression (e.g., A1, A2, B1 for languages; 1-5 for math)
    level = Column(String(50), nullable=True, index=True)

    # Recommended age range
    age_group_min = Column(Integer, nullable=True)  # e.g., 6
    age_group_max = Column(Integer, nullable=True)  # e.g., 10

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    skill_scores = relationship("SkillScore", back_populates="skill", cascade="all, delete-orphan")
    tasks = relationship("Task", secondary=task_skills, back_populates="skills")

    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}', category={self.category.value}, level='{self.level}')>"


class SkillScore(Base):
    """
    Tracks a student's proficiency in a specific skill.

    Score ranges from 0-100:
    - 0-29: Beginner
    - 30-59: Developing
    - 60-79: Proficient
    - 80-100: Advanced/Mastered
    """
    __tablename__ = "skill_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)

    # Proficiency score (0-100)
    score = Column(Float, default=0.0, nullable=False)

    # Confidence level (0.0 - 1.0) - how confident the system is in this score
    confidence = Column(Float, default=0.5, nullable=False)

    # Number of assessments/tasks that contributed to this score
    assessment_count = Column(Integer, default=0, nullable=False)

    # Last time this skill was practiced
    last_practiced_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="skill_scores")
    skill = relationship("Skill", back_populates="skill_scores")

    def __repr__(self):
        return f"<SkillScore(student_id={self.student_id}, skill_id={self.skill_id}, score={self.score:.1f})>"

    @property
    def proficiency_level(self) -> str:
        """Get human-readable proficiency level based on score."""
        if self.score < 30:
            return "Beginner"
        elif self.score < 60:
            return "Developing"
        elif self.score < 80:
            return "Proficient"
        else:
            return "Advanced"
