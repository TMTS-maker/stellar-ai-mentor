"""
Stellecta LucidAI Backend - Gamification Models

Gamification tracking: XP, achievements, badges, streaks.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database.engine import Base


class GamificationProgress(Base):
    """
    Gamification Progress entity.

    Tracks student's gamification progress:
    - Experience Points (XP)
    - Level
    - Achievements/Badges
    - Streaks
    """

    __tablename__ = "gamification_progress"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Key
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), unique=True, nullable=False, index=True)

    # ========================================================================
    # XP & LEVEL
    # ========================================================================
    total_xp = Column(Integer, default=0, nullable=False)
    """Total experience points earned"""

    level = Column(Integer, default=1, nullable=False)
    """Student's current level (calculated from XP)"""

    # ========================================================================
    # STREAKS
    # ========================================================================
    current_streak_days = Column(Integer, default=0, nullable=False)
    """Current consecutive days of activity"""

    longest_streak_days = Column(Integer, default=0, nullable=False)
    """Longest streak ever achieved"""

    last_activity_date = Column(DateTime(timezone=True), nullable=True)
    """Last date of student activity (for streak calculation)"""

    # ========================================================================
    # ACHIEVEMENTS
    # ========================================================================
    achievements = Column(JSON, default=list, nullable=True)
    """
    List of earned achievement IDs:
    ["first_mastery", "math_champion", "streak_7_days", ...]
    """

    # ========================================================================
    # MASTERY TOKENS (Blockchain-Ready)
    # ========================================================================
    mastery_tokens_earned = Column(Integer, default=0, nullable=False)
    """Total mastery tokens earned (can be minted to blockchain)"""

    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<GamificationProgress(student_id={self.student_id}, level={self.level}, xp={self.total_xp})>"


class Achievement(Base):
    """
    Achievement definition (catalog).

    Defines all available achievements in the system.
    """

    __tablename__ = "achievements"

    # Primary Key
    id = Column(String(50), primary_key=True)
    """Achievement ID (e.g., 'first_mastery', 'math_champion')"""

    # ========================================================================
    # ACHIEVEMENT DETAILS
    # ========================================================================
    name = Column(String(100), nullable=False)
    """Display name"""

    description = Column(String(500), nullable=False)
    """Achievement description"""

    icon = Column(String(50), nullable=True)
    """Icon identifier (emoji or asset path)"""

    xp_reward = Column(Integer, default=0, nullable=False)
    """XP awarded when earned"""

    category = Column(String(50), nullable=True)
    """Category: mastery, streak, social, etc."""

    # ========================================================================
    # CRITERIA
    # ========================================================================
    criteria = Column(JSON, nullable=True)
    """
    Achievement unlock criteria:
    {
        "type": "streak",
        "days": 7
    }
    """

    # ========================================================================
    # METADATA
    # ========================================================================
    is_secret = Column(Boolean, default=False, nullable=False)
    """Hidden until earned"""

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Achievement(id={self.id}, name={self.name})>"
