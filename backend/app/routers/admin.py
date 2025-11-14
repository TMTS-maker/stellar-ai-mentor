"""
Admin router for school administrators and teachers

Provides comprehensive management endpoints for:
- Students (LVO profiles, progress tracking)
- Resources (curriculum content management)
- Skills (skill management and mapping)
- Learning Paths (path and module management)
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import get_current_user, require_role
from app.db import get_db
from app.models.user import User
from app.models.student import Student
from app.models.skill import Skill, SkillScore
from app.models.learning_path import LearningPath, LearningModule, StudentLearningPath, StudentModule
from app.models.verification import Verification
from app.models.credential import Credential
from app.models.gamification import XPEvent, Badge, StudentBadge
from app.models.curriculum import LearningResource
from app.schemas.skill import SkillResponse, SkillCreate, SkillUpdate
from app.schemas.learning_path import LearningPathResponse, LearningPathCreate
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])


# ============================================================================
# SCHEMAS
# ============================================================================

class AdminStatsResponse(BaseModel):
    """Overview statistics for admin dashboard"""
    total_students: int
    total_teachers: int
    total_classrooms: int
    total_skills: int
    total_learning_paths: int
    total_resources: int
    active_students_last_week: int
    total_credentials_issued: int
    total_xp_earned: int


class StudentLVOProfile(BaseModel):
    """Comprehensive student LVO profile"""
    student_id: UUID
    student_name: str
    email: str
    grade_level: int

    # XP and Level
    total_xp: int
    current_level: int

    # Skills
    skill_scores: List[dict]
    weak_skills: List[dict]  # Skills < 60
    strong_skills: List[dict]  # Skills >= 80

    # Learning Paths
    learning_paths: List[dict]
    active_modules: List[dict]

    # Verifications
    verifications_count: int
    recent_verifications: List[dict]

    # Credentials
    credentials_count: int
    recent_credentials: List[dict]

    # Badges
    badges_earned: List[dict]

    # Recommendations
    recommended_resources: List[dict]


class StudentListItem(BaseModel):
    """Student list item for admin view"""
    student_id: UUID
    name: str
    email: str
    grade_level: int
    total_xp: int
    current_level: int
    weak_skills_count: int
    credentials_count: int
    last_active: Optional[str] = None


class ResourceManagementResponse(BaseModel):
    """Resource with admin metadata"""
    id: UUID
    title: str
    resource_type: str
    source_type: str
    subject: Optional[str]
    grade_min: Optional[int]
    grade_max: Optional[int]
    quality_score: Optional[int]
    view_count: int
    completion_count: int
    is_active: bool
    skills_count: int
    created_at: str


# ============================================================================
# DASHBOARD & STATS
# ============================================================================

@router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Get overview statistics for admin dashboard"""

    # Count students
    students_result = await db.execute(select(func.count(Student.user_id)))
    total_students = students_result.scalar()

    # Count teachers (would need Teacher model count)
    total_teachers = 0  # Placeholder

    # Count classrooms
    total_classrooms = 0  # Placeholder

    # Count skills
    skills_result = await db.execute(select(func.count(Skill.id)))
    total_skills = skills_result.scalar()

    # Count learning paths
    paths_result = await db.execute(select(func.count(LearningPath.id)))
    total_learning_paths = paths_result.scalar()

    # Count resources
    resources_result = await db.execute(select(func.count(LearningResource.id)))
    total_resources = resources_result.scalar()

    # Active students last week (placeholder)
    active_students_last_week = total_students  # Would need proper query

    # Count credentials
    credentials_result = await db.execute(select(func.count(Credential.id)))
    total_credentials_issued = credentials_result.scalar()

    # Sum total XP
    xp_result = await db.execute(select(func.sum(XPEvent.amount)))
    total_xp_earned = xp_result.scalar() or 0

    return AdminStatsResponse(
        total_students=total_students or 0,
        total_teachers=total_teachers,
        total_classrooms=total_classrooms,
        total_skills=total_skills or 0,
        total_learning_paths=total_learning_paths or 0,
        total_resources=total_resources or 0,
        active_students_last_week=active_students_last_week or 0,
        total_credentials_issued=total_credentials_issued or 0,
        total_xp_earned=total_xp_earned,
    )


# ============================================================================
# STUDENT MANAGEMENT
# ============================================================================

@router.get("/students", response_model=List[StudentListItem])
async def list_students(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """List all students with summary data"""

    # Get students with user data
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.user))
        .limit(limit)
        .offset(offset)
    )
    students = result.scalars().all()

    student_list = []

    for student in students:
        # Get total XP
        xp_result = await db.execute(
            select(func.sum(XPEvent.amount))
            .where(XPEvent.student_id == student.user_id)
        )
        total_xp = xp_result.scalar() or 0

        # Calculate level (100 XP per level)
        current_level = total_xp // 100

        # Count weak skills (score < 60)
        weak_skills_result = await db.execute(
            select(func.count(SkillScore.id))
            .where(
                and_(
                    SkillScore.student_id == student.user_id,
                    SkillScore.score < 60
                )
            )
        )
        weak_skills_count = weak_skills_result.scalar() or 0

        # Count credentials
        credentials_result = await db.execute(
            select(func.count(Credential.id))
            .where(Credential.student_id == student.user_id)
        )
        credentials_count = credentials_result.scalar() or 0

        student_list.append(StudentListItem(
            student_id=student.user_id,
            name=student.user.full_name,
            email=student.user.email,
            grade_level=student.grade_level,
            total_xp=total_xp,
            current_level=current_level,
            weak_skills_count=weak_skills_count,
            credentials_count=credentials_count,
        ))

    return student_list


@router.get("/students/{student_id}/lvo-profile", response_model=StudentLVOProfile)
async def get_student_lvo_profile(
    student_id: UUID,
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive LVO profile for a student"""

    # Get student
    result = await db.execute(
        select(Student)
        .where(Student.user_id == student_id)
        .options(selectinload(Student.user))
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Get total XP and level
    xp_result = await db.execute(
        select(func.sum(XPEvent.amount))
        .where(XPEvent.student_id == student_id)
    )
    total_xp = xp_result.scalar() or 0
    current_level = total_xp // 100

    # Get skill scores
    skills_result = await db.execute(
        select(SkillScore)
        .where(SkillScore.student_id == student_id)
        .options(selectinload(SkillScore.skill))
    )
    skill_scores = skills_result.scalars().all()

    skill_scores_data = []
    weak_skills_data = []
    strong_skills_data = []

    for score in skill_scores:
        skill_data = {
            "skill_id": str(score.skill_id),
            "skill_name": score.skill.name,
            "score": score.score,
            "confidence": score.confidence,
            "assessment_count": score.assessment_count,
        }
        skill_scores_data.append(skill_data)

        if score.score < 60:
            weak_skills_data.append(skill_data)
        elif score.score >= 80:
            strong_skills_data.append(skill_data)

    # Get learning paths
    paths_result = await db.execute(
        select(StudentLearningPath)
        .where(StudentLearningPath.student_id == student_id)
        .options(selectinload(StudentLearningPath.learning_path))
    )
    student_paths = paths_result.scalars().all()

    paths_data = [
        {
            "path_id": str(path.learning_path_id),
            "path_name": path.learning_path.name,
            "status": path.status.value,
            "progress_percentage": path.progress_percentage,
        }
        for path in student_paths
    ]

    # Get active modules
    modules_result = await db.execute(
        select(StudentModule)
        .where(
            and_(
                StudentModule.student_id == student_id,
                StudentModule.status.in_(["unlocked", "in_progress"])
            )
        )
        .options(selectinload(StudentModule.module))
    )
    active_modules = modules_result.scalars().all()

    modules_data = [
        {
            "module_id": str(module.module_id),
            "module_name": module.module.name,
            "status": module.status.value,
            "score": module.score,
            "tasks_completed": module.tasks_completed,
            "tasks_total": module.tasks_total,
        }
        for module in active_modules
    ]

    # Get verifications
    verifications_result = await db.execute(
        select(Verification)
        .where(Verification.student_id == student_id)
        .options(selectinload(Verification.skill))
        .order_by(Verification.verified_at.desc())
        .limit(5)
    )
    verifications = verifications_result.scalars().all()

    verifications_data = [
        {
            "verification_id": str(v.id),
            "skill_name": v.skill.name,
            "status": v.status.value,
            "score": v.score,
            "verified_at": v.verified_at.isoformat() if v.verified_at else None,
        }
        for v in verifications
    ]

    verifications_count_result = await db.execute(
        select(func.count(Verification.id))
        .where(Verification.student_id == student_id)
    )
    verifications_count = verifications_count_result.scalar() or 0

    # Get credentials
    credentials_result = await db.execute(
        select(Credential)
        .where(Credential.student_id == student_id)
        .order_by(Credential.issued_at.desc())
        .limit(5)
    )
    credentials = credentials_result.scalars().all()

    credentials_data = [
        {
            "credential_id": str(c.id),
            "title": c.title,
            "credential_type": c.credential_type.value,
            "status": c.status.value,
            "issued_at": c.issued_at.isoformat() if c.issued_at else None,
        }
        for c in credentials
    ]

    credentials_count_result = await db.execute(
        select(func.count(Credential.id))
        .where(Credential.student_id == student_id)
    )
    credentials_count = credentials_count_result.scalar() or 0

    # Get badges
    badges_result = await db.execute(
        select(StudentBadge)
        .where(StudentBadge.student_id == student_id)
        .options(selectinload(StudentBadge.badge))
    )
    student_badges = badges_result.scalars().all()

    badges_data = [
        {
            "badge_id": str(sb.badge_id),
            "badge_name": sb.badge.name,
            "earned_at": sb.earned_at.isoformat(),
        }
        for sb in student_badges
    ]

    # Get recommended resources (based on weak skills)
    recommended_resources = []
    if weak_skills_data:
        weak_skill_ids = [UUID(skill["skill_id"]) for skill in weak_skills_data[:3]]

        resources_result = await db.execute(
            select(LearningResource)
            .join(LearningResource.skills)
            .where(Skill.id.in_(weak_skill_ids))
            .where(LearningResource.is_active == True)
            .limit(5)
        )
        resources = resources_result.scalars().all()

        recommended_resources = [
            {
                "resource_id": str(r.id),
                "title": r.title,
                "resource_type": r.resource_type.value,
                "estimated_minutes": r.estimated_minutes,
            }
            for r in resources
        ]

    return StudentLVOProfile(
        student_id=student_id,
        student_name=student.user.full_name,
        email=student.user.email,
        grade_level=student.grade_level,
        total_xp=total_xp,
        current_level=current_level,
        skill_scores=skill_scores_data,
        weak_skills=weak_skills_data,
        strong_skills=strong_skills_data,
        learning_paths=paths_data,
        active_modules=modules_data,
        verifications_count=verifications_count,
        recent_verifications=verifications_data,
        credentials_count=credentials_count,
        recent_credentials=credentials_data,
        badges_earned=badges_data,
        recommended_resources=recommended_resources,
    )


# ============================================================================
# RESOURCE MANAGEMENT
# ============================================================================

@router.get("/resources", response_model=List[ResourceManagementResponse])
async def list_resources_admin(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    subject: Optional[str] = None,
    resource_type: Optional[str] = None,
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """List all resources with admin metadata"""

    query = select(LearningResource).options(selectinload(LearningResource.skills))

    if subject:
        query = query.where(LearningResource.subject == subject)

    if resource_type:
        query = query.where(LearningResource.resource_type == resource_type)

    query = query.order_by(LearningResource.created_at.desc()).limit(limit).offset(offset)

    result = await db.execute(query)
    resources = result.scalars().all()

    resources_data = [
        ResourceManagementResponse(
            id=r.id,
            title=r.title,
            resource_type=r.resource_type.value,
            source_type=r.source_type.value,
            subject=r.subject,
            grade_min=r.grade_min,
            grade_max=r.grade_max,
            quality_score=r.quality_score,
            view_count=r.view_count,
            completion_count=r.completion_count,
            is_active=r.is_active,
            skills_count=len(r.skills),
            created_at=r.created_at.isoformat(),
        )
        for r in resources
    ]

    return resources_data


@router.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: UUID,
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Delete a resource (soft delete by setting is_active=False)"""

    result = await db.execute(
        select(LearningResource).where(LearningResource.id == resource_id)
    )
    resource = result.scalar_one_or_none()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    # Soft delete
    resource.is_active = False
    await db.commit()

    return {"message": "Resource deactivated successfully"}


# ============================================================================
# SKILL MANAGEMENT
# ============================================================================

@router.get("/skills", response_model=List[SkillResponse])
async def list_skills_admin(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    category: Optional[str] = None,
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """List all skills"""

    query = select(Skill)

    if category:
        query = query.where(Skill.category == category)

    query = query.order_by(Skill.name).limit(limit).offset(offset)

    result = await db.execute(query)
    skills = result.scalars().all()

    return skills


@router.post("/skills", response_model=SkillResponse)
async def create_skill(
    skill: SkillCreate,
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Create a new skill"""

    from datetime import datetime
    import uuid

    new_skill = Skill(
        id=uuid.uuid4(),
        **skill.dict(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(new_skill)
    await db.commit()
    await db.refresh(new_skill)

    return new_skill


# ============================================================================
# LEARNING PATH MANAGEMENT
# ============================================================================

@router.get("/learning-paths", response_model=List[LearningPathResponse])
async def list_learning_paths_admin(
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(require_role("school_admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """List all learning paths"""

    result = await db.execute(
        select(LearningPath)
        .where(LearningPath.is_active == True)
        .order_by(LearningPath.name)
        .limit(limit)
    )
    paths = result.scalars().all()

    return paths
