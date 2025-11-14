"""Task and student progress models"""
import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class TaskStatus(str, enum.Enum):
    """Task status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):
    """Learning task/exercise model"""
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learning_path_id = Column(UUID(as_uuid=True), nullable=True)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    xp_reward = Column(Integer, default=0, nullable=False)
    scenario_type = Column(String, nullable=True)  # conversation, quiz, pronunciation, etc.
    task_metadata = Column(JSON, nullable=True)  # prompt templates, avatar persona, difficulty, etc.

    # Relationships
    subject = relationship("Subject", back_populates="tasks")
    student_progress = relationship("StudentTaskProgress", back_populates="task")
    xp_events = relationship("XPEvent", back_populates="task")
    conversation_sessions = relationship("ConversationSession", back_populates="task")

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title})>"


class StudentTaskProgress(Base):
    """Student progress on tasks"""
    __tablename__ = "student_task_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED, nullable=False)
    score = Column(Integer, nullable=True)
    xp_earned = Column(Integer, default=0, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    last_interaction_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="task_progress")
    task = relationship("Task", back_populates="student_progress")

    def __repr__(self):
        return f"<StudentTaskProgress(id={self.id}, status={self.status})>"
