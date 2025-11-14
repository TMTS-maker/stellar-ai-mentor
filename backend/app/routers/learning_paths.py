"""
API router for Learning Paths and Modules (LVO - LEARN phase).
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_db
from app.auth import get_current_user, require_role
from app.models.user import User
from app.models.student import Student
from app.models.learning_path import LearningPath, LearningModule, StudentLearningPath
from app.schemas.learning_path import (
    LearningPathCreate, LearningPathUpdate, LearningPathResponse, LearningPathWithModules,
    LearningModuleCreate, LearningModuleUpdate, LearningModuleResponse,
    StudentLearningPathWithDetails,
    NextTaskRecommendation
)
from app.services.learning_paths import LearningPathService


router = APIRouter(prefix="/learning-paths", tags=["Learning Paths"])


# ============================================================================
# Learning Paths
# ============================================================================

@router.post("", response_model=LearningPathResponse, status_code=status.HTTP_201_CREATED)
async def create_learning_path(
    path_data: LearningPathCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("school_admin", "teacher"))
):
    """Create a new learning path. Only school_admin or teacher can create."""
    learning_path = LearningPath(**path_data.model_dump())
    db.add(learning_path)
    await db.commit()
    await db.refresh(learning_path)
    return learning_path


@router.get("", response_model=list[LearningPathResponse])
async def list_learning_paths(
    is_active: bool | None = None,
    difficulty: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all learning paths, optionally filtered."""
    query = select(LearningPath)

    if is_active is not None:
        query = query.where(LearningPath.is_active == is_active)
    if difficulty:
        query = query.where(LearningPath.difficulty == difficulty)

    query = query.offset(skip).limit(limit).order_by(LearningPath.name.asc())

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{path_id}", response_model=LearningPathWithModules)
async def get_learning_path(
    path_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a learning path with all its modules."""
    result = await db.execute(
        select(LearningPath)
        .options(selectinload(LearningPath.modules))
        .where(LearningPath.id == path_id)
    )
    learning_path = result.scalar_one_or_none()

    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")

    return learning_path


@router.put("/{path_id}", response_model=LearningPathResponse)
async def update_learning_path(
    path_id: UUID,
    path_data: LearningPathUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("school_admin", "teacher"))
):
    """Update a learning path."""
    result = await db.execute(select(LearningPath).where(LearningPath.id == path_id))
    learning_path = result.scalar_one_or_none()

    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")

    for field, value in path_data.model_dump(exclude_unset=True).items():
        setattr(learning_path, field, value)

    await db.commit()
    await db.refresh(learning_path)
    return learning_path


# ============================================================================
# Learning Modules
# ============================================================================

@router.post("/modules", response_model=LearningModuleResponse, status_code=status.HTTP_201_CREATED)
async def create_learning_module(
    module_data: LearningModuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("school_admin", "teacher"))
):
    """Create a new learning module within a path."""
    module = LearningModule(**module_data.model_dump())
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module


@router.get("/modules/{module_id}", response_model=LearningModuleResponse)
async def get_learning_module(
    module_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific learning module."""
    result = await db.execute(select(LearningModule).where(LearningModule.id == module_id))
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    return module


@router.put("/modules/{module_id}", response_model=LearningModuleResponse)
async def update_learning_module(
    module_id: UUID,
    module_data: LearningModuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("school_admin", "teacher"))
):
    """Update a learning module."""
    result = await db.execute(select(LearningModule).where(LearningModule.id == module_id))
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    for field, value in module_data.model_dump(exclude_unset=True).items():
        setattr(module, field, value)

    await db.commit()
    await db.refresh(module)
    return module


# ============================================================================
# Student Learning Paths
# ============================================================================

@router.get("/me/paths", response_model=list[StudentLearningPathWithDetails])
async def get_my_learning_paths(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    """Get current student's enrolled learning paths."""
    # Get student
    student_result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # Get student learning paths
    paths_result = await db.execute(
        select(StudentLearningPath, LearningPath)
        .join(LearningPath, StudentLearningPath.learning_path_id == LearningPath.id)
        .where(StudentLearningPath.student_id == student.id)
        .order_by(StudentLearningPath.created_at.desc())
    )
    paths_data = paths_result.all()

    result = []
    for student_path, learning_path in paths_data:
        result.append(StudentLearningPathWithDetails(
            id=student_path.id,
            student_id=student_path.student_id,
            learning_path_id=student_path.learning_path_id,
            status=student_path.status,
            progress_percentage=student_path.progress_percentage,
            started_at=student_path.started_at,
            completed_at=student_path.completed_at,
            created_at=student_path.created_at,
            updated_at=student_path.updated_at,
            learning_path=LearningPathResponse.model_validate(learning_path),
            current_module=None  # TODO: Get current module if needed
        ))

    return result


@router.post("/{path_id}/enroll", response_model=StudentLearningPathWithDetails)
async def enroll_in_learning_path(
    path_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    """Enroll current student in a learning path."""
    # Get student
    student_result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # Check if path exists
    path_result = await db.execute(
        select(LearningPath).where(LearningPath.id == path_id)
    )
    learning_path = path_result.scalar_one_or_none()

    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")

    if not learning_path.is_active:
        raise HTTPException(status_code=400, detail="This learning path is not active")

    # Check if already enrolled
    existing_result = await db.execute(
        select(StudentLearningPath)
        .where(
            (StudentLearningPath.student_id == student.id) &
            (StudentLearningPath.learning_path_id == path_id)
        )
    )
    if existing_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already enrolled in this path")

    # Create enrollment
    from app.models.learning_path import PathStatus
    from datetime import datetime

    student_path = StudentLearningPath(
        student_id=student.id,
        learning_path_id=path_id,
        status=PathStatus.IN_PROGRESS,
        progress_percentage=0,
        started_at=datetime.utcnow()
    )

    db.add(student_path)
    await db.commit()
    await db.refresh(student_path)

    return StudentLearningPathWithDetails(
        id=student_path.id,
        student_id=student_path.student_id,
        learning_path_id=student_path.learning_path_id,
        status=student_path.status,
        progress_percentage=student_path.progress_percentage,
        started_at=student_path.started_at,
        completed_at=student_path.completed_at,
        created_at=student_path.created_at,
        updated_at=student_path.updated_at,
        learning_path=LearningPathResponse.model_validate(learning_path),
        current_module=None
    )


# ============================================================================
# AI-Powered Next Task Recommendation
# ============================================================================

@router.get("/me/next-task", response_model=NextTaskRecommendation)
async def get_next_best_task(
    use_ai: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    """
    Get AI-powered recommendation for the next best task for the current student.

    This is the core "LEARN" feature of the LVO architecture.
    The AI analyzes the student's skill profile, learning progress, and knowledge gaps
    to recommend the most appropriate next task.

    Args:
        use_ai: Whether to use AI for reasoning (default True). If False, uses rule-based recommendation.
    """
    # Get student
    student_result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # Get recommendation
    recommendation = await LearningPathService.get_next_best_task_for_student(
        student_id=student.id,
        db=db,
        use_ai=use_ai
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="No suitable tasks found. Try enrolling in a learning path or complete more tasks to build your profile."
        )

    return recommendation
