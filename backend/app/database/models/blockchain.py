"""
Blockchain and H-PEM Credential Models
"""

from sqlalchemy import Column, String, Float, TIMESTAMP, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
from datetime import datetime


class HPEMCredential(Base):
    """H-PEM Credentials stored on Stellar blockchain"""

    __tablename__ = "hpem_credentials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    objective_id = Column(
        UUID(as_uuid=True), ForeignKey("curriculum_objectives.id"), nullable=False
    )
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=True)

    # H-PEM Score
    h_pem_score = Column(Float, nullable=False)

    # LVO Breakdown
    learn_score = Column(Float, nullable=False)
    verify_score = Column(Float, nullable=False)
    own_score = Column(Float, nullable=False)

    # Blockchain details
    stellar_tx_hash = Column(String(255), nullable=False, unique=True)
    stellar_asset_code = Column(String(12), nullable=True)
    stellar_issuer_address = Column(String(56), nullable=True)

    # Verification
    is_verified = Column(String(20), default="pending")  # 'pending', 'verified', 'failed'
    verification_timestamp = Column(TIMESTAMP, nullable=True)

    # Metadata
    extra_metadata = Column(JSON, nullable=True)
    credential_data = Column(JSON, nullable=True)

    # Timestamps
    issued_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    student = relationship("Student")
    objective = relationship("CurriculumObjective")
    skill = relationship("Skill")
