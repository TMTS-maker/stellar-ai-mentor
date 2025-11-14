"""Teacher-related Pydantic schemas"""
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional


class TeacherBase(BaseModel):
    """Base teacher schema"""
    pass


class TeacherCreate(BaseModel):
    """Schema for teacher creation"""
    email: EmailStr
    full_name: str
    password: str
    school_id: UUID


class TeacherResponse(TeacherBase):
    """Schema for teacher response"""
    id: UUID
    user_id: UUID
    school_id: UUID

    class Config:
        from_attributes = True
