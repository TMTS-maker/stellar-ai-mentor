"""Parent-related Pydantic schemas"""
from typing import List
from uuid import UUID
from pydantic import BaseModel, EmailStr


class ParentBase(BaseModel):
    """Base parent schema"""
    pass


class ParentCreate(BaseModel):
    """Schema for parent creation"""
    email: EmailStr
    full_name: str
    password: str


class ParentResponse(ParentBase):
    """Schema for parent response"""
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class ChildLinkRequest(BaseModel):
    """Schema for linking parent to child"""
    student_email: str
