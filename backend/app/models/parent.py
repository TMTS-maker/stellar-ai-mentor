"""Parent model and parent-student relationship"""
import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class Parent(Base):
    """Parent profile model"""
    __tablename__ = "parents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="parent_profile")
    child_links = relationship("ParentStudent", back_populates="parent")

    def __repr__(self):
        return f"<Parent(id={self.id}, user_id={self.user_id})>"


class ParentStudent(Base):
    """Many-to-many relationship between parents and students"""
    __tablename__ = "parent_students"

    parent_id = Column(UUID(as_uuid=True), ForeignKey("parents.id"), primary_key=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), primary_key=True)

    # Relationships
    parent = relationship("Parent", back_populates="child_links")
    student = relationship("Student", back_populates="parent_links")

    def __repr__(self):
        return f"<ParentStudent(parent_id={self.parent_id}, student_id={self.student_id})>"
