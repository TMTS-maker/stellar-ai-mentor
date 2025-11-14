"""
API router for Verifications (LVO - VERIFY phase).
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.auth import get_current_user, require_role
from app.models.user import User
from app.models.student import Student
from app.models.skill import Skill
from app.models.verification import Verification, VerificationStatus
from app.schemas.verification import (
    VerificationCreate, VerificationUpdate, VerificationResponse, VerificationWithDetails,
    VerificationRequest, StudentVerificationProfile
)
from app.services.verification import VerificationService


router = APIRouter(prefix="/verifications", tags=["Verifications"])


@router.post("", response_model=VerificationResponse, status_code=status.HTTP_201_CREATED)
async def create_verification(
    verification_data: VerificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "school_admin"))
):
    """
    Create a new verification.

    Only teachers and school admins can create verifications manually.
    AI-generated verifications are created automatically through the system.
    """
    verification = await VerificationService.create_verification(
        student_id=verification_data.student_id,
        skill_id=verification_data.skill_id,
        source=verification_data.source,
        db=db,
        score=verification_data.score,
        evidence=verification_data.evidence,
        notes=verification_data.notes,
        module_id=verification_data.module_id,
        task_id=verification_data.task_id,
        verified_by_user_id=verification_data.verified_by_user_id or current_user.id,
        auto_approve=True  # Teacher-created verifications are auto-approved
    )

    return verification


@router.get("/me/verifications", response_model=StudentVerificationProfile)
async def get_my_verifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    """Get current student's complete verification profile."""
    # Get student
    student_result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # Get all verifications
    verifications = await VerificationService.get_student_verifications(
        student_id=student.id,
        db=db
    )

    # Get skill details for each verification
    verifications_with_details = []
    verified_skills = set()
    pending_count = 0

    for verification in verifications:
        # Get skill
        skill_result = await db.execute(
            select(Skill).where(Skill.id == verification.skill_id)
        )
        skill = skill_result.scalar_one_or_none()

        if skill:
            verifications_with_details.append(VerificationWithDetails(
                id=verification.id,
                student_id=verification.student_id,
                skill_id=verification.skill_id,
                source=verification.source,
                score=verification.score,
                evidence=verification.evidence,
                notes=verification.notes,
                expires_at=verification.expires_at,
                module_id=verification.module_id,
                task_id=verification.task_id,
                status=verification.status,
                verified_by_user_id=verification.verified_by_user_id,
                verified_at=verification.verified_at,
                is_valid=verification.is_valid,
                created_at=verification.created_at,
                updated_at=verification.updated_at,
                skill_name=skill.name,
                skill_category=skill.category.value
            ))

            if verification.status == VerificationStatus.VERIFIED:
                verified_skills.add(verification.skill_id)
            elif verification.status == VerificationStatus.PENDING:
                pending_count += 1

    return StudentVerificationProfile(
        student_id=student.id,
        total_verifications=len(verifications),
        verified_skills_count=len(verified_skills),
        pending_verifications_count=pending_count,
        verifications=verifications_with_details
    )


@router.get("/student/{student_id}/verifications", response_model=list[VerificationResponse])
async def get_student_verifications(
    student_id: UUID,
    skill_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "parent", "school_admin"))
):
    """
    Get verifications for a specific student.

    Only teachers, parents, and school admins can access this.
    Teachers and parents should only see students they're associated with (TODO: add authorization).
    """
    # TODO: Add authorization check
    verifications = await VerificationService.get_student_verifications(
        student_id=student_id,
        db=db,
        skill_id=skill_id
    )

    return verifications


@router.get("/{verification_id}", response_model=VerificationResponse)
async def get_verification(
    verification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific verification by ID."""
    result = await db.execute(
        select(Verification).where(Verification.id == verification_id)
    )
    verification = result.scalar_one_or_none()

    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")

    # TODO: Add authorization check (students can only see their own, teachers their students, etc.)

    return verification


@router.put("/{verification_id}", response_model=VerificationResponse)
async def update_verification(
    verification_id: UUID,
    verification_data: VerificationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "school_admin"))
):
    """
    Update a verification status or details.

    Only teachers and school admins can update verifications.
    """
    result = await db.execute(
        select(Verification).where(Verification.id == verification_id)
    )
    verification = result.scalar_one_or_none()

    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")

    # Update fields
    for field, value in verification_data.model_dump(exclude_unset=True).items():
        setattr(verification, field, value)

    # If status changed to VERIFIED, update skill score
    if verification_data.status == VerificationStatus.VERIFIED and verification.status != VerificationStatus.VERIFIED:
        verification.verified_at = datetime.utcnow()
        await VerificationService.update_skill_score_from_verification(
            verification=verification,
            db=db
        )

    await db.commit()
    await db.refresh(verification)

    return verification


@router.post("/teacher-review", response_model=VerificationResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher_review_verification(
    request: VerificationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher"))
):
    """
    Create a verification based on teacher manual review.

    This endpoint allows teachers to verify a student's skill competency
    after reviewing their work or observing their performance.
    """
    verification = await VerificationService.verify_from_teacher_review(
        student_id=request.student_id,
        skill_id=request.skill_id,
        teacher_user_id=current_user.id,
        score=request.score or 75.0,
        notes=request.notes or "Teacher verified competency",
        db=db,
        task_id=request.task_id
    )

    return verification


# Import datetime for update endpoint
from datetime import datetime
