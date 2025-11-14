"""Student-related Pydantic schemas"""
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.schemas.task import TaskProgressResponse
from app.schemas.gamification import XPResponse


class StudentBase(BaseModel):
    """Base student schema"""
    grade_level: Optional[str] = None


class StudentCreate(BaseModel):
    """Schema for student creation"""
    email: EmailStr
    full_name: str
    password: str
    school_id: UUID
    grade_level: Optional[str] = None


class StudentBulkCreate(BaseModel):
    """Schema for bulk student creation"""
    students: List[dict]  # List of {email, full_name, password, grade_level}


class StudentResponse(StudentBase):
    """Schema for student response"""
    id: UUID
    user_id: UUID
    school_id: UUID

    class Config:
        from_attributes = True


class StudentDashboard(BaseModel):
    """Schema for student dashboard data"""
    student: StudentResponse
    xp: XPResponse
    assigned_tasks: List[TaskProgressResponse]
    recent_sessions: List[dict]  # Simplified for now
