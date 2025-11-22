"""
Pydantic Schemas for Authentication

Request and response models for auth endpoints
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import uuid


# ============================================================================
# Request Schemas
# ============================================================================

class LoginRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str = Field(..., min_length=8)


class RegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=255)
    user_type: str = Field(..., pattern="^(student|teacher|parent)$")

    # Student-specific fields
    school_id: Optional[uuid.UUID] = None
    grade_level: Optional[int] = Field(None, ge=1, le=12)
    age: Optional[int] = Field(None, ge=5, le=100)
    curriculum_id: Optional[uuid.UUID] = None

    # Teacher-specific fields
    subjects: Optional[list[str]] = None
    grade_levels: Optional[list[int]] = None

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('grade_level')
    def validate_grade_for_student(cls, v, values):
        if values.get('user_type') == 'student' and v is None:
            raise ValueError('Grade level is required for students')
        return v

    @validator('subjects')
    def validate_subjects_for_teacher(cls, v, values):
        if values.get('user_type') == 'teacher' and not v:
            raise ValueError('Subjects are required for teachers')
        return v


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class PasswordChangeRequest(BaseModel):
    """Password change request"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    confirm_new_password: str = Field(..., min_length=8, max_length=100)

    @validator('confirm_new_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('New passwords do not match')
        return v


# ============================================================================
# Response Schemas
# ============================================================================

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class UserResponse(BaseModel):
    """User information response"""
    id: uuid.UUID
    email: str
    full_name: str
    user_type: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class StudentResponse(UserResponse):
    """Student-specific response"""
    school_id: Optional[uuid.UUID]
    grade_level: int
    age: Optional[int]
    total_xp: int
    current_level: int
    h_pem_level: float

    class Config:
        from_attributes = True


class TeacherResponse(UserResponse):
    """Teacher-specific response"""
    school_id: uuid.UUID
    subjects: list[str]
    grade_levels: list[int]

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Complete login response with token and user info"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: UserResponse


class RegisterResponse(BaseModel):
    """Registration success response"""
    message: str
    user_id: uuid.UUID
    email: str


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    detail: Optional[str] = None
