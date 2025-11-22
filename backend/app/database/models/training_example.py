"""
Stellecta LucidAI Backend - Training Example Model

NEW TABLE: Anonymized, labeled training data for LucidAI fine-tuning.

This table stores processed conversation data ready for:
- Supervised fine-tuning (SFT)
- Reinforcement learning from human feedback (RLHF)
- Model evaluation and benchmarking
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database.engine import Base


class TrainingExample(Base):
    """
    Training Example entity.

    Anonymized, labeled conversation examples for LucidAI training.

    CRITICAL: All data in this table is anonymized and COPPA/GDPR compliant.
    No personally identifiable information (PII) is stored.
    """

    __tablename__ = "training_examples"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ========================================================================
    # SOURCE TRACKING
    # ========================================================================
    source_interaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("llm_interactions.id"),
        nullable=False,
        index=True
    )

    anonymous_student_id = Column(String(64), nullable=False, index=True)
    """One-way hash of student ID (cannot be reversed)"""

    # ========================================================================
    # TRAINING DATA (Instruction-Tuning Format)
    # ========================================================================
    system_prompt = Column(Text, nullable=False)
    """
    Mentor persona + student context:
    "You are Stella, a patient math tutor. Student is 12 years old, grade 7,
    proficiency 0.65, weak in fractions..."
    """

    user_message = Column(Text, nullable=False)
    """Student's question or input"""

    assistant_response = Column(Text, nullable=False)
    """Target response for training (best quality response)"""

    # ========================================================================
    # LABELS (Automated)
    # ========================================================================
    subject = Column(String(50), nullable=True, index=True)
    """Subject domain: math, physics, chemistry, etc."""

    grade_level = Column(Integer, nullable=True)
    """Student grade level at time of interaction"""

    mentor_persona = Column(String(50), nullable=True, index=True)
    """Mentor ID: stella, max, nova, etc."""

    h_pem_proficiency = Column(Float, nullable=True)
    """Student H-PEM proficiency score at time of interaction"""

    student_age = Column(Integer, nullable=True)
    """Student age (anonymized age band acceptable)"""

    # ========================================================================
    # LABELS (Semi-Automated - Evaluation Models)
    # ========================================================================
    didactic_quality_score = Column(Float, nullable=True)
    """Didactic quality score from evaluation model (0-1)"""

    error_type = Column(String(50), nullable=True)
    """
    Error classification:
    - conceptual
    - procedural
    - careless
    - none
    """

    scaffolding_level = Column(String(20), nullable=True)
    """
    Scaffolding appropriateness:
    - heavy
    - medium
    - light
    - none
    """

    # ========================================================================
    # LABELS (Human - Teacher Reviews)
    # ========================================================================
    teacher_rating = Column(Integer, nullable=True)
    """Teacher quality rating (1-5 stars) if available"""

    teacher_notes = Column(Text, nullable=True)
    """Teacher feedback/improvement suggestions"""

    # ========================================================================
    # LABELS (Implicit Feedback)
    # ========================================================================
    student_helpful = Column(Boolean, nullable=True)
    """Student thumbs up/down feedback"""

    outcome_h_pem_delta = Column(Float, nullable=True)
    """
    H-PEM proficiency change after interaction.
    CRITICAL for RLHF reward signal:
    - Positive delta = good teaching
    - Negative delta = poor teaching
    """

    # ========================================================================
    # DATASET VERSIONING
    # ========================================================================
    dataset_version = Column(String(50), nullable=True, index=True)
    """
    Dataset version for reproducibility:
    - v1.0
    - v1.1
    - v2.0
    """

    split = Column(String(20), nullable=True, index=True)
    """
    Train/val/test split:
    - train
    - val
    - test
    """

    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # ========================================================================
    # RELATIONSHIPS
    # ========================================================================
    source_interaction = relationship("LLMInteraction", back_populates="training_example")

    def __repr__(self):
        return f"<TrainingExample(id={self.id}, subject={self.subject}, quality={self.didactic_quality_score})>"
