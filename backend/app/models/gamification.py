"""Gamification models: XP events, badges, and student badges"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class XPEvent(Base):
    """XP event tracking for students"""
    __tablename__ = "xp_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True)
    event_type = Column(String, nullable=False)  # session_completed, streak_day, etc.
    xp_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="xp_events")
    task = relationship("Task", back_populates="xp_events")

    def __repr__(self):
        return f"<XPEvent(id={self.id}, type={self.event_type}, xp={self.xp_amount})>"


class Badge(Base):
    """Badge definition model"""
    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    criteria = Column(JSON, nullable=True)  # Achievement criteria

    # Relationships
    student_badges = relationship("StudentBadge", back_populates="badge")

    def __repr__(self):
        return f"<Badge(id={self.id}, name={self.name})>"


class StudentBadge(Base):
    """Student-earned badges"""
    __tablename__ = "student_badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=False)
    awarded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="badges")
    badge = relationship("Badge", back_populates="student_badges")

    def __repr__(self):
        return f"<StudentBadge(id={self.id}, student_id={self.student_id}, badge_id={self.badge_id})>"
