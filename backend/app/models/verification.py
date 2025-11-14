"""
Verification model for the VERIFY phase of LVO architecture.

Verifications provide proof that a student has demonstrated competency in specific skills.
Multi-source verification: AI assessment, teacher review, system checks.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db import Base


class VerificationSource(str, enum.Enum):
    """Source of the verification."""
    AI_ASSESSMENT = "ai_assessment"  # AI evaluated student work
    TEACHER_REVIEW = "teacher_review"  # Teacher manually verified
    SYSTEM_CHECK = "system_check"  # Automated system verification (e.g., quiz score)
    PEER_REVIEW = "peer_review"  # Another student verified (future feature)
    SELF_ASSESSMENT = "self_assessment"  # Student self-reported (requires other verification)


class VerificationStatus(str, enum.Enum):
    """Status of the verification."""
    PENDING = "pending"  # Waiting for review
    VERIFIED = "verified"  # Competency confirmed
    REJECTED = "rejected"  # Competency not demonstrated
    EXPIRED = "expired"  # Verification no longer valid


class Verification(Base):
    """
    Represents proof that a student has demonstrated competency in a skill.

    Verifications are created when:
    1. A student completes a module with sufficient score
    2. AI assesses student work and confirms understanding
    3. A teacher manually verifies competency
    4. System checks automated assessments (quizzes, tests)

    Multiple verifications for the same skill strengthen confidence.
    """
    __tablename__ = "verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)

    # Optional: link to specific module, task, or conversation that triggered this verification
    module_id = Column(UUID(as_uuid=True), ForeignKey("learning_modules.id", ondelete="SET NULL"), nullable=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)

    # Source of verification
    source = Column(Enum(VerificationSource), nullable=False, index=True)

    # Status
    status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING, nullable=False, index=True)

    # Score or confidence level (0-100) from the verification source
    score = Column(Float, nullable=True)

    # Evidence: JSON containing proof data
    # Examples:
    # - AI: {"conversation_id": "...", "assessment_text": "...", "reasoning": "..."}
    # - Teacher: {"teacher_id": "...", "notes": "..."}
    # - System: {"quiz_id": "...", "correct_answers": 8, "total_questions": 10}
    evidence = Column(JSON, nullable=True)

    # Optional: ID of the teacher/user who verified (if source is teacher_review)
    verified_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Notes or comments from verifier
    notes = Column(Text, nullable=True)

    # Expiration date (some verifications may expire, e.g., after 1 year)
    expires_at = Column(DateTime, nullable=True)

    verified_at = Column(DateTime, nullable=True)  # When status changed to VERIFIED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="verifications")
    skill = relationship("Skill")
    module = relationship("LearningModule")
    task = relationship("Task")
    verified_by = relationship("User", foreign_keys=[verified_by_user_id])

    def __repr__(self):
        return f"<Verification(id={self.id}, student_id={self.student_id}, skill_id={self.skill_id}, source={self.source.value}, status={self.status.value})>"

    @property
    def is_valid(self) -> bool:
        """Check if verification is currently valid (verified and not expired)."""
        if self.status != VerificationStatus.VERIFIED:
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        return True
