"""
User and User-related Models

Includes: User, Student, Teacher, Parent
"""
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, ForeignKey, Float, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
from datetime import datetime


class User(Base):
    """Base user model for all user types"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    user_type = Column(String(20), nullable=False)  # 'student', 'teacher', 'parent', 'admin'
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False)
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    parent_profile = relationship("Parent", back_populates="user", uselist=False)


class Student(Base):
    """Student profile extending User"""
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=True)
    grade_level = Column(Integer, nullable=False)
    age = Column(Integer)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    curriculum_id = Column(UUID(as_uuid=True), ForeignKey("curricula.id"), nullable=True)

    # Gamification fields
    h_pem_level = Column(Float, default=0.0)
    total_xp = Column(Integer, default=0)
    current_level = Column(Integer, default=1)

    # Blockchain
    stellar_wallet_address = Column(String(56), nullable=True, unique=True)

    # Preferences
    preferred_mentor_id = Column(String(50), nullable=True)
    learning_style = Column(String(50), nullable=True)  # 'visual', 'auditory', 'kinesthetic'

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="student_profile", foreign_keys=[id])
    school = relationship("School", back_populates="students")
    curriculum = relationship("Curriculum", back_populates="students")
    skill_progress = relationship("StudentSkillProgress", back_populates="student")
    badges = relationship("StudentBadge", back_populates="student")
    xp_logs = relationship("StudentXPLog", back_populates="student")
    streak = relationship("StudentStreak", back_populates="student", uselist=False)
    sessions = relationship("ConversationSession", back_populates="student")


class Teacher(Base):
    """Teacher profile extending User"""
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    subjects = Column(ARRAY(String), nullable=False)
    grade_levels = Column(ARRAY(Integer), nullable=False)

    # Professional info
    qualifications = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="teacher_profile", foreign_keys=[id])
    school = relationship("School", back_populates="teachers")
    classrooms = relationship("Classroom", back_populates="teacher")


class Parent(Base):
    """Parent profile extending User"""
    __tablename__ = "parents"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    phone_number = Column(String(20), nullable=True)

    # Relationships
    user = relationship("User", back_populates="parent_profile", foreign_keys=[id])
    children = relationship("Student", foreign_keys=[Student.parent_id])
