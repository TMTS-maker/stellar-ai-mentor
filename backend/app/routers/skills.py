"""
API router for Skills and SkillScores (LVO - LEARN phase).
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
from app.models.skill import Skill, SkillScore
from app.schemas.skill import (
    SkillCreate, SkillUpdate, SkillResponse,
    SkillScoreResponse, SkillScoreWithSkill,
    StudentSkillsProfile
)


router = APIRouter(prefix="/skills", tags=["Skills"])


@router.post("", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill_data: SkillCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("school_admin", "teacher"))
):
    """Create a new skill. Only school_admin or teacher can create skills."""
    skill = Skill(**skill_data.model_dump())
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return skill


@router.get("", response_model=list[SkillResponse])
async def list_skills(
    category: str | None = None,
    level: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all skills, optionally filtered by category and level."""
    query = select(Skill)

    if category:
        query = query.where(Skill.category == category)
    if level:
        query = query.where(Skill.level == level)

    query = query.offset(skip).limit(limit).order_by(Skill.name.asc())

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(
    skill_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific skill by ID."""
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return skill


@router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: UUID,
    skill_data: SkillUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("school_admin", "teacher"))
):
    """Update a skill. Only school_admin or teacher can update skills."""
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Update fields
    for field, value in skill_data.model_dump(exclude_unset=True).items():
        setattr(skill, field, value)

    await db.commit()
    await db.refresh(skill)
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("school_admin"))
):
    """Delete a skill. Only school_admin can delete skills."""
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    await db.delete(skill)
    await db.commit()


# ============================================================================
# Student Skill Scores
# ============================================================================

@router.get("/me/skills", response_model=StudentSkillsProfile)
async def get_my_skills(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    """Get current student's complete skills profile."""
    # Get student
    student_result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # Get all skill scores with skill details
    skill_scores_result = await db.execute(
        select(SkillScore, Skill)
        .join(Skill, SkillScore.skill_id == Skill.id)
        .where(SkillScore.student_id == student.id)
        .order_by(SkillScore.score.desc())
    )
    skill_scores_data = skill_scores_result.all()

    # Build skill scores with skill details
    skill_scores = []
    mastered = 0
    proficient = 0
    developing = 0
    beginner = 0

    for score, skill in skill_scores_data:
        skill_score_with_skill = SkillScoreWithSkill(
            id=score.id,
            student_id=score.student_id,
            skill_id=score.skill_id,
            score=score.score,
            confidence=score.confidence,
            assessment_count=score.assessment_count,
            last_practiced_at=score.last_practiced_at,
            proficiency_level=score.proficiency_level,
            created_at=score.created_at,
            updated_at=score.updated_at,
            skill=SkillResponse(
                id=skill.id,
                name=skill.name,
                description=skill.description,
                category=skill.category,
                level=skill.level,
                age_group_min=skill.age_group_min,
                age_group_max=skill.age_group_max,
                created_at=skill.created_at,
                updated_at=skill.updated_at
            )
        )
        skill_scores.append(skill_score_with_skill)

        # Count by proficiency level
        if score.score >= 80:
            mastered += 1
        elif score.score >= 60:
            proficient += 1
        elif score.score >= 30:
            developing += 1
        else:
            beginner += 1

    return StudentSkillsProfile(
        student_id=student.id,
        total_skills=len(skill_scores),
        mastered_skills=mastered,
        proficient_skills=proficient,
        developing_skills=developing,
        beginner_skills=beginner,
        skill_scores=skill_scores
    )


@router.get("/student/{student_id}/skills", response_model=list[SkillScoreWithSkill])
async def get_student_skills(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "parent", "school_admin"))
):
    """Get a student's skill scores. Only teacher, parent, or school_admin can access."""
    # TODO: Add authorization check (teacher must teach this student, parent must be linked, etc.)

    skill_scores_result = await db.execute(
        select(SkillScore, Skill)
        .join(Skill, SkillScore.skill_id == Skill.id)
        .where(SkillScore.student_id == student_id)
        .order_by(SkillScore.score.desc())
    )
    skill_scores_data = skill_scores_result.all()

    # Build response
    result = []
    for score, skill in skill_scores_data:
        result.append(SkillScoreWithSkill(
            id=score.id,
            student_id=score.student_id,
            skill_id=score.skill_id,
            score=score.score,
            confidence=score.confidence,
            assessment_count=score.assessment_count,
            last_practiced_at=score.last_practiced_at,
            proficiency_level=score.proficiency_level,
            created_at=score.created_at,
            updated_at=score.updated_at,
            skill=SkillResponse.model_validate(skill)
        ))

    return result
