"""Gamification service for XP calculation and badge management"""
from typing import List, Tuple
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.models.gamification import XPEvent, Badge, StudentBadge
from app.models.student import Student
from app.schemas.gamification import (
    XPResponse, RingsResponse, RingProgress, PlantResponse,
    StreakResponse, AchievementsResponse, EarnedAchievement, AchievementProgress
)


class GamificationService:
    """Service for gamification logic"""

    # XP thresholds for levels (level 0 = 0 XP, level 1 = 100 XP, etc.)
    LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 3500, 5500, 8000, 11000, 15000]

    LEVEL_TITLES = [
        "Beginner",
        "Curious Learner",
        "Dedicated Scholar",
        "Knowledge Seeker",
        "Star Student",
        "Academic Champion",
        "Master Learner",
        "Stellar Scholar",
        "Genius",
        "Legendary Mind"
    ]

    @staticmethod
    async def calculate_total_xp(student_id: UUID, db: AsyncSession) -> int:
        """Calculate total XP for a student"""
        result = await db.execute(
            select(func.sum(XPEvent.xp_amount))
            .where(XPEvent.student_id == student_id)
        )
        total = result.scalar()
        return total or 0

    @classmethod
    async def get_xp_data(cls, student_id: UUID, db: AsyncSession) -> XPResponse:
        """Get XP data for a student"""
        total_xp = await cls.calculate_total_xp(student_id, db)

        # Calculate level
        current_level = 0
        for i, threshold in enumerate(cls.LEVEL_THRESHOLDS):
            if total_xp >= threshold:
                current_level = i
            else:
                break

        # Get XP thresholds for current and next level
        xp_for_current_level = cls.LEVEL_THRESHOLDS[current_level]
        if current_level + 1 < len(cls.LEVEL_THRESHOLDS):
            xp_for_next_level = cls.LEVEL_THRESHOLDS[current_level + 1]
        else:
            xp_for_next_level = xp_for_current_level + 5000

        # Calculate progress in current level
        xp_progress_in_level = total_xp - xp_for_current_level
        xp_needed_for_next = xp_for_next_level - xp_for_current_level
        progress_percentage = int((xp_progress_in_level / xp_needed_for_next) * 100) if xp_needed_for_next > 0 else 0

        # Get level title
        level_title = cls.LEVEL_TITLES[current_level] if current_level < len(cls.LEVEL_TITLES) else "Legend"

        return XPResponse(
            total_xp=total_xp,
            current_level=current_level,
            level_title=level_title,
            xp_for_current_level=xp_for_current_level,
            xp_for_next_level=xp_for_next_level,
            xp_progress_in_level=xp_progress_in_level,
            progress_percentage=progress_percentage
        )

    @staticmethod
    async def award_xp(
        student_id: UUID,
        xp_amount: int,
        event_type: str,
        task_id: UUID = None,
        db: AsyncSession = None
    ) -> XPEvent:
        """Award XP to a student"""
        xp_event = XPEvent(
            student_id=student_id,
            task_id=task_id,
            event_type=event_type,
            xp_amount=xp_amount
        )
        db.add(xp_event)
        await db.commit()
        await db.refresh(xp_event)
        return xp_event

    @staticmethod
    async def check_and_award_badges(student_id: UUID, db: AsyncSession) -> List[Badge]:
        """Check badge criteria and award new badges if earned"""
        # This is a simplified implementation
        # In production, you'd have more sophisticated badge logic
        awarded_badges = []

        # Example: Check for "First Steps" badge (first task completed)
        # This would be called after task completion
        # For now, return empty list as badges need to be pre-seeded

        return awarded_badges

    @staticmethod
    async def get_rings_progress(student_id: UUID, db: AsyncSession) -> RingsResponse:
        """Calculate rings progress (engagement, mastery, curiosity)"""
        # This is mock data for MVP - implement real calculation based on activities
        # Engagement: daily activities
        # Mastery: tasks completed with high scores
        # Curiosity: exploration and questions asked

        return RingsResponse(
            engagement=RingProgress(
                current_value=18,
                goal_value=30,
                percentage=60,
                is_closed=False
            ),
            mastery=RingProgress(
                current_value=4,
                goal_value=5,
                percentage=80,
                is_closed=False
            ),
            curiosity=RingProgress(
                current_value=4,
                goal_value=4,
                percentage=100,
                is_closed=True
            )
        )

    @staticmethod
    async def get_plant_progress(student_id: UUID, db: AsyncSession) -> PlantResponse:
        """Get plant growth progress"""
        total_xp = await GamificationService.calculate_total_xp(student_id, db)

        # Plant stages based on XP
        stages = [
            (0, "Seed"),
            (500, "Sprout"),
            (1500, "Seedling"),
            (3000, "Young Plant"),
            (5000, "Growing Plant"),
            (8000, "Mature Plant"),
            (12000, "Flowering Plant"),
            (18000, "Stellar Tree")
        ]

        stage_id = 0
        stage_name = "Seed"
        points_to_next_stage = 500

        for i, (threshold, name) in enumerate(stages):
            if total_xp >= threshold:
                stage_id = i
                stage_name = name
                if i + 1 < len(stages):
                    points_to_next_stage = stages[i + 1][0] - total_xp
            else:
                break

        progress_percentage = 0
        if stage_id + 1 < len(stages):
            current_stage_threshold = stages[stage_id][0]
            next_stage_threshold = stages[stage_id + 1][0]
            range_size = next_stage_threshold - current_stage_threshold
            progress_in_stage = total_xp - current_stage_threshold
            progress_percentage = int((progress_in_stage / range_size) * 100) if range_size > 0 else 0

        return PlantResponse(
            stage_id=stage_id,
            stage_name=stage_name,
            total_points=total_xp,
            points_to_next_stage=points_to_next_stage,
            progress_percentage=progress_percentage
        )

    @staticmethod
    async def get_streaks(student_id: UUID, db: AsyncSession) -> StreakResponse:
        """Calculate streak data"""
        # This is mock data for MVP
        # In production, track daily activity and calculate real streaks
        return StreakResponse(
            current_streak=12,
            longest_streak=28,
            current_start_date="2025-10-27",
            streak_freeze_available=2
        )

    @staticmethod
    async def get_achievements(student_id: UUID, db: AsyncSession) -> AchievementsResponse:
        """Get earned and available achievements"""
        # This is mock data for MVP
        # In production, calculate based on actual student progress
        earned = [
            EarnedAchievement(
                id="perfect_day",
                name="Perfect Day",
                category="daily",
                earned_count=15,
                earned_at=datetime.utcnow().isoformat()
            ),
            EarnedAchievement(
                id="consistent_scholar",
                name="Consistent Scholar",
                category="streak",
                earned_count=1,
                earned_at="2025-11-04"
            )
        ]

        available = [
            AchievementProgress(
                id="dedicated_student",
                name="Dedicated Student",
                category="streak",
                description="Achieve 30-day streak",
                progress=12,
                required=30
            ),
            AchievementProgress(
                id="master_learner",
                name="Master Learner",
                category="milestone",
                description="Reach Level 5",
                progress=3,
                required=5
            )
        ]

        return AchievementsResponse(earned=earned, available=available)
