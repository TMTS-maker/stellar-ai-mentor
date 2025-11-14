"""Gamification-related Pydantic schemas"""
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class XPResponse(BaseModel):
    """Schema for XP data response"""
    total_xp: int
    current_level: int
    level_title: str
    xp_for_current_level: int
    xp_for_next_level: int
    xp_progress_in_level: int
    progress_percentage: int


class BadgeResponse(BaseModel):
    """Schema for badge response"""
    id: UUID
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None

    class Config:
        from_attributes = True


class StudentBadgeResponse(BaseModel):
    """Schema for student badge response"""
    id: UUID
    badge_id: UUID
    badge: BadgeResponse
    awarded_at: datetime

    class Config:
        from_attributes = True


class RingProgress(BaseModel):
    """Ring progress for gamification UI"""
    current_value: int
    goal_value: int
    percentage: int
    is_closed: bool


class RingsResponse(BaseModel):
    """All rings progress"""
    engagement: RingProgress
    mastery: RingProgress
    curiosity: RingProgress


class PlantResponse(BaseModel):
    """Plant/growth gamification response"""
    stage_id: int
    stage_name: str
    total_points: int
    points_to_next_stage: int
    progress_percentage: int


class StreakResponse(BaseModel):
    """Streak data response"""
    current_streak: int
    longest_streak: int
    current_start_date: Optional[str] = None
    streak_freeze_available: int


class AchievementProgress(BaseModel):
    """Achievement progress data"""
    id: str
    name: str
    description: str
    category: str
    progress: int
    required: int


class EarnedAchievement(BaseModel):
    """Earned achievement data"""
    id: str
    name: str
    category: str
    earned_count: int
    earned_at: str


class AchievementsResponse(BaseModel):
    """All achievements response"""
    earned: List[EarnedAchievement]
    available: List[AchievementProgress]
