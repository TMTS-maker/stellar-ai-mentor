"""Subject-related Pydantic schemas"""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class SubjectBase(BaseModel):
    """Base subject schema"""
    name: str
    description: Optional[str] = None


class SubjectCreate(SubjectBase):
    """Schema for subject creation"""
    school_id: UUID


class SubjectResponse(SubjectBase):
    """Schema for subject response"""
    id: UUID
    school_id: UUID

    class Config:
        from_attributes = True
