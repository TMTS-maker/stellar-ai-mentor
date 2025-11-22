"""
Gamification Models

Includes: Badge, StudentBadge, StudentXPLog, StudentStreak
"""

from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, Text, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
from datetime import datetime, date


class Badge(Base):
    """Badge/Achievement definitions"""

    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    icon_url = Column(String(500), nullable=True)
    category = Column(String(50), nullable=False)  # 'streak', 'xp', 'mastery', 'subject'

    # Requirements
    xp_required = Column(Integer, nullable=True)
    streak_required = Column(Integer, nullable=True)
    condition_json = Column(Text, nullable=True)  # JSON string with complex conditions

    # Rarity
    rarity = Column(String(20), default="common")  # common, rare, epic, legendary

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student_badges = relationship("StudentBadge", back_populates="badge")


class StudentBadge(Base):
    """Badges earned by students"""

    __tablename__ = "student_badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=False)

    earned_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="badges")
    badge = relationship("Badge", back_populates="student_badges")


class StudentXPLog(Base):
    """XP transaction log for students"""

    __tablename__ = "student_xp_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)

    xp_amount = Column(Integer, nullable=False)
    source = Column(
        String(100), nullable=False
    )  # 'message', 'correct_answer', 'streak_bonus', etc.
    description = Column(Text, nullable=True)

    # Reference
    session_id = Column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id"), nullable=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=True)

    # Timestamp
    timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="xp_logs")


class StudentStreak(Base):
    """Daily activity streak tracking"""

    __tablename__ = "student_streaks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False, unique=True)

    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)

    last_active_date = Column(Date, default=date.today, nullable=False)

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="streak")
