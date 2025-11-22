"""
School and Classroom Models
"""

from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
from datetime import datetime


class School(Base):
    """School/Institution model"""

    __tablename__ = "schools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    curriculum_type = Column(String(50), nullable=False)  # INDIAN_CBSE, UK_NATIONAL, etc.

    # Contact info
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(20), nullable=True)

    # Admin
    admin_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Metadata
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    students = relationship("Student", back_populates="school")
    teachers = relationship("Teacher", back_populates="school")
    classrooms = relationship("Classroom", back_populates="school")


class Classroom(Base):
    """Classroom model for organizing students"""

    __tablename__ = "classrooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=False)

    name = Column(String(255), nullable=False)
    grade_level = Column(Integer, nullable=False)
    subject = Column(String(50), nullable=False)

    # Student IDs (could also be a junction table, but ARRAY is simpler)
    student_ids = Column(ARRAY(String), default=list)

    # Schedule
    academic_year = Column(String(20), nullable=True)  # e.g., "2024-2025"

    # Metadata
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    school = relationship("School", back_populates="classrooms")
    teacher = relationship("Teacher", back_populates="classrooms")
