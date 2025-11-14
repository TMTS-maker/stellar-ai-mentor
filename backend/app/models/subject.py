"""Subject model"""
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class Subject(Base):
    """Subject model"""
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Relationships
    school = relationship("School", back_populates="subjects")
    classroom_links = relationship("ClassSubject", back_populates="subject")
    tasks = relationship("Task", back_populates="subject")

    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name})>"
