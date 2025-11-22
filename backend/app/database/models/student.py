"""
Stellecta LucidAI Backend - Student Model

Core student domain model.
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database.engine import Base


class Student(Base):
    """
    Student entity.

    Represents a learner in the Stellecta platform.
    """

    __tablename__ = "students"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic Info
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    full_name = Column(String(255), nullable=True)

    # Profile
    age = Column(Integer, nullable=True)
    grade_level = Column(Integer, nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Metadata
    metadata = Column(JSON, default=dict, nullable=True)
    """
    Additional metadata such as:
    - learning_preferences
    - accessibility_needs
    - parent_consent
    """

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships (defined in other models)
    # conversations = relationship("Conversation", back_populates="student")
    # h_pem_scores = relationship("HPEMScore", back_populates="student")
    # gamification_progress = relationship("GamificationProgress", back_populates="student")
    # credentials = relationship("BlockchainCredential", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.id}, username={self.username}, grade={self.grade_level})>"
