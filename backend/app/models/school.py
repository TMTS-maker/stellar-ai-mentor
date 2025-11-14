"""School model"""
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class School(Base):
    """School model"""
    __tablename__ = "schools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    admin_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relationships
    admin_user = relationship("User", back_populates="school")
    teachers = relationship("Teacher", back_populates="school")
    students = relationship("Student", back_populates="school")
    classrooms = relationship("Classroom", back_populates="school")
    subjects = relationship("Subject", back_populates="school")

    def __repr__(self):
        return f"<School(id={self.id}, name={self.name})>"
