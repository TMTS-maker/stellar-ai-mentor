"""
Gamification API Schemas

Request and response models for gamification endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid


# ============================================================================
# Badge Schemas
# ============================================================================


class BadgeResponse(BaseModel):
    """Badge information"""

    id: uuid.UUID
    name: str
    description: str
    icon_url: Optional[str] = None
    category: str
    rarity: str

    class Config:
        from_attributes = True


class StudentBadgeResponse(BaseModel):
    """Student's earned badge"""

    id: uuid.UUID
    badge_id: uuid.UUID
    name: str
    description: str
    icon_url: Optional[str] = None
    category: str
    rarity: str
    earned_at: datetime

    class Config:
        from_attributes = True


class BadgeListResponse(BaseModel):
    """List of badges"""

    badges: List[BadgeResponse]
    total_badges: int


class StudentBadgeListResponse(BaseModel):
    """List of student's earned badges"""

    badges: List[StudentBadgeResponse]
    total_earned: int


# ============================================================================
# Streak Schemas
# ============================================================================


class StreakResponse(BaseModel):
    """Student's streak information"""

    student_id: str
    current_streak: int
    longest_streak: int
    last_active_date: str
    streak_continued: Optional[bool] = None
    streak_broken: Optional[bool] = None
    previous_streak: Optional[int] = None


# ============================================================================
# Leaderboard Schemas
# ============================================================================


class LeaderboardEntry(BaseModel):
    """Single leaderboard entry"""

    rank: int
    student_id: str
    student_name: str
    total_xp: int
    current_level: int
    badge_count: int
    current_streak: int


class LeaderboardResponse(BaseModel):
    """Leaderboard rankings"""

    entries: List[LeaderboardEntry]
    total_entries: int
    scope: str  # 'school', 'classroom', 'global'


class StudentRankResponse(BaseModel):
    """Student's rank information"""

    student_id: str
    rank: int
    total_students: int
    total_xp: int
    current_level: int
    percentile: float


# ============================================================================
# Statistics Schemas
# ============================================================================


class GamificationStatsResponse(BaseModel):
    """Comprehensive gamification statistics"""

    student_id: str
    total_xp: int
    current_level: int
    xp_to_next_level: int
    xp_earned_today: int
    badges: dict
    streak: dict
    rank: dict
    total_messages: int
