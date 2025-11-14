"""
Pydantic schemas for Curriculum models.
"""

from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.curriculum import ResourceType, SourceType


# =============================================================================
# LearningResource Schemas
# =============================================================================

class LearningResourceBase(BaseModel):
    """Base schema for LearningResource"""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    resource_type: ResourceType
    url: Optional[str] = Field(None, max_length=1000)
    file_path: Optional[str] = Field(None, max_length=1000)
    language: str = Field("en", max_length=10)
    subject: Optional[str] = Field(None, max_length=100)
    grade_min: Optional[int] = Field(None, ge=0, le=12)
    grade_max: Optional[int] = Field(None, ge=0, le=12)
    age_min: Optional[int] = Field(None, ge=0, le=18)
    age_max: Optional[int] = Field(None, ge=0, le=18)
    estimated_minutes: Optional[int] = Field(None, ge=0)
    source_type: SourceType
    source_attribution: Optional[str] = None
    source_url: Optional[str] = Field(None, max_length=1000)
    license_type: Optional[str] = Field(None, max_length=100)
    is_active: bool = True
    is_public: bool = False
    difficulty_level: Optional[str] = Field(None, max_length=50)
    resource_metadata: Optional[dict] = None


class LearningResourceCreate(LearningResourceBase):
    """Schema for creating a learning resource"""
    school_id: Optional[UUID] = None
    skill_ids: Optional[List[UUID]] = Field(default_factory=list, description="Skills this resource teaches")


class LearningResourceUpdate(BaseModel):
    """Schema for updating a learning resource"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    url: Optional[str] = None
    is_active: Optional[bool] = None
    difficulty_level: Optional[str] = None
    resource_metadata: Optional[dict] = None


class LearningResourceResponse(LearningResourceBase):
    """Schema for learning resource response"""
    id: UUID
    created_by_user_id: Optional[UUID]
    school_id: Optional[UUID]
    quality_score: Optional[int]
    view_count: int
    completion_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LearningResourceWithSkills(LearningResourceResponse):
    """Schema for learning resource with linked skills"""
    skill_ids: List[UUID] = Field(default_factory=list)

    class Config:
        from_attributes = True


# =============================================================================
# Resource Recommendations
# =============================================================================

class ResourceRecommendation(BaseModel):
    """AI-powered resource recommendation for a student"""
    resource_id: UUID
    title: str
    resource_type: str
    estimated_minutes: Optional[int]
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="How relevant to student's needs (0-1)")
    reason: str = Field(..., description="Why this resource is recommended")
    target_skills: List[str] = Field(default_factory=list, description="Skills this helps with")

    class Config:
        from_attributes = True


class StudentResourceRecommendations(BaseModel):
    """Complete set of recommendations for a student"""
    student_id: UUID
    recommendations: List[ResourceRecommendation] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
