"""
API router for Curriculum management (content ingestion and recommendations).
"""

from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.auth import get_current_user, require_role
from app.models.user import User
from app.models.student import Student
from app.models.curriculum import ResourceType, SourceType
from app.schemas.curriculum import (
    LearningResourceCreate, LearningResourceUpdate, LearningResourceResponse,
    LearningResourceWithSkills, StudentResourceRecommendations, ResourceRecommendation
)
from app.services.curriculum import CurriculumService


router = APIRouter(prefix="/curriculum", tags=["Curriculum"])


@router.post("/resources", response_model=LearningResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_learning_resource(
    resource_data: LearningResourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "school_admin"))
):
    """
    Create a new learning resource.

    Only teachers and school admins can create resources.
    """
    resource_dict = resource_data.model_dump(exclude={"skill_ids"})
    resource = await CurriculumService.ingest_resource(
        resource_data=resource_dict,
        db=db,
        created_by_user_id=current_user.id
    )

    # Link skills if provided
    if resource_data.skill_ids:
        resource = await CurriculumService.link_resource_to_skills(
            resource_id=resource.id,
            skill_ids=resource_data.skill_ids,
            db=db
        )

    return resource


@router.get("/resources", response_model=List[LearningResourceResponse])
async def list_learning_resources(
    query: Optional[str] = Query(None, description="Search in title/description"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    resource_type: Optional[ResourceType] = Query(None, description="Filter by resource type"),
    source_type: Optional[SourceType] = Query(None, description="Filter by source type"),
    grade_min: Optional[int] = Query(None, ge=0, le=12, description="Minimum grade level"),
    grade_max: Optional[int] = Query(None, ge=0, le=12, description="Maximum grade level"),
    is_public: Optional[bool] = Query(None, description="Filter by public/private"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search and list learning resources with filters.
    """
    # If not admin/teacher, only show public resources or resources from their school
    school_id = None
    if current_user.role in ["student", "parent"]:
        # Get student's school
        from sqlalchemy import select
        if current_user.role == "student":
            result = await db.execute(
                select(Student).where(Student.user_id == current_user.id)
            )
            student = result.scalar_one_or_none()
            if student:
                school_id = student.school_id

    resources = await CurriculumService.search_resources(
        db=db,
        query=query,
        subject=subject,
        resource_type=resource_type,
        grade_min=grade_min,
        grade_max=grade_max,
        source_type=source_type,
        is_public=is_public,
        school_id=school_id,
        limit=limit,
        offset=offset
    )

    return resources


@router.get("/resources/{resource_id}", response_model=LearningResourceWithSkills)
async def get_learning_resource(
    resource_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific learning resource by ID."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    result = await db.execute(
        select(CurriculumService.model.LearningResource)
        .options(selectinload(CurriculumService.model.LearningResource.skills))
        .where(CurriculumService.model.LearningResource.id == resource_id)
    )
    resource = result.scalar_one_or_none()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Build response with skill IDs
    response_dict = {
        **resource.__dict__,
        "skill_ids": [skill.id for skill in resource.skills]
    }

    return response_dict


@router.put("/resources/{resource_id}", response_model=LearningResourceResponse)
async def update_learning_resource(
    resource_id: UUID,
    resource_data: LearningResourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "school_admin"))
):
    """Update a learning resource. Only teachers and school admins can update."""
    from sqlalchemy import select
    from app.models.curriculum import LearningResource

    result = await db.execute(
        select(LearningResource).where(LearningResource.id == resource_id)
    )
    resource = result.scalar_one_or_none()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Update fields
    for field, value in resource_data.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)

    await db.commit()
    await db.refresh(resource)

    return resource


@router.post("/resources/{resource_id}/skills", response_model=LearningResourceWithSkills)
async def link_resource_to_skills(
    resource_id: UUID,
    skill_ids: List[UUID],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "school_admin"))
):
    """
    Link a resource to skills.

    This maps the resource to specific skills it teaches, enabling
    skill-based recommendations.
    """
    resource = await CurriculumService.link_resource_to_skills(
        resource_id=resource_id,
        skill_ids=skill_ids,
        db=db
    )

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    return {
        **resource.__dict__,
        "skill_ids": [skill.id for skill in resource.skills]
    }


@router.get("/me/recommended", response_model=StudentResourceRecommendations)
async def get_my_recommended_resources(
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    """
    Get AI-powered recommended learning resources for current student.

    Recommendations are based on:
    - Student's weak skills (skills needing practice)
    - Age and grade appropriateness
    - Resource quality and engagement metrics
    - Variety of resource types

    This is a key feature of the LEARN phase in the LVO architecture.
    """
    from sqlalchemy import select

    # Get student
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # Get recommendations
    recommendations = await CurriculumService.get_recommended_resources_for_student(
        student_id=student.id,
        db=db,
        limit=limit
    )

    return StudentResourceRecommendations(
        student_id=student.id,
        recommendations=recommendations
    )


@router.post("/ingest/public", response_model=LearningResourceResponse, status_code=status.HTTP_201_CREATED)
async def ingest_from_public_source(
    content_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("school_admin"))
):
    """
    Ingest content from public open educational resources.

    This endpoint allows school admins to pull content from external OER sources.
    Future implementation will support APIs from Khan Academy, OpenStax, etc.
    """
    resource = await CurriculumService.ingest_from_public_source(
        content_data=content_data,
        db=db
    )

    return resource
