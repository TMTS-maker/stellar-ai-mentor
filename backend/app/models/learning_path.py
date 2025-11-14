"""
LearningPath and LearningModule models for the LEARN phase of LVO architecture.

LearningPaths represent structured learning journeys (e.g., "English A1 Beginner Path").
LearningModules are individual steps within a path.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db import Base


class PathStatus(str, enum.Enum):
    """Status of a student's progress through a learning path."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"


class ModuleStatus(str, enum.Enum):
    """Status of a student's progress through a module."""
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class LearningPath(Base):
    """
    Represents a structured learning journey.

    Examples:
    - "English A1 Beginner Path"
    - "Elementary Math: Numbers & Operations"
    - "Introduction to Science for Kids"
    """
    __tablename__ = "learning_paths"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Recommended age range
    recommended_age_min = Column(Integer, nullable=True)  # e.g., 6
    recommended_age_max = Column(Integer, nullable=True)  # e.g., 10

    # Estimated completion time in hours
    estimated_hours = Column(Integer, nullable=True)

    # Difficulty level (beginner, intermediate, advanced)
    difficulty = Column(String(50), nullable=True, index=True)

    # Prerequisites: IDs of other paths that should be completed first
    prerequisites = Column(JSON, nullable=True)  # e.g., ["path-uuid-1", "path-uuid-2"]

    # Whether this path is currently active/published
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    modules = relationship("LearningModule", back_populates="learning_path", cascade="all, delete-orphan", order_by="LearningModule.order")
    student_paths = relationship("StudentLearningPath", back_populates="learning_path", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<LearningPath(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"


class LearningModule(Base):
    """
    Represents a single module/step within a learning path.

    Each module focuses on specific skills and contains tasks.
    Completion of a module triggers verification checks.
    """
    __tablename__ = "learning_modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    learning_path_id = Column(UUID(as_uuid=True), ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Order within the path (1, 2, 3, ...)
    order = Column(Integer, nullable=False, index=True)

    # IDs of skills that this module teaches/reinforces
    skill_ids = Column(JSON, nullable=True)  # e.g., ["skill-uuid-1", "skill-uuid-2"]

    # IDs of tasks associated with this module
    task_ids = Column(JSON, nullable=True)  # e.g., ["task-uuid-1", "task-uuid-2"]

    # Minimum score required to complete this module (0-100)
    completion_threshold = Column(Integer, default=70, nullable=False)

    # Estimated time to complete in minutes
    estimated_minutes = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    learning_path = relationship("LearningPath", back_populates="modules")
    student_modules = relationship("StudentModule", back_populates="module", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<LearningModule(id={self.id}, name='{self.name}', order={self.order})>"


class StudentLearningPath(Base):
    """
    Tracks a student's enrollment and progress in a learning path.
    """
    __tablename__ = "student_learning_paths"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    learning_path_id = Column(UUID(as_uuid=True), ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False, index=True)

    status = Column(Enum(PathStatus), default=PathStatus.NOT_STARTED, nullable=False, index=True)

    # Progress percentage (0-100)
    progress_percentage = Column(Integer, default=0, nullable=False)

    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="learning_paths")
    learning_path = relationship("LearningPath", back_populates="student_paths")

    def __repr__(self):
        return f"<StudentLearningPath(student_id={self.student_id}, path_id={self.learning_path_id}, status={self.status.value})>"


class StudentModule(Base):
    """
    Tracks a student's progress through a specific module.
    """
    __tablename__ = "student_modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(UUID(as_uuid=True), ForeignKey("learning_modules.id", ondelete="CASCADE"), nullable=False, index=True)

    status = Column(Enum(ModuleStatus), default=ModuleStatus.LOCKED, nullable=False, index=True)

    # Score achieved in this module (0-100)
    score = Column(Float, nullable=True)

    # Number of tasks completed in this module
    tasks_completed = Column(Integer, default=0, nullable=False)

    # Total number of tasks in this module
    tasks_total = Column(Integer, default=0, nullable=False)

    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="modules")
    module = relationship("LearningModule", back_populates="student_modules")

    def __repr__(self):
        return f"<StudentModule(student_id={self.student_id}, module_id={self.module_id}, status={self.status.value})>"
