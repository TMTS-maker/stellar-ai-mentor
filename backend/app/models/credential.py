"""
Credential and OnChainCredential models for the OWN phase of LVO architecture.

Credentials are portable, student-owned proof of achievement.
OnChainCredential provides blockchain anchoring for tamper-proof verification.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db import Base


class CredentialType(str, enum.Enum):
    """Type of credential."""
    SKILL_MASTERY = "skill_mastery"  # Mastered a single skill
    MODULE_COMPLETION = "module_completion"  # Completed a learning module
    PATH_COMPLETION = "path_completion"  # Completed entire learning path
    BADGE_ACHIEVEMENT = "badge_achievement"  # Earned a gamification badge
    MILESTONE = "milestone"  # Reached a significant milestone
    CERTIFICATE = "certificate"  # Formal certificate of completion


class CredentialStatus(str, enum.Enum):
    """Status of the credential."""
    DRAFT = "draft"  # Being prepared
    ISSUED = "issued"  # Issued to student
    MINTED = "minted"  # Anchored on blockchain
    REVOKED = "revoked"  # No longer valid


class Credential(Base):
    """
    Represents a portable, student-owned proof of achievement.

    Credentials are created when students:
    - Master a skill (verified proficiency)
    - Complete a learning module
    - Complete a learning path
    - Earn significant badges or reach milestones

    Students can share credentials with schools, parents, or future employers.
    """
    __tablename__ = "credentials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)

    # Type of credential
    credential_type = Column(Enum(CredentialType), nullable=False, index=True)

    # Status
    status = Column(Enum(CredentialStatus), default=CredentialStatus.DRAFT, nullable=False, index=True)

    # Title and description of the achievement
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # What was achieved: skill_id, module_id, path_id, or badge_id
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="SET NULL"), nullable=True)
    module_id = Column(UUID(as_uuid=True), ForeignKey("learning_modules.id", ondelete="SET NULL"), nullable=True)
    learning_path_id = Column(UUID(as_uuid=True), ForeignKey("learning_paths.id", ondelete="SET NULL"), nullable=True)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id", ondelete="SET NULL"), nullable=True)

    # Evidence: IDs of verifications that support this credential
    verification_ids = Column(JSON, nullable=True)  # e.g., ["verification-uuid-1", "verification-uuid-2"]

    # Metadata: additional information
    # Examples:
    # - {"final_score": 95, "tasks_completed": 12, "time_spent_hours": 8}
    # - {"level": "A1", "category": "language"}
    credential_metadata = Column(JSON, nullable=True)

    # Issuer information (school, organization)
    issuer_name = Column(String(255), nullable=True)  # e.g., "Stellar AI" or school name
    issuer_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="SET NULL"), nullable=True)

    # Expiration (some credentials may expire)
    expires_at = Column(DateTime, nullable=True)

    issued_at = Column(DateTime, nullable=True)  # When status changed to ISSUED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="credentials")
    skill = relationship("Skill")
    module = relationship("LearningModule")
    learning_path = relationship("LearningPath")
    badge = relationship("Badge")
    issuer_school = relationship("School")
    on_chain_record = relationship("OnChainCredential", back_populates="credential", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Credential(id={self.id}, student_id={self.student_id}, type={self.credential_type.value}, status={self.status.value})>"

    @property
    def is_valid(self) -> bool:
        """Check if credential is currently valid."""
        if self.status == CredentialStatus.REVOKED:
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        return self.status in [CredentialStatus.ISSUED, CredentialStatus.MINTED]

    @property
    def is_blockchain_anchored(self) -> bool:
        """Check if credential is anchored on blockchain."""
        return self.status == CredentialStatus.MINTED and self.on_chain_record is not None


class OnChainCredential(Base):
    """
    Tracks blockchain anchoring details for credentials.

    In MVP: Simulated minting (generates transaction hash, stores locally).
    In Production: Real blockchain integration (Stellar, Ethereum, Polygon, etc.).

    This abstraction allows seamless upgrade from simulated to real blockchain.
    """
    __tablename__ = "on_chain_credentials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    credential_id = Column(UUID(as_uuid=True), ForeignKey("credentials.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Blockchain network (simulated for MVP, real for production)
    network = Column(String(100), nullable=False, index=True)  # e.g., "stellar-testnet", "polygon-mainnet", "simulated"

    # Transaction/minting details
    transaction_hash = Column(String(255), nullable=True, unique=True, index=True)  # Blockchain tx hash
    contract_address = Column(String(255), nullable=True)  # Smart contract address (if applicable)
    token_id = Column(String(255), nullable=True)  # NFT token ID (if applicable)

    # Wallet address that owns this credential
    owner_wallet_address = Column(String(255), nullable=True, index=True)

    # IPFS or storage URL for credential metadata
    metadata_uri = Column(String(512), nullable=True)

    # Gas/transaction fees (for production tracking)
    gas_fee = Column(String(100), nullable=True)

    # Verification: anyone can verify this credential by checking the blockchain
    verification_url = Column(String(512), nullable=True)  # e.g., block explorer link

    # Minting status
    is_simulated = Column(Boolean, default=True, nullable=False)  # True for MVP, False for production
    minting_successful = Column(Boolean, default=False, nullable=False)
    minting_error = Column(Text, nullable=True)

    minted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    credential = relationship("Credential", back_populates="on_chain_record")

    def __repr__(self):
        return f"<OnChainCredential(id={self.id}, credential_id={self.credential_id}, network='{self.network}', tx_hash='{self.transaction_hash}')>"

    @property
    def blockchain_explorer_url(self) -> str | None:
        """Generate blockchain explorer URL based on network and transaction hash."""
        if not self.transaction_hash or self.is_simulated:
            return None

        # Map networks to explorer base URLs
        explorers = {
            "stellar-mainnet": "https://stellarchain.io/tx",
            "stellar-testnet": "https://testnet.stellarchain.io/tx",
            "polygon-mainnet": "https://polygonscan.com/tx",
            "polygon-mumbai": "https://mumbai.polygonscan.com/tx",
            "ethereum-mainnet": "https://etherscan.io/tx",
            "ethereum-sepolia": "https://sepolia.etherscan.io/tx",
        }

        base_url = explorers.get(self.network)
        if base_url:
            return f"{base_url}/{self.transaction_hash}"
        return None
