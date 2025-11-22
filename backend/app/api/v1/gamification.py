"""
Gamification API Endpoints

Handles badges, streaks, leaderboards, and statistics
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_db, get_current_student
from app.database.models.user import Student
from app.services.gamification_service import GamificationService
from app.schemas.gamification import (
    BadgeListResponse,
    StudentBadgeListResponse,
    StreakResponse,
    LeaderboardResponse,
    StudentRankResponse,
    GamificationStatsResponse,
)

router = APIRouter(prefix="/gamification", tags=["gamification"])


# ============================================================================
# Badge Endpoints
# ============================================================================


@router.get("/badges", response_model=BadgeListResponse)
async def get_all_badges(
    db: Session = Depends(get_db), current_student: Student = Depends(get_current_student)
):
    """
    Get all available badges

    Returns list of all badges that can be earned
    """
    gamification_service = GamificationService(db)
    badges = await gamification_service.get_all_badges()

    return {"badges": badges, "total_badges": len(badges)}


@router.get("/student/badges", response_model=StudentBadgeListResponse)
async def get_student_badges(
    db: Session = Depends(get_db), current_student: Student = Depends(get_current_student)
):
    """
    Get student's earned badges

    Returns all badges the current student has earned
    """
    gamification_service = GamificationService(db)
    badges = await gamification_service.get_student_badges(str(current_student.id))

    return {"badges": badges, "total_earned": len(badges)}


@router.post("/student/badges/check")
async def check_badges(
    db: Session = Depends(get_db), current_student: Student = Depends(get_current_student)
):
    """
    Manually trigger badge check

    Checks if student qualifies for any new badges and awards them
    """
    gamification_service = GamificationService(db)
    new_badges = await gamification_service.check_and_award_badges(str(current_student.id))

    return {"new_badges_awarded": len(new_badges), "badges": new_badges}


# ============================================================================
# Streak Endpoints
# ============================================================================


@router.get("/student/streak", response_model=StreakResponse)
async def get_student_streak(
    db: Session = Depends(get_db), current_student: Student = Depends(get_current_student)
):
    """
    Get student's current streak

    Returns daily activity streak information
    """
    gamification_service = GamificationService(db)
    streak = await gamification_service.get_student_streak(str(current_student.id))

    if not streak:
        # Return default streak for new students
        return {
            "student_id": str(current_student.id),
            "current_streak": 0,
            "longest_streak": 0,
            "last_active_date": "never",
        }

    return streak


# ============================================================================
# Leaderboard Endpoints
# ============================================================================


@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100, description="Number of top students"),
    scope: str = Query("school", description="Leaderboard scope: school, classroom, global"),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student),
):
    """
    Get leaderboard rankings

    Returns top students ranked by total XP
    """
    gamification_service = GamificationService(db)

    # Determine school_id based on scope
    school_id = None
    if scope == "school":
        school_id = str(current_student.school_id) if current_student.school_id else None

    entries = await gamification_service.get_leaderboard(school_id=school_id, limit=limit)

    return {"entries": entries, "total_entries": len(entries), "scope": scope}


@router.get("/student/rank", response_model=StudentRankResponse)
async def get_student_rank(
    scope: str = Query("school", description="Ranking scope: school, classroom, global"),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student),
):
    """
    Get student's rank in leaderboard

    Returns student's position relative to other students
    """
    gamification_service = GamificationService(db)

    # Determine school_id based on scope
    school_id = None
    if scope == "school":
        school_id = str(current_student.school_id) if current_student.school_id else None

    rank_info = await gamification_service.get_student_rank(
        student_id=str(current_student.id), school_id=school_id
    )

    if "error" in rank_info:
        raise HTTPException(status_code=404, detail=rank_info["error"])

    return rank_info


# ============================================================================
# Statistics Endpoints
# ============================================================================


@router.get("/student/stats", response_model=GamificationStatsResponse)
async def get_student_statistics(
    db: Session = Depends(get_db), current_student: Student = Depends(get_current_student)
):
    """
    Get comprehensive gamification statistics

    Returns complete overview of student's achievements, progress, and rankings
    """
    gamification_service = GamificationService(db)
    stats = await gamification_service.get_student_statistics(str(current_student.id))

    if "error" in stats:
        raise HTTPException(status_code=404, detail=stats["error"])

    return stats
