"""
CredentialService and BlockchainService for managing student credentials.

This service implements the core "OWN" phase of the LVO architecture.
"""

import hashlib
import secrets
from uuid import UUID
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.student import Student
from app.models.skill import Skill
from app.models.learning_path import LearningPath, LearningModule
from app.models.gamification import Badge
from app.models.verification import Verification, VerificationStatus
from app.models.credential import (
    Credential, OnChainCredential,
    CredentialType, CredentialStatus
)
from app.config import settings


class BlockchainService:
    """
    Service for blockchain operations.

    MVP: Simulated minting with transaction hash generation.
    Production: Real blockchain integration (Stellar, Polygon, etc.).

    This abstraction allows seamless upgrade from simulated to real blockchain.
    """

    @staticmethod
    async def mint_credential(
        credential: Credential,
        network: str = "simulated",
        owner_wallet_address: Optional[str] = None,
        db: AsyncSession = None
    ) -> OnChainCredential:
        """
        Mint a credential on blockchain (simulated for MVP).

        Args:
            credential: Credential to mint
            network: Target network ("simulated", "stellar-testnet", etc.)
            owner_wallet_address: Student's wallet address
            db: Database session (for committing)

        Returns:
            OnChainCredential record with minting details
        """
        # Check if already minted
        if credential.on_chain_record:
            return credential.on_chain_record

        # Generate simulated transaction details
        if network == "simulated":
            on_chain_record = await BlockchainService._simulated_mint(
                credential=credential,
                owner_wallet_address=owner_wallet_address
            )
        else:
            # Future: Real blockchain integration
            on_chain_record = await BlockchainService._real_blockchain_mint(
                credential=credential,
                network=network,
                owner_wallet_address=owner_wallet_address
            )

        # Save to database
        if db:
            db.add(on_chain_record)
            credential.status = CredentialStatus.MINTED
            await db.commit()
            await db.refresh(on_chain_record)

        return on_chain_record

    @staticmethod
    async def _simulated_mint(
        credential: Credential,
        owner_wallet_address: Optional[str]
    ) -> OnChainCredential:
        """
        Simulate blockchain minting for MVP.

        Generates realistic-looking transaction hash and metadata.
        """
        # Generate simulated transaction hash
        # Hash of credential ID + timestamp + random salt
        hash_input = f"{credential.id}{datetime.utcnow().isoformat()}{secrets.token_hex(16)}"
        tx_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        # Generate simulated wallet address if not provided
        if not owner_wallet_address:
            owner_wallet_address = f"SIMULATED_{secrets.token_hex(20).upper()}"

        # Generate metadata URI (simulated IPFS)
        metadata_uri = f"ipfs://Qm{secrets.token_hex(23)}"  # Simulated IPFS hash

        # Create on-chain record
        on_chain_record = OnChainCredential(
            credential_id=credential.id,
            network="simulated",
            transaction_hash=tx_hash,
            owner_wallet_address=owner_wallet_address,
            metadata_uri=metadata_uri,
            verification_url=f"https://stellar-ai.example.com/verify/{tx_hash}",
            is_simulated=True,
            minting_successful=True,
            minted_at=datetime.utcnow()
        )

        return on_chain_record

    @staticmethod
    async def _real_blockchain_mint(
        credential: Credential,
        network: str,
        owner_wallet_address: Optional[str]
    ) -> OnChainCredential:
        """
        Real blockchain minting (production-ready architecture).

        This is a placeholder for future implementation.
        In production, this would:
        1. Connect to blockchain network (Stellar, Polygon, etc.)
        2. Create NFT or credential token
        3. Upload metadata to IPFS
        4. Submit transaction
        5. Wait for confirmation
        6. Return transaction details

        Supported networks:
        - Stellar (stellar-mainnet, stellar-testnet)
        - Polygon (polygon-mainnet, polygon-mumbai)
        - Ethereum (ethereum-mainnet, ethereum-sepolia)
        """
        # TODO: Implement real blockchain integration
        # For now, return simulated with flag indicating it should be real
        on_chain_record = await BlockchainService._simulated_mint(
            credential=credential,
            owner_wallet_address=owner_wallet_address
        )
        on_chain_record.network = network
        on_chain_record.is_simulated = True  # Will be False in production
        on_chain_record.minting_error = "Production blockchain integration not yet implemented"

        return on_chain_record

    @staticmethod
    def verify_credential_on_chain(transaction_hash: str, network: str) -> dict:
        """
        Verify a credential by checking blockchain.

        Args:
            transaction_hash: Transaction hash to verify
            network: Blockchain network

        Returns:
            Dictionary with verification results
        """
        if network == "simulated":
            return {
                "valid": True,
                "network": "simulated",
                "tx_hash": transaction_hash,
                "message": "Simulated credential - MVP demo mode"
            }
        else:
            # TODO: Implement real blockchain verification
            return {
                "valid": False,
                "network": network,
                "tx_hash": transaction_hash,
                "message": "Production blockchain verification not yet implemented"
            }


class CredentialService:
    """Service for creating and managing student credentials."""

    @staticmethod
    async def create_credential_from_skill_mastery(
        student_id: UUID,
        skill_id: UUID,
        db: AsyncSession
    ) -> Optional[Credential]:
        """
        Create credential when student masters a skill (score >= 80).

        Args:
            student_id: ID of the student
            skill_id: ID of the mastered skill
            db: Database session

        Returns:
            Created credential or None if criteria not met
        """
        # Get skill and verifications
        skill_result = await db.execute(
            select(Skill).where(Skill.id == skill_id)
        )
        skill = skill_result.scalar_one_or_none()
        if not skill:
            return None

        # Check verifications
        verifications_result = await db.execute(
            select(Verification)
            .where(
                and_(
                    Verification.student_id == student_id,
                    Verification.skill_id == skill_id,
                    Verification.status == VerificationStatus.VERIFIED
                )
            )
        )
        verifications = verifications_result.scalars().all()

        # Need at least one verification
        if not verifications:
            return None

        # Calculate average score from verifications
        avg_score = sum(v.score for v in verifications if v.score) / len(verifications)

        # Only create credential if mastery level (80+)
        if avg_score < 80:
            return None

        # Check if credential already exists
        existing_result = await db.execute(
            select(Credential)
            .where(
                and_(
                    Credential.student_id == student_id,
                    Credential.skill_id == skill_id,
                    Credential.credential_type == CredentialType.SKILL_MASTERY,
                    Credential.status.in_([CredentialStatus.ISSUED, CredentialStatus.MINTED])
                )
            )
        )
        if existing_result.scalar_one_or_none():
            return None  # Already has this credential

        # Create credential
        credential = Credential(
            student_id=student_id,
            credential_type=CredentialType.SKILL_MASTERY,
            skill_id=skill_id,
            title=f"{skill.name} - Mastered",
            description=f"Demonstrated mastery of {skill.name} with {avg_score:.0f}% proficiency",
            verification_ids=[str(v.id) for v in verifications],
            credential_metadata={
                "skill_category": skill.category.value,
                "skill_level": skill.level,
                "average_score": avg_score,
                "verification_count": len(verifications)
            },
            issuer_name="Stellar AI",
            status=CredentialStatus.ISSUED,
            issued_at=datetime.utcnow()
        )

        db.add(credential)
        await db.commit()
        await db.refresh(credential)

        return credential

    @staticmethod
    async def create_credential_from_module_completion(
        student_id: UUID,
        module_id: UUID,
        module_score: float,
        db: AsyncSession
    ) -> Credential:
        """
        Create credential when student completes a module.

        Args:
            student_id: ID of the student
            module_id: ID of the completed module
            module_score: Score achieved in module
            db: Database session

        Returns:
            Created credential
        """
        # Get module and learning path
        module_result = await db.execute(
            select(LearningModule, LearningPath)
            .join(LearningPath, LearningModule.learning_path_id == LearningPath.id)
            .where(LearningModule.id == module_id)
        )
        result = module_result.first()
        if not result:
            return None

        module, learning_path = result

        # Get verifications from this module
        verifications_result = await db.execute(
            select(Verification)
            .where(
                and_(
                    Verification.student_id == student_id,
                    Verification.module_id == module_id,
                    Verification.status == VerificationStatus.VERIFIED
                )
            )
        )
        verifications = verifications_result.scalars().all()

        # Create credential
        credential = Credential(
            student_id=student_id,
            credential_type=CredentialType.MODULE_COMPLETION,
            module_id=module_id,
            learning_path_id=learning_path.id,
            title=f"{module.name} - Completed",
            description=f"Completed {module.name} in {learning_path.name} with {module_score:.0f}% score",
            verification_ids=[str(v.id) for v in verifications],
            credential_metadata={
                "module_name": module.name,
                "learning_path_name": learning_path.name,
                "score": module_score,
                "skills_verified": len(verifications)
            },
            issuer_name="Stellar AI",
            status=CredentialStatus.ISSUED,
            issued_at=datetime.utcnow()
        )

        db.add(credential)
        await db.commit()
        await db.refresh(credential)

        return credential

    @staticmethod
    async def create_credential_from_path_completion(
        student_id: UUID,
        learning_path_id: UUID,
        db: AsyncSession
    ) -> Credential:
        """
        Create credential when student completes entire learning path.

        Args:
            student_id: ID of the student
            learning_path_id: ID of the completed learning path
            db: Database session

        Returns:
            Created credential
        """
        # Get learning path
        path_result = await db.execute(
            select(LearningPath)
            .where(LearningPath.id == learning_path_id)
        )
        learning_path = path_result.scalar_one_or_none()
        if not learning_path:
            return None

        # Get all module credentials from this path
        module_credentials_result = await db.execute(
            select(Credential)
            .where(
                and_(
                    Credential.student_id == student_id,
                    Credential.learning_path_id == learning_path_id,
                    Credential.credential_type == CredentialType.MODULE_COMPLETION
                )
            )
        )
        module_credentials = module_credentials_result.scalars().all()

        # Create credential
        credential = Credential(
            student_id=student_id,
            credential_type=CredentialType.PATH_COMPLETION,
            learning_path_id=learning_path_id,
            title=f"{learning_path.name} - Path Completed",
            description=f"Successfully completed the {learning_path.name} learning path",
            credential_metadata={
                "learning_path_name": learning_path.name,
                "difficulty": learning_path.difficulty,
                "modules_completed": len(module_credentials),
                "completion_date": datetime.utcnow().isoformat()
            },
            issuer_name="Stellar AI",
            status=CredentialStatus.ISSUED,
            issued_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=365 * 3)  # Valid for 3 years
        )

        db.add(credential)
        await db.commit()
        await db.refresh(credential)

        return credential

    @staticmethod
    async def get_student_credentials(
        student_id: UUID,
        db: AsyncSession,
        credential_type: Optional[CredentialType] = None,
        include_blockchain: bool = True
    ) -> list[Credential]:
        """
        Get all credentials for a student.

        Args:
            student_id: ID of the student
            db: Database session
            credential_type: Optional filter by type
            include_blockchain: Whether to include blockchain details

        Returns:
            List of credentials
        """
        query = select(Credential).where(Credential.student_id == student_id)

        if credential_type:
            query = query.where(Credential.credential_type == credential_type)

        if include_blockchain:
            query = query.options(selectinload(Credential.on_chain_record))

        query = query.order_by(Credential.issued_at.desc())

        result = await db.execute(query)
        return result.scalars().all()
