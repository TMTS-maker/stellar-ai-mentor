"""
Stellecta LucidAI Backend - H-PEM Model

H-PEM (Holistic Pedagogical Engagement Metrics) tracking.

H-PEM = Proficiency + Resilience + Velocity + Engagement + Transfer
"""

from sqlalchemy import Column, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database.engine import Base


class HPEMScore(Base):
    """
    H-PEM Score entity.

    Tracks student's holistic learning metrics over time.

    H-PEM Components:
    - Proficiency (30%): Mastery of concepts
    - Resilience (20%): Recovery from errors, growth mindset
    - Velocity (20%): Learning speed, progress rate
    - Engagement (15%): Active participation, curiosity
    - Transfer (15%): Ability to apply knowledge to new contexts
    """

    __tablename__ = "hpem_scores"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Key
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False, index=True)

    # ========================================================================
    # H-PEM COMPONENTS (0-1 scale)
    # ========================================================================
    proficiency = Column(Float, nullable=False, default=0.5)
    """Mastery of concepts (30% weight)"""

    resilience = Column(Float, nullable=False, default=0.5)
    """Recovery from errors, growth mindset (20% weight)"""

    velocity = Column(Float, nullable=False, default=0.5)
    """Learning speed, progress rate (20% weight)"""

    engagement = Column(Float, nullable=False, default=0.5)
    """Active participation, curiosity (15% weight)"""

    transfer = Column(Float, nullable=False, default=0.5)
    """Ability to apply knowledge to new contexts (15% weight)"""

    # ========================================================================
    # COMPOSITE SCORE
    # ========================================================================
    composite_score = Column(Float, nullable=False, default=0.5)
    """
    Weighted composite H-PEM score:
    composite = (
        0.30 * proficiency +
        0.20 * resilience +
        0.20 * velocity +
        0.15 * engagement +
        0.15 * transfer
    )
    """

    # ========================================================================
    # CONTEXT
    # ========================================================================
    subject = Column(UUID, nullable=True)
    """Subject-specific H-PEM (if applicable)"""

    metadata = Column(JSON, default=dict, nullable=True)
    """Additional context (weak skills, recent improvements, etc.)"""

    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    measured_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<HPEMScore(student_id={self.student_id}, composite={self.composite_score:.2f})>"
