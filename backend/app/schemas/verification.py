"""
Pydantic schemas for Verification model.
"""

from uuid import UUID
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

from app.models.verification import VerificationSource, VerificationStatus


# ============================================================================
# Verification Schemas
# ============================================================================

class VerificationBase(BaseModel):
    """Base schema for Verification."""
    skill_id: UUID = Field(..., description="ID of the skill being verified")
    source: VerificationSource = Field(..., description="Source of verification")
    score: Optional[float] = Field(None, ge=0, le=100, description="Score or confidence from verification source (0-100)")
    evidence: Optional[dict[str, Any]] = Field(None, description="Evidence supporting this verification")
    notes: Optional[str] = Field(None, description="Additional notes or comments")
    expires_at: Optional[datetime] = Field(None, description="Expiration date for this verification")


class VerificationCreate(VerificationBase):
    """Schema for creating a verification."""
    student_id: UUID = Field(..., description="ID of the student being verified")
    module_id: Optional[UUID] = Field(None, description="ID of the module (if applicable)")
    task_id: Optional[UUID] = Field(None, description="ID of the task (if applicable)")
    verified_by_user_id: Optional[UUID] = Field(None, description="ID of the user who verified (for teacher reviews)")


class VerificationUpdate(BaseModel):
    """Schema for updating a verification."""
    status: Optional[VerificationStatus] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    evidence: Optional[dict[str, Any]] = None
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None


class VerificationResponse(VerificationBase):
    """Schema for verification response."""
    id: UUID
    student_id: UUID
    module_id: Optional[UUID]
    task_id: Optional[UUID]
    status: VerificationStatus
    verified_by_user_id: Optional[UUID]
    verified_at: Optional[datetime]
    is_valid: bool  # Computed property
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VerificationWithDetails(VerificationResponse):
    """Schema for verification with skill details."""
    skill_name: str = Field(..., description="Name of the verified skill")
    skill_category: str = Field(..., description="Category of the verified skill")

    class Config:
        from_attributes = True


# ============================================================================
# Verification Request (for teachers/AI)
# ============================================================================

class VerificationRequest(BaseModel):
    """Request to create a verification."""
    student_id: UUID
    skill_id: UUID
    source: VerificationSource
    score: Optional[float] = Field(None, ge=0, le=100, description="Assessment score")
    notes: Optional[str] = None
    evidence: Optional[dict[str, Any]] = None

    # Optional context
    module_id: Optional[UUID] = None
    task_id: Optional[UUID] = None


# ============================================================================
# Skill Verification Summary
# ============================================================================

class SkillVerificationSummary(BaseModel):
    """Summary of verifications for a specific skill."""
    skill_id: UUID
    skill_name: str
    total_verifications: int = Field(..., description="Total number of verifications")
    verified_count: int = Field(..., description="Number of verified confirmations")
    pending_count: int = Field(..., description="Number of pending verifications")
    rejected_count: int = Field(..., description="Number of rejected verifications")
    latest_verification: Optional[VerificationResponse] = None
    average_score: Optional[float] = Field(None, description="Average score across all verifications")
    verification_sources: list[str] = Field(default_factory=list, description="List of verification sources used")

    class Config:
        from_attributes = True


# ============================================================================
# Student Verification Profile
# ============================================================================

class StudentVerificationProfile(BaseModel):
    """Complete verification profile for a student."""
    student_id: UUID
    total_verifications: int = Field(..., description="Total verifications received")
    verified_skills_count: int = Field(..., description="Number of verified skills")
    pending_verifications_count: int = Field(..., description="Number of pending verifications")
    verifications: list[VerificationWithDetails] = Field(default_factory=list, description="All verifications")

    class Config:
        from_attributes = True
