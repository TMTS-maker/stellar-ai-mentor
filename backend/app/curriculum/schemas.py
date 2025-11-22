"""
Curriculum Pydantic Schemas

For API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CurriculumResponse(BaseModel):
    """Curriculum response schema."""
    id: int
    code: str
    name: str
    country_code: str
    provider_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CurriculumVersionResponse(BaseModel):
    """Curriculum version response schema."""
    id: int
    curriculum_id: int
    version_code: str
    version_name: Optional[str]
    is_current: bool
    effective_from: Optional[datetime]

    class Config:
        from_attributes = True


class SubjectResponse(BaseModel):
    """Subject response schema."""
    id: int
    code: str
    name: str
    description: Optional[str]
    recommended_mentor_id: Optional[str]

    class Config:
        from_attributes = True


class LearningObjectiveResponse(BaseModel):
    """Learning objective response schema."""
    id: int
    code: str
    description: str
    cognitive_level: Optional[str]
    lvo_phase_emphasis: Optional[str]

    class Config:
        from_attributes = True


class IngestCurriculumRequest(BaseModel):
    """Request to ingest a curriculum."""
    provider_type: str = Field(..., description="Provider type: indian, uk, us")
    curriculum_code: str = Field(..., description="Curriculum code: CBSE, UK_NATIONAL, COMMON_CORE")
    version_code: Optional[str] = Field(None, description="Optional version code")


class CompetencyRecordResponse(BaseModel):
    """Competency record response schema."""
    id: int
    student_id: int
    objective_id: int
    status: str
    mastery_level: int
    practice_count: int
    last_practiced_at: Optional[datetime]
    evaluation_score: Optional[int]
    started_at: Optional[datetime]
    mastered_at: Optional[datetime]

    class Config:
        from_attributes = True


class UpdateCompetencyRequest(BaseModel):
    """Request to update student competency."""
    objective_id: int = Field(..., description="Learning objective ID")
    mastery_level: int = Field(..., ge=0, le=100, description="Mastery level 0-100")
    status: str = Field(..., description="Status: not_started, in_progress, mastered, needs_review")
    evaluation_score: Optional[int] = Field(None, ge=0, le=100, description="Assessment score 0-100")
