"""
Pydantic schemas for Skill and SkillScore models.
"""

from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.skill import SkillCategory


# ============================================================================
# Skill Schemas
# ============================================================================

class SkillBase(BaseModel):
    """Base schema for Skill."""
    name: str = Field(..., min_length=1, max_length=255, description="Name of the skill")
    description: Optional[str] = Field(None, description="Detailed description of the skill")
    category: SkillCategory = Field(..., description="Skill category")
    level: Optional[str] = Field(None, max_length=50, description="Difficulty or progression level (e.g., A1, A2, Level 1)")
    age_group_min: Optional[int] = Field(None, ge=0, le=18, description="Minimum recommended age")
    age_group_max: Optional[int] = Field(None, ge=0, le=18, description="Maximum recommended age")


class SkillCreate(SkillBase):
    """Schema for creating a new skill."""
    pass


class SkillUpdate(BaseModel):
    """Schema for updating a skill."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[SkillCategory] = None
    level: Optional[str] = Field(None, max_length=50)
    age_group_min: Optional[int] = Field(None, ge=0, le=18)
    age_group_max: Optional[int] = Field(None, ge=0, le=18)


class SkillResponse(SkillBase):
    """Schema for skill response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# SkillScore Schemas
# ============================================================================

class SkillScoreBase(BaseModel):
    """Base schema for SkillScore."""
    skill_id: UUID = Field(..., description="ID of the skill being scored")
    score: float = Field(..., ge=0, le=100, description="Proficiency score (0-100)")
    confidence: float = Field(0.5, ge=0.0, le=1.0, description="Confidence level in this score (0-1)")


class SkillScoreCreate(SkillScoreBase):
    """Schema for creating a new skill score."""
    student_id: UUID = Field(..., description="ID of the student")


class SkillScoreUpdate(BaseModel):
    """Schema for updating a skill score."""
    score: Optional[float] = Field(None, ge=0, le=100)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    last_practiced_at: Optional[datetime] = None


class SkillScoreResponse(SkillScoreBase):
    """Schema for skill score response."""
    id: UUID
    student_id: UUID
    assessment_count: int
    last_practiced_at: Optional[datetime]
    proficiency_level: str  # Computed property: Beginner, Developing, Proficient, Advanced
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SkillScoreWithSkill(SkillScoreResponse):
    """Schema for skill score with full skill details."""
    skill: SkillResponse

    class Config:
        from_attributes = True


# ============================================================================
# Student Skills Profile
# ============================================================================

class StudentSkillsProfile(BaseModel):
    """Complete skills profile for a student."""
    student_id: UUID
    total_skills: int = Field(..., description="Total number of skills tracked")
    mastered_skills: int = Field(..., description="Skills with score >= 80")
    proficient_skills: int = Field(..., description="Skills with score 60-79")
    developing_skills: int = Field(..., description="Skills with score 30-59")
    beginner_skills: int = Field(..., description="Skills with score < 30")
    skill_scores: list[SkillScoreWithSkill] = Field(default_factory=list, description="All skill scores with details")

    class Config:
        from_attributes = True
