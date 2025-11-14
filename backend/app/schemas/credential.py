"""
Pydantic schemas for Credential and OnChainCredential models.
"""

from uuid import UUID
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

from app.models.credential import CredentialType, CredentialStatus


# ============================================================================
# OnChainCredential Schemas
# ============================================================================

class OnChainCredentialBase(BaseModel):
    """Base schema for OnChainCredential."""
    network: str = Field(..., description="Blockchain network (e.g., 'stellar-testnet', 'simulated')")
    transaction_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    contract_address: Optional[str] = Field(None, description="Smart contract address")
    token_id: Optional[str] = Field(None, description="NFT token ID")
    owner_wallet_address: Optional[str] = Field(None, description="Wallet address that owns this credential")
    metadata_uri: Optional[str] = Field(None, description="IPFS or storage URL for metadata")
    gas_fee: Optional[str] = Field(None, description="Gas/transaction fee")
    verification_url: Optional[str] = Field(None, description="Block explorer link")
    is_simulated: bool = Field(True, description="True for MVP simulated minting, False for real blockchain")


class OnChainCredentialResponse(OnChainCredentialBase):
    """Schema for on-chain credential response."""
    id: UUID
    credential_id: UUID
    minting_successful: bool
    minting_error: Optional[str]
    blockchain_explorer_url: Optional[str]  # Computed property
    minted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Credential Schemas
# ============================================================================

class CredentialBase(BaseModel):
    """Base schema for Credential."""
    credential_type: CredentialType = Field(..., description="Type of credential")
    title: str = Field(..., min_length=1, max_length=255, description="Title of the achievement")
    description: Optional[str] = Field(None, description="Description of what was achieved")
    credential_metadata: Optional[dict[str, Any]] = Field(None, description="Additional metadata")
    issuer_name: Optional[str] = Field(None, description="Name of the issuing organization")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")


class CredentialCreate(CredentialBase):
    """Schema for creating a credential."""
    student_id: UUID = Field(..., description="ID of the student")
    skill_id: Optional[UUID] = Field(None, description="ID of the skill (for skill mastery credentials)")
    module_id: Optional[UUID] = Field(None, description="ID of the module (for module completion)")
    learning_path_id: Optional[UUID] = Field(None, description="ID of the learning path (for path completion)")
    badge_id: Optional[UUID] = Field(None, description="ID of the badge (for badge achievements)")
    verification_ids: Optional[list[str]] = Field(None, description="IDs of supporting verifications")
    issuer_id: Optional[UUID] = Field(None, description="ID of the issuing school")


class CredentialUpdate(BaseModel):
    """Schema for updating a credential."""
    status: Optional[CredentialStatus] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    credential_metadata: Optional[dict[str, Any]] = None
    expires_at: Optional[datetime] = None


class CredentialResponse(CredentialBase):
    """Schema for credential response."""
    id: UUID
    student_id: UUID
    status: CredentialStatus
    skill_id: Optional[UUID]
    module_id: Optional[UUID]
    learning_path_id: Optional[UUID]
    badge_id: Optional[UUID]
    verification_ids: Optional[list[str]]
    issuer_id: Optional[UUID]
    is_valid: bool  # Computed property
    is_blockchain_anchored: bool  # Computed property
    issued_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CredentialWithBlockchain(CredentialResponse):
    """Schema for credential with blockchain details."""
    on_chain_record: Optional[OnChainCredentialResponse] = None

    class Config:
        from_attributes = True


class CredentialWithDetails(CredentialWithBlockchain):
    """Schema for credential with full details (skill name, module name, etc.)."""
    skill_name: Optional[str] = None
    module_name: Optional[str] = None
    learning_path_name: Optional[str] = None
    badge_name: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================================
# Minting Request
# ============================================================================

class MintCredentialRequest(BaseModel):
    """Request to mint a credential on blockchain."""
    credential_id: UUID = Field(..., description="ID of the credential to mint")
    network: str = Field("simulated", description="Target blockchain network")
    owner_wallet_address: Optional[str] = Field(None, description="Student's wallet address (optional for simulated)")


class MintCredentialResponse(BaseModel):
    """Response after minting a credential."""
    credential_id: UUID
    success: bool
    message: str
    on_chain_record: Optional[OnChainCredentialResponse] = None

    class Config:
        from_attributes = True


# ============================================================================
# Student Credentials Portfolio
# ============================================================================

class StudentCredentialsPortfolio(BaseModel):
    """Complete credentials portfolio for a student."""
    student_id: UUID
    total_credentials: int = Field(..., description="Total number of credentials")
    issued_credentials: int = Field(..., description="Issued credentials")
    minted_credentials: int = Field(..., description="Blockchain-anchored credentials")
    credentials_by_type: dict[str, int] = Field(default_factory=dict, description="Count by credential type")
    credentials: list[CredentialWithDetails] = Field(default_factory=list, description="All credentials with details")

    class Config:
        from_attributes = True


# ============================================================================
# Shareable Credential (for external sharing)
# ============================================================================

class ShareableCredential(BaseModel):
    """Public-facing credential for sharing (no sensitive data)."""
    credential_id: UUID
    title: str
    description: Optional[str]
    credential_type: str
    skill_name: Optional[str]
    issued_at: Optional[datetime]
    issuer_name: Optional[str]
    verification_url: Optional[str]  # Blockchain verification URL
    is_blockchain_verified: bool

    class Config:
        from_attributes = True
