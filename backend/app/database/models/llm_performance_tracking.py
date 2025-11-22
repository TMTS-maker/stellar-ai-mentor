"""
Stellecta LucidAI Backend - LLM Performance Tracking Model

NEW TABLE: Tracks LLM accuracy over time for confidence calibration.

Used to:
- Calibrate LLM self-reported confidence scores
- Optimize routing policies (which LLM performs best on which tasks)
- Monitor model degradation or improvement
"""

from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database.engine import Base


class LLMPerformanceTracking(Base):
    """
    LLM Performance Tracking entity.

    Tracks prediction vs. actual outcomes for each LLM provider.

    CRITICAL for:
    - Confidence calibration (adjust overconfident/underconfident models)
    - Routing policy optimization (route tasks to best-performing LLM)
    """

    __tablename__ = "llm_performance_tracking"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Key
    interaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("llm_interactions.id"),
        nullable=False,
        index=True
    )

    # ========================================================================
    # LLM IDENTIFICATION
    # ========================================================================
    llm_provider = Column(String(50), nullable=False, index=True)
    """LLM provider: lucidai, gemini, openai, claude, etc."""

    task_type = Column(String(50), nullable=False, index=True)
    """Task type: tutoring, mastery_verification, creative, etc."""

    # ========================================================================
    # PREDICTION VS. OUTCOME
    # ========================================================================
    predicted_confidence = Column(Float, nullable=False)
    """LLM's self-reported confidence (0-1)"""

    actual_success = Column(Boolean, nullable=True)
    """
    Did the task succeed?
    - True: Student succeeded, H-PEM improved, or task completed
    - False: Student struggled, needed escalation, or negative feedback
    """

    h_pem_delta = Column(Float, nullable=True)
    """H-PEM proficiency change after interaction (can be negative)"""

    student_helpful = Column(Boolean, nullable=True)
    """Student thumbs up/down feedback"""

    # ========================================================================
    # CALIBRATION METRICS
    # ========================================================================
    confidence_error = Column(Float, nullable=True)
    """
    Absolute difference between predicted confidence and actual success.
    confidence_error = abs(predicted_confidence - actual_success)

    Low error = well-calibrated model
    High error = poorly calibrated (overconfident or underconfident)
    """

    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # ========================================================================
    # RELATIONSHIPS
    # ========================================================================
    interaction = relationship("LLMInteraction", back_populates="performance_tracking")

    def __repr__(self):
        return f"<LLMPerformanceTracking(llm={self.llm_provider}, task={self.task_type}, error={self.confidence_error})>"
