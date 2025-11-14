"""Teachers router"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import get_current_user, require_role
from app.db import get_db
from app.models.user import User
from app.models.teacher import Teacher
from app.models.classroom import Classroom
from app.models.student import Student
from app.models.task import StudentTaskProgress
from app.schemas.classroom import ClassroomResponse

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/me/classes", response_model=List[ClassroomResponse])
async def get_teacher_classes(
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Get all classes for the current teacher"""
    # Get teacher profile
    result = await db.execute(
        select(Teacher).where(Teacher.user_id == current_user.id)
    )
    teacher = result.scalar_one_or_none()

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
        )

    # Get classrooms
    result = await db.execute(
        select(Classroom).where(Classroom.teacher_id == teacher.id)
    )
    classrooms = result.scalars().all()

    return classrooms


@router.get("/me/classes/{class_id}/students/progress")
async def get_class_student_progress(
    class_id: UUID,
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Get progress for all students in a class"""
    # Get teacher profile
    result = await db.execute(
        select(Teacher).where(Teacher.user_id == current_user.id)
    )
    teacher = result.scalar_one_or_none()

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
        )

    # Verify teacher owns this class
    result = await db.execute(
        select(Classroom).where(
            Classroom.id == class_id,
            Classroom.teacher_id == teacher.id
        )
    )
    classroom = result.scalar_one_or_none()

    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found or not owned by you"
        )

    # Get students in this classroom with their progress
    result = await db.execute(
        select(Student)
        .join(Student.enrollments)
        .where(Student.enrollments.any(classroom_id=class_id))
        .options(selectinload(Student.user))
    )
    students = result.scalars().all()

    # Build progress summary for each student
    student_progress = []
    for student in students:
        # Get task progress count
        result = await db.execute(
            select(StudentTaskProgress).where(
                StudentTaskProgress.student_id == student.id
            )
        )
        progress_records = result.scalars().all()

        total_tasks = len(progress_records)
        completed_tasks = sum(1 for p in progress_records if p.status == "completed")
        total_xp = sum(p.xp_earned for p in progress_records)

        student_progress.append({
            "student_id": str(student.id),
            "student_name": student.user.full_name,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "total_xp": total_xp,
            "last_activity": max([p.last_interaction_at for p in progress_records]) if progress_records else None
        })

    return {
        "classroom_id": str(class_id),
        "classroom_name": classroom.name,
        "students": student_progress
    }
