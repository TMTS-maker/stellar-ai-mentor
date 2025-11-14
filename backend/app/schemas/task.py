"""Task-related Pydantic schemas"""
from typing import Optional, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    """Base task schema"""
    title: str
    description: Optional[str] = None
    xp_reward: int = 0
    scenario_type: Optional[str] = None


class TaskCreate(TaskBase):
    """Schema for task creation"""
    subject_id: Optional[UUID] = None
    learning_path_id: Optional[UUID] = None
    metadata: Optional[dict] = None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: UUID
    subject_id: Optional[UUID] = None
    learning_path_id: Optional[UUID] = None
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True


class TaskProgressResponse(BaseModel):
    """Schema for task progress response"""
    id: UUID
    task_id: UUID
    task: TaskResponse
    status: TaskStatus
    score: Optional[int] = None
    xp_earned: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_interaction_at: datetime

    class Config:
        from_attributes = True
