"""Schools management router"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user, require_role
from app.db import get_db
from app.models.user import User, UserRole
from app.models.school import School
from app.models.teacher import Teacher
from app.models.classroom import Classroom
from app.models.subject import Subject
from app.schemas.school import SchoolCreate, SchoolResponse
from app.schemas.teacher import TeacherCreate, TeacherResponse
from app.schemas.classroom import ClassroomCreate, ClassroomResponse
from app.schemas.subject import SubjectCreate, SubjectResponse
from app.auth import get_password_hash

router = APIRouter(prefix="/schools", tags=["Schools"])


@router.post("", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def create_school(
    school_data: SchoolCreate,
    current_user: User = Depends(require_role("school_admin")),
    db: AsyncSession = Depends(get_db)
):
    """Create a new school (school admins only)"""
    school = School(
        name=school_data.name,
        address=school_data.address,
        admin_user_id=current_user.id
    )
    db.add(school)
    await db.commit()
    await db.refresh(school)

    return school


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get school information"""
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )

    return school


@router.post("/{school_id}/teachers", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    school_id: UUID,
    teacher_data: TeacherCreate,
    current_user: User = Depends(require_role("school_admin")),
    db: AsyncSession = Depends(get_db)
):
    """Create a new teacher account"""
    # Verify school exists and user is admin of this school
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()

    if not school or school.admin_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add teachers to this school"
        )

    # Check if email already exists
    result = await db.execute(select(User).where(User.email == teacher_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create teacher user
    user = User(
        email=teacher_data.email,
        password_hash=get_password_hash(teacher_data.password),
        full_name=teacher_data.full_name,
        role=UserRole.TEACHER
    )
    db.add(user)
    await db.flush()

    # Create teacher profile
    teacher = Teacher(
        user_id=user.id,
        school_id=school_id
    )
    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)

    return teacher


@router.post("/{school_id}/classes", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED)
async def create_classroom(
    school_id: UUID,
    classroom_data: ClassroomCreate,
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Create a new classroom"""
    classroom = Classroom(
        school_id=school_id,
        teacher_id=classroom_data.teacher_id,
        name=classroom_data.name,
        grade_level=classroom_data.grade_level
    )
    db.add(classroom)
    await db.commit()
    await db.refresh(classroom)

    return classroom


@router.post("/{school_id}/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    school_id: UUID,
    subject_data: SubjectCreate,
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Create a new subject"""
    subject = Subject(
        school_id=school_id,
        name=subject_data.name,
        description=subject_data.description
    )
    db.add(subject)
    await db.commit()
    await db.refresh(subject)

    return subject
