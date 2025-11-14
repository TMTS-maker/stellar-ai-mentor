"""Student model"""
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class Student(Base):
    """Student profile model"""
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    grade_level = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="student_profile")
    school = relationship("School", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    task_progress = relationship("StudentTaskProgress", back_populates="student")
    xp_events = relationship("XPEvent", back_populates="student")
    badges = relationship("StudentBadge", back_populates="student")
    conversation_sessions = relationship("ConversationSession", back_populates="student")
    parent_links = relationship("ParentStudent", back_populates="student")

    # LVO relationships
    skill_scores = relationship("SkillScore", back_populates="student", cascade="all, delete-orphan")
    learning_paths = relationship("StudentLearningPath", back_populates="student", cascade="all, delete-orphan")
    modules = relationship("StudentModule", back_populates="student", cascade="all, delete-orphan")
    verifications = relationship("Verification", back_populates="student", cascade="all, delete-orphan")
    credentials = relationship("Credential", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(id={self.id}, user_id={self.user_id}, grade={self.grade_level})>"
