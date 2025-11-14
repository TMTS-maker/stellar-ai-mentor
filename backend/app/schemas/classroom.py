"""Classroom-related Pydantic schemas"""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ClassroomBase(BaseModel):
    """Base classroom schema"""
    name: str
    grade_level: Optional[str] = None


class ClassroomCreate(ClassroomBase):
    """Schema for classroom creation"""
    school_id: UUID
    teacher_id: UUID


class ClassroomResponse(ClassroomBase):
    """Schema for classroom response"""
    id: UUID
    school_id: UUID
    teacher_id: UUID

    class Config:
        from_attributes = True
