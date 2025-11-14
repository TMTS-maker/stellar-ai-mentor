"""Tasks router"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user, require_role
from app.db import get_db
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(require_role("teacher", "school_admin")),
    db: AsyncSession = Depends(get_db)
):
    """Create a new learning task"""
    task = Task(
        title=task_data.title,
        description=task_data.description,
        subject_id=task_data.subject_id,
        learning_path_id=task_data.learning_path_id,
        xp_reward=task_data.xp_reward,
        scenario_type=task_data.scenario_type,
        task_metadata=task_data.task_metadata
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get task details"""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    subject_id: UUID = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all tasks, optionally filtered by subject"""
    query = select(Task)

    if subject_id:
        query = query.where(Task.subject_id == subject_id)

    result = await db.execute(query)
    tasks = result.scalars().all()

    return tasks
