"""School-related Pydantic schemas"""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class SchoolBase(BaseModel):
    """Base school schema"""
    name: str
    address: Optional[str] = None


class SchoolCreate(SchoolBase):
    """Schema for school creation"""
    pass


class SchoolResponse(SchoolBase):
    """Schema for school response"""
    id: UUID
    admin_user_id: UUID

    class Config:
        from_attributes = True
