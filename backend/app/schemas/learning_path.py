"""
Pydantic schemas for LearningPath and LearningModule models.
"""

from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.learning_path import PathStatus, ModuleStatus


# ============================================================================
# LearningModule Schemas
# ============================================================================

class LearningModuleBase(BaseModel):
    """Base schema for LearningModule."""
    name: str = Field(..., min_length=1, max_length=255, description="Module name")
    description: Optional[str] = Field(None, description="Module description")
    order: int = Field(..., ge=1, description="Order within the learning path")
    skill_ids: Optional[list[str]] = Field(None, description="IDs of skills this module teaches")
    task_ids: Optional[list[str]] = Field(None, description="IDs of tasks in this module")
    completion_threshold: int = Field(70, ge=0, le=100, description="Minimum score to complete module (0-100)")
    estimated_minutes: Optional[int] = Field(None, ge=0, description="Estimated time to complete in minutes")


class LearningModuleCreate(LearningModuleBase):
    """Schema for creating a learning module."""
    learning_path_id: UUID = Field(..., description="ID of the parent learning path")


class LearningModuleUpdate(BaseModel):
    """Schema for updating a learning module."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    order: Optional[int] = Field(None, ge=1)
    skill_ids: Optional[list[str]] = None
    task_ids: Optional[list[str]] = None
    completion_threshold: Optional[int] = Field(None, ge=0, le=100)
    estimated_minutes: Optional[int] = Field(None, ge=0)


class LearningModuleResponse(LearningModuleBase):
    """Schema for learning module response."""
    id: UUID
    learning_path_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# LearningPath Schemas
# ============================================================================

class LearningPathBase(BaseModel):
    """Base schema for LearningPath."""
    name: str = Field(..., min_length=1, max_length=255, description="Learning path name")
    description: Optional[str] = Field(None, description="Learning path description")
    recommended_age_min: Optional[int] = Field(None, ge=0, le=18, description="Minimum recommended age")
    recommended_age_max: Optional[int] = Field(None, ge=0, le=18, description="Maximum recommended age")
    estimated_hours: Optional[int] = Field(None, ge=0, description="Estimated completion time in hours")
    difficulty: Optional[str] = Field(None, description="Difficulty level (beginner, intermediate, advanced)")
    prerequisites: Optional[list[str]] = Field(None, description="IDs of prerequisite learning paths")
    is_active: bool = Field(True, description="Whether this path is currently active/published")


class LearningPathCreate(LearningPathBase):
    """Schema for creating a learning path."""
    pass


class LearningPathUpdate(BaseModel):
    """Schema for updating a learning path."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    recommended_age_min: Optional[int] = Field(None, ge=0, le=18)
    recommended_age_max: Optional[int] = Field(None, ge=0, le=18)
    estimated_hours: Optional[int] = Field(None, ge=0)
    difficulty: Optional[str] = None
    prerequisites: Optional[list[str]] = None
    is_active: Optional[bool] = None


class LearningPathResponse(LearningPathBase):
    """Schema for learning path response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LearningPathWithModules(LearningPathResponse):
    """Schema for learning path with all its modules."""
    modules: list[LearningModuleResponse] = Field(default_factory=list, description="Modules in this path")

    class Config:
        from_attributes = True


# ============================================================================
# StudentModule Schemas
# ============================================================================

class StudentModuleBase(BaseModel):
    """Base schema for StudentModule."""
    status: ModuleStatus = Field(..., description="Current status of the module")
    score: Optional[float] = Field(None, ge=0, le=100, description="Score achieved (0-100)")
    tasks_completed: int = Field(0, ge=0, description="Number of tasks completed")
    tasks_total: int = Field(0, ge=0, description="Total number of tasks")


class StudentModuleResponse(StudentModuleBase):
    """Schema for student module response."""
    id: UUID
    student_id: UUID
    module_id: UUID
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentModuleWithDetails(StudentModuleResponse):
    """Schema for student module with full module details."""
    module: LearningModuleResponse

    class Config:
        from_attributes = True


# ============================================================================
# StudentLearningPath Schemas
# ============================================================================

class StudentLearningPathBase(BaseModel):
    """Base schema for StudentLearningPath."""
    status: PathStatus = Field(..., description="Current status of the path")
    progress_percentage: int = Field(0, ge=0, le=100, description="Progress percentage (0-100)")


class StudentLearningPathResponse(StudentLearningPathBase):
    """Schema for student learning path response."""
    id: UUID
    student_id: UUID
    learning_path_id: UUID
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentLearningPathWithDetails(StudentLearningPathResponse):
    """Schema for student learning path with full details."""
    learning_path: LearningPathResponse
    current_module: Optional[StudentModuleWithDetails] = None

    class Config:
        from_attributes = True


# ============================================================================
# Next Best Task Recommendation
# ============================================================================

class NextTaskRecommendation(BaseModel):
    """AI-powered recommendation for the next best task."""
    task_id: UUID = Field(..., description="ID of the recommended task")
    task_title: str = Field(..., description="Title of the task")
    task_description: Optional[str] = Field(None, description="Description of the task")
    module_id: Optional[UUID] = Field(None, description="ID of the associated module")
    module_name: Optional[str] = Field(None, description="Name of the associated module")
    learning_path_id: Optional[UUID] = Field(None, description="ID of the associated learning path")
    learning_path_name: Optional[str] = Field(None, description="Name of the associated learning path")
    skill_ids: list[str] = Field(default_factory=list, description="Skills this task will help develop")
    xp_reward: int = Field(..., description="XP reward for completing this task")
    estimated_minutes: Optional[int] = Field(None, description="Estimated time to complete")
    reason: str = Field(..., description="AI-generated reason why this task is recommended")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this recommendation (0-1)")

    class Config:
        from_attributes = True
