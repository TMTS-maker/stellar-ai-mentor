"""Students router"""
from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import get_current_user, require_role
from app.db import get_db
from app.models.user import User
from app.models.student import Student
from app.models.task import Task, StudentTaskProgress, TaskStatus
from app.models.gamification import XPEvent
from app.models.conversation import ConversationSession
from app.schemas.student import StudentResponse, StudentDashboard, StudentBulkCreate
from app.schemas.task import TaskProgressResponse
from app.services.gamification import GamificationService

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/me/dashboard", response_model=StudentDashboard)
async def get_student_dashboard(
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """Get student dashboard data"""
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    # Get XP data
    xp_data = await GamificationService.get_xp_data(student.id, db)

    # Get assigned tasks with progress
    result = await db.execute(
        select(StudentTaskProgress)
        .where(StudentTaskProgress.student_id == student.id)
        .options(selectinload(StudentTaskProgress.task))
        .order_by(StudentTaskProgress.last_interaction_at.desc())
        .limit(10)
    )
    task_progress = result.scalars().all()

    # Get recent conversation sessions
    result = await db.execute(
        select(ConversationSession)
        .where(ConversationSession.student_id == student.id)
        .order_by(ConversationSession.started_at.desc())
        .limit(5)
    )
    recent_sessions = result.scalars().all()

    recent_sessions_data = [
        {
            "id": str(session.id),
            "started_at": session.started_at.isoformat(),
            "ended_at": session.ended_at.isoformat() if session.ended_at else None,
            "avatar_type": session.avatar_type
        }
        for session in recent_sessions
    ]

    return StudentDashboard(
        student=student,
        xp=xp_data,
        assigned_tasks=task_progress,
        recent_sessions=recent_sessions_data
    )


@router.post("/tasks/{task_id}/start")
async def start_task(
    task_id: UUID,
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """Start a task"""
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    # Check if task exists
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if progress already exists
    result = await db.execute(
        select(StudentTaskProgress).where(
            StudentTaskProgress.student_id == student.id,
            StudentTaskProgress.task_id == task_id
        )
    )
    progress = result.scalar_one_or_none()

    if progress:
        # Update existing progress
        progress.status = TaskStatus.IN_PROGRESS
        progress.started_at = datetime.utcnow()
        progress.last_interaction_at = datetime.utcnow()
    else:
        # Create new progress
        progress = StudentTaskProgress(
            student_id=student.id,
            task_id=task_id,
            status=TaskStatus.IN_PROGRESS,
            started_at=datetime.utcnow(),
            last_interaction_at=datetime.utcnow()
        )
        db.add(progress)

    await db.commit()
    await db.refresh(progress)

    return {"status": "started", "progress_id": str(progress.id)}


@router.post("/tasks/{task_id}/complete")
async def complete_task(
    task_id: UUID,
    score: int = 100,
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """Mark task as completed"""
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    # Get task
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Get or create progress
    result = await db.execute(
        select(StudentTaskProgress).where(
            StudentTaskProgress.student_id == student.id,
            StudentTaskProgress.task_id == task_id
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = StudentTaskProgress(
            student_id=student.id,
            task_id=task_id,
            started_at=datetime.utcnow()
        )
        db.add(progress)

    # Update progress
    progress.status = TaskStatus.COMPLETED
    progress.score = score
    progress.xp_earned = task.xp_reward
    progress.completed_at = datetime.utcnow()
    progress.last_interaction_at = datetime.utcnow()

    # Award XP
    xp_event = XPEvent(
        student_id=student.id,
        task_id=task_id,
        event_type="task_completed",
        xp_amount=task.xp_reward
    )
    db.add(xp_event)

    await db.commit()

    return {
        "status": "completed",
        "xp_earned": task.xp_reward,
        "score": score
    }


@router.get("/me/xp")
async def get_student_xp(
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """Get student XP data"""
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    return await GamificationService.get_xp_data(student.id, db)


@router.get("/me/badges")
async def get_student_badges(
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """Get student badges"""
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    # Return achievements data
    return await GamificationService.get_achievements(student.id, db)


@router.get("/me/rings")
async def get_student_rings(
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """Get student rings progress"""
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    return await GamificationService.get_rings_progress(student.id, db)


@router.get("/me/plant")
async def get_student_plant(
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """Get student plant progress"""
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    return await GamificationService.get_plant_progress(student.id, db)


@router.get("/me/streaks")
async def get_student_streaks(
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """Get student streak data"""
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    return await GamificationService.get_streaks(student.id, db)
