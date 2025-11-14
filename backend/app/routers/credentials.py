"""
API router for Credentials (LVO - OWN phase).
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_db
from app.auth import get_current_user, require_role
from app.models.user import User
from app.models.student import Student
from app.models.skill import Skill
from app.models.learning_path import LearningPath, LearningModule
from app.models.gamification import Badge
from app.models.credential import Credential, CredentialType, CredentialStatus
from app.schemas.credential import (
    CredentialCreate, CredentialUpdate, CredentialResponse,
    CredentialWithBlockchain, CredentialWithDetails,
    MintCredentialRequest, MintCredentialResponse,
    StudentCredentialsPortfolio, ShareableCredential,
    OnChainCredentialResponse
)
from app.services.credentials import CredentialService, BlockchainService


router = APIRouter(prefix="/credentials", tags=["Credentials"])


@router.post("", response_model=CredentialResponse, status_code=status.HTTP_201_CREATED)
async def create_credential(
    credential_data: CredentialCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "school_admin"))
):
    """
    Create a new credential manually.

    Typically, credentials are created automatically when students:
    - Master a skill
    - Complete a module
    - Complete a learning path

    But teachers and admins can also create them manually.
    """
    credential = Credential(**credential_data.model_dump())
    db.add(credential)
    await db.commit()
    await db.refresh(credential)

    return credential


@router.get("/me/credentials", response_model=StudentCredentialsPortfolio)
async def get_my_credentials(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    """Get current student's complete credentials portfolio."""
    # Get student
    student_result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # Get all credentials
    credentials = await CredentialService.get_student_credentials(
        student_id=student.id,
        db=db,
        include_blockchain=True
    )

    # Build credentials with details
    credentials_with_details = []
    issued_count = 0
    minted_count = 0
    credentials_by_type = {}

    for credential in credentials:
        # Get skill name if applicable
        skill_name = None
        if credential.skill_id:
            skill_result = await db.execute(
                select(Skill.name).where(Skill.id == credential.skill_id)
            )
            skill_name = skill_result.scalar_one_or_none()

        # Get module name if applicable
        module_name = None
        if credential.module_id:
            module_result = await db.execute(
                select(LearningModule.name).where(LearningModule.id == credential.module_id)
            )
            module_name = module_result.scalar_one_or_none()

        # Get learning path name if applicable
        learning_path_name = None
        if credential.learning_path_id:
            path_result = await db.execute(
                select(LearningPath.name).where(LearningPath.id == credential.learning_path_id)
            )
            learning_path_name = path_result.scalar_one_or_none()

        # Get badge name if applicable
        badge_name = None
        if credential.badge_id:
            badge_result = await db.execute(
                select(Badge.name).where(Badge.id == credential.badge_id)
            )
            badge_name = badge_result.scalar_one_or_none()

        # Build on-chain record response
        on_chain_response = None
        if credential.on_chain_record:
            on_chain_response = OnChainCredentialResponse.model_validate(credential.on_chain_record)

        credentials_with_details.append(CredentialWithDetails(
            id=credential.id,
            student_id=credential.student_id,
            credential_type=credential.credential_type,
            status=credential.status,
            title=credential.title,
            description=credential.description,
            skill_id=credential.skill_id,
            module_id=credential.module_id,
            learning_path_id=credential.learning_path_id,
            badge_id=credential.badge_id,
            verification_ids=credential.verification_ids,
            credential_metadata=credential.credential_metadata,
            issuer_name=credential.issuer_name,
            issuer_id=credential.issuer_id,
            expires_at=credential.expires_at,
            is_valid=credential.is_valid,
            is_blockchain_anchored=credential.is_blockchain_anchored,
            issued_at=credential.issued_at,
            created_at=credential.created_at,
            updated_at=credential.updated_at,
            on_chain_record=on_chain_response,
            skill_name=skill_name,
            module_name=module_name,
            learning_path_name=learning_path_name,
            badge_name=badge_name
        ))

        # Count stats
        if credential.status == CredentialStatus.ISSUED:
            issued_count += 1
        elif credential.status == CredentialStatus.MINTED:
            minted_count += 1

        # Count by type
        type_key = credential.credential_type.value
        credentials_by_type[type_key] = credentials_by_type.get(type_key, 0) + 1

    return StudentCredentialsPortfolio(
        student_id=student.id,
        total_credentials=len(credentials),
        issued_credentials=issued_count,
        minted_credentials=minted_count,
        credentials_by_type=credentials_by_type,
        credentials=credentials_with_details
    )


@router.get("/student/{student_id}/credentials", response_model=list[CredentialWithDetails])
async def get_student_credentials(
    student_id: UUID,
    credential_type: CredentialType | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "parent", "school_admin"))
):
    """
    Get credentials for a specific student.

    Only teachers, parents, and school admins can access this.
    """
    # TODO: Add authorization check
    credentials = await CredentialService.get_student_credentials(
        student_id=student_id,
        db=db,
        credential_type=credential_type,
        include_blockchain=True
    )

    # Build response with details (similar to above)
    result = []
    for credential in credentials:
        on_chain_response = None
        if credential.on_chain_record:
            on_chain_response = OnChainCredentialResponse.model_validate(credential.on_chain_record)

        result.append(CredentialWithDetails(
            id=credential.id,
            student_id=credential.student_id,
            credential_type=credential.credential_type,
            status=credential.status,
            title=credential.title,
            description=credential.description,
            skill_id=credential.skill_id,
            module_id=credential.module_id,
            learning_path_id=credential.learning_path_id,
            badge_id=credential.badge_id,
            verification_ids=credential.verification_ids,
            credential_metadata=credential.credential_metadata,
            issuer_name=credential.issuer_name,
            issuer_id=credential.issuer_id,
            expires_at=credential.expires_at,
            is_valid=credential.is_valid,
            is_blockchain_anchored=credential.is_blockchain_anchored,
            issued_at=credential.issued_at,
            created_at=credential.created_at,
            updated_at=credential.updated_at,
            on_chain_record=on_chain_response,
            skill_name=None,
            module_name=None,
            learning_path_name=None,
            badge_name=None
        ))

    return result


@router.get("/{credential_id}", response_model=CredentialWithBlockchain)
async def get_credential(
    credential_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific credential by ID."""
    result = await db.execute(
        select(Credential)
        .options(selectinload(Credential.on_chain_record))
        .where(Credential.id == credential_id)
    )
    credential = result.scalar_one_or_none()

    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")

    # TODO: Add authorization check

    return credential


@router.put("/{credential_id}", response_model=CredentialResponse)
async def update_credential(
    credential_id: UUID,
    credential_data: CredentialUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "school_admin"))
):
    """Update a credential. Only teachers and school admins can update credentials."""
    result = await db.execute(
        select(Credential).where(Credential.id == credential_id)
    )
    credential = result.scalar_one_or_none()

    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")

    for field, value in credential_data.model_dump(exclude_unset=True).items():
        setattr(credential, field, value)

    await db.commit()
    await db.refresh(credential)

    return credential


# ============================================================================
# Blockchain Minting
# ============================================================================

@router.post("/mint", response_model=MintCredentialResponse, status_code=status.HTTP_201_CREATED)
async def mint_credential(
    mint_request: MintCredentialRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    """
    Mint a credential on blockchain (simulated for MVP).

    This endpoint allows students to anchor their credentials on blockchain,
    making them tamper-proof and independently verifiable.

    In MVP: Simulated minting with transaction hash generation.
    In Production: Real blockchain integration (Stellar, Polygon, etc.).

    Students can only mint their own credentials.
    """
    # Get credential
    result = await db.execute(
        select(Credential, Student)
        .join(Student, Credential.student_id == Student.id)
        .where(Credential.id == mint_request.credential_id)
    )
    data = result.first()

    if not data:
        raise HTTPException(status_code=404, detail="Credential not found")

    credential, student = data

    # Check authorization: student can only mint their own credentials
    if student.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only mint your own credentials")

    # Check if credential is issued
    if credential.status not in [CredentialStatus.ISSUED, CredentialStatus.MINTED]:
        raise HTTPException(status_code=400, detail="Credential must be issued before minting")

    # Check if already minted
    if credential.on_chain_record:
        return MintCredentialResponse(
            credential_id=credential.id,
            success=True,
            message="Credential was already minted on blockchain",
            on_chain_record=OnChainCredentialResponse.model_validate(credential.on_chain_record)
        )

    try:
        # Mint on blockchain
        on_chain_record = await BlockchainService.mint_credential(
            credential=credential,
            network=mint_request.network,
            owner_wallet_address=mint_request.owner_wallet_address,
            db=db
        )

        return MintCredentialResponse(
            credential_id=credential.id,
            success=on_chain_record.minting_successful,
            message="Credential successfully minted on blockchain!" if on_chain_record.minting_successful else "Minting failed",
            on_chain_record=OnChainCredentialResponse.model_validate(on_chain_record)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to mint credential: {str(e)}"
        )


@router.get("/verify/{transaction_hash}", response_model=dict)
async def verify_credential_on_chain(
    transaction_hash: str,
    network: str = "simulated",
    db: AsyncSession = Depends(get_db)
):
    """
    Verify a credential by checking blockchain.

    This endpoint is public - anyone with a transaction hash can verify a credential.
    No authentication required.
    """
    result = BlockchainService.verify_credential_on_chain(
        transaction_hash=transaction_hash,
        network=network
    )

    return result


# ============================================================================
# Public Sharing
# ============================================================================

@router.get("/{credential_id}/share", response_model=ShareableCredential)
async def get_shareable_credential(
    credential_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a public-facing shareable version of a credential.

    This endpoint is public (no auth required) and returns only non-sensitive data
    suitable for sharing with schools, employers, or portfolio websites.
    """
    result = await db.execute(
        select(Credential)
        .options(selectinload(Credential.on_chain_record))
        .where(Credential.id == credential_id)
    )
    credential = result.scalar_one_or_none()

    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")

    # Only share if credential is issued or minted
    if credential.status not in [CredentialStatus.ISSUED, CredentialStatus.MINTED]:
        raise HTTPException(status_code=403, detail="This credential is not available for sharing")

    # Get skill name if applicable
    skill_name = None
    if credential.skill_id:
        skill_result = await db.execute(
            select(Skill.name).where(Skill.id == credential.skill_id)
        )
        skill_name = skill_result.scalar_one_or_none()

    # Get verification URL from blockchain record
    verification_url = None
    if credential.on_chain_record:
        verification_url = credential.on_chain_record.verification_url or credential.on_chain_record.blockchain_explorer_url

    return ShareableCredential(
        credential_id=credential.id,
        title=credential.title,
        description=credential.description,
        credential_type=credential.credential_type.value,
        skill_name=skill_name,
        issued_at=credential.issued_at,
        issuer_name=credential.issuer_name,
        verification_url=verification_url,
        is_blockchain_verified=credential.is_blockchain_anchored
    )
