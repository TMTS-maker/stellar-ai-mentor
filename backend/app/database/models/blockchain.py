"""
Stellecta LucidAI Backend - Blockchain Credential Model

Stellar blockchain-based credential (NFT) tracking.

STUB: Basic schema for Phase 0.
Full Stellar integration to be implemented later.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database.engine import Base


class BlockchainCredential(Base):
    """
    Blockchain Credential entity.

    Represents a skill/mastery credential issued to a student.

    Credentials are:
    - Verified on-chain (Stellar blockchain)
    - Immutable proof of mastery
    - Portable across institutions
    """

    __tablename__ = "blockchain_credentials"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Key
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False, index=True)

    # ========================================================================
    # CREDENTIAL DETAILS
    # ========================================================================
    credential_type = Column(String(50), nullable=False)
    """
    Credential type:
    - mastery_certificate
    - competency_badge
    - course_completion
    """

    subject = Column(String(100), nullable=False)
    """Subject: Mathematics, Physics, etc."""

    competency = Column(String(255), nullable=True)
    """Specific competency: Fractions, Quadratic Equations, etc."""

    metadata = Column(JSON, default=dict, nullable=True)
    """
    Additional credential metadata:
    {
        "issuer": "Stellecta",
        "grade_level": 7,
        "assessment_score": 0.95
    }
    """

    # ========================================================================
    # BLOCKCHAIN DATA (Stellar)
    # ========================================================================
    stellar_transaction_hash = Column(String(255), nullable=True, unique=True)
    """Stellar transaction hash (proof on blockchain)"""

    stellar_asset_code = Column(String(12), nullable=True)
    """Stellar asset code (e.g., 'MATHMAS')"""

    stellar_issuer_address = Column(String(56), nullable=True)
    """Stellar issuer public key"""

    stellar_recipient_address = Column(String(56), nullable=True)
    """Student's Stellar wallet address"""

    # ========================================================================
    # STATUS
    # ========================================================================
    is_minted = Column(Boolean, default=False, nullable=False)
    """Whether credential has been minted to blockchain"""

    minted_at = Column(DateTime(timezone=True), nullable=True)
    """Timestamp of blockchain minting"""

    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    earned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    """When student earned this credential"""

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        status = "minted" if self.is_minted else "pending"
        return f"<BlockchainCredential(student_id={self.student_id}, subject={self.subject}, status={status})>"
