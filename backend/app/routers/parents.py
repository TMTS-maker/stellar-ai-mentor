"""Parents router"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import get_current_user, require_role
from app.db import get_db
from app.models.user import User
from app.models.parent import Parent, ParentStudent
from app.models.student import Student
from app.schemas.parent import ParentResponse, ChildLinkRequest
from app.services.gamification import GamificationService

router = APIRouter(prefix="/parents", tags=["Parents"])


@router.post("/link-child", status_code=status.HTTP_201_CREATED)
async def link_child(
    link_request: ChildLinkRequest,
    current_user: User = Depends(require_role("parent")),
    db: AsyncSession = Depends(get_db)
):
    """Link parent to a child (student)"""
    # Get parent profile
    result = await db.execute(
        select(Parent).where(Parent.user_id == current_user.id)
    )
    parent = result.scalar_one_or_none()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent profile not found"
        )

    # Find student by email
    result = await db.execute(
        select(User).where(User.email == link_request.student_email)
    )
    student_user = result.scalar_one_or_none()

    if not student_user or student_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == student_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    # Check if link already exists
    result = await db.execute(
        select(ParentStudent).where(
            ParentStudent.parent_id == parent.id,
            ParentStudent.student_id == student.id
        )
    )
    existing_link = result.scalar_one_or_none()

    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Child already linked"
        )

    # Create link
    link = ParentStudent(
        parent_id=parent.id,
        student_id=student.id
    )
    db.add(link)
    await db.commit()

    return {"status": "linked", "student_id": str(student.id)}


@router.get("/me/children")
async def get_my_children(
    current_user: User = Depends(require_role("parent")),
    db: AsyncSession = Depends(get_db)
):
    """Get all children linked to this parent"""
    # Get parent profile
    result = await db.execute(
        select(Parent).where(Parent.user_id == current_user.id)
    )
    parent = result.scalar_one_or_none()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent profile not found"
        )

    # Get linked students
    result = await db.execute(
        select(Student)
        .join(ParentStudent, ParentStudent.student_id == Student.id)
        .where(ParentStudent.parent_id == parent.id)
        .options(selectinload(Student.user))
    )
    students = result.scalars().all()

    # Build response with summary for each child
    children_data = []
    for student in students:
        xp_data = await GamificationService.get_xp_data(student.id, db)

        children_data.append({
            "student_id": str(student.id),
            "name": student.user.full_name,
            "email": student.user.email,
            "grade_level": student.grade_level,
            "xp": xp_data.dict()
        })

    return {"children": children_data}


@router.get("/me/overview")
async def get_parent_overview(
    current_user: User = Depends(require_role("parent")),
    db: AsyncSession = Depends(get_db)
):
    """Get overview of all children's progress"""
    # Get parent profile
    result = await db.execute(
        select(Parent).where(Parent.user_id == current_user.id)
    )
    parent = result.scalar_one_or_none()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent profile not found"
        )

    # Get linked students
    result = await db.execute(
        select(Student)
        .join(ParentStudent, ParentStudent.student_id == Student.id)
        .where(ParentStudent.parent_id == parent.id)
        .options(selectinload(Student.user))
    )
    students = result.scalars().all()

    # Build detailed overview
    children_overview = []
    for student in students:
        xp_data = await GamificationService.get_xp_data(student.id, db)
        plant_data = await GamificationService.get_plant_progress(student.id, db)
        streak_data = await GamificationService.get_streaks(student.id, db)

        # Get open tasks count
        result = await db.execute(
            select(Student)
            .where(Student.id == student.id)
            .options(selectinload(Student.task_progress))
        )
        student_with_progress = result.scalar_one()
        open_tasks = sum(1 for p in student_with_progress.task_progress if p.status != "completed")

        children_overview.append({
            "student_id": str(student.id),
            "name": student.user.full_name,
            "xp": xp_data.dict(),
            "plant": plant_data.dict(),
            "streaks": streak_data.dict(),
            "open_tasks": open_tasks
        })

    return {"children": children_overview}
