"""
CurriculumService for managing learning content ingestion and recommendations.

Supports multiple content sources:
1. School internal systems
2. Teacher uploads
3. Public open educational resources (OER)
4. AI-assisted content generation
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.curriculum import LearningResource, SourceType, ResourceType
from app.models.student import Student
from app.models.skill import Skill, SkillScore
from app.schemas.curriculum import ResourceRecommendation


class CurriculumService:
    """Service for curriculum content management and recommendations"""

    @staticmethod
    async def ingest_resource(
        resource_data: dict,
        db: AsyncSession,
        created_by_user_id: Optional[UUID] = None
    ) -> LearningResource:
        """
        Ingest a new learning resource into the system.

        Args:
            resource_data: Dictionary with resource information
            db: Database session
            created_by_user_id: ID of user creating the resource

        Returns:
            Created LearningResource
        """
        resource = LearningResource(
            **resource_data,
            created_by_user_id=created_by_user_id
        )

        db.add(resource)
        await db.commit()
        await db.refresh(resource)

        return resource

    @staticmethod
    async def link_resource_to_skills(
        resource_id: UUID,
        skill_ids: List[UUID],
        db: AsyncSession
    ) -> LearningResource:
        """
        Link a resource to one or more skills.

        Args:
            resource_id: ID of the resource
            skill_ids: List of skill IDs to link
            db: Database session

        Returns:
            Updated LearningResource
        """
        # Get resource
        resource_result = await db.execute(
            select(LearningResource)
            .options(selectinload(LearningResource.skills))
            .where(LearningResource.id == resource_id)
        )
        resource = resource_result.scalar_one_or_none()

        if not resource:
            return None

        # Get skills
        skills_result = await db.execute(
            select(Skill).where(Skill.id.in_(skill_ids))
        )
        skills = skills_result.scalars().all()

        # Link skills to resource
        for skill in skills:
            if skill not in resource.skills:
                resource.skills.append(skill)

        await db.commit()
        await db.refresh(resource)

        return resource

    @staticmethod
    async def get_recommended_resources_for_student(
        student_id: UUID,
        db: AsyncSession,
        limit: int = 5
    ) -> List[ResourceRecommendation]:
        """
        Get AI-powered recommended resources for a student.

        Recommendation strategy:
        1. Identify student's weak skills (score < 60)
        2. Find resources that teach those skills
        3. Prioritize by:
           - Skill weakness (lower scores = higher priority)
           - Resource quality score
           - Age/grade appropriateness
           - Resource type variety

        Args:
            student_id: ID of the student
            db: Database session
            limit: Maximum number of recommendations

        Returns:
            List of ResourceRecommendation objects
        """
        # Get student
        student_result = await db.execute(
            select(Student).where(Student.id == student_id)
        )
        student = student_result.scalar_one_or_none()

        if not student:
            return []

        # Get weak skills (score < 60)
        weak_skills_result = await db.execute(
            select(SkillScore, Skill)
            .join(Skill, SkillScore.skill_id == Skill.id)
            .where(SkillScore.student_id == student_id)
            .where(SkillScore.score < 60)
            .order_by(SkillScore.score.asc())
            .limit(5)
        )
        weak_skills_data = weak_skills_result.all()

        if not weak_skills_data:
            # Student has no weak skills - recommend resources for skill expansion
            return await CurriculumService._get_expansion_recommendations(
                student=student,
                db=db,
                limit=limit
            )

        # Get skill IDs that need work
        weak_skill_ids = [skill.id for _, skill in weak_skills_data]

        # Find resources that teach these skills
        resources_result = await db.execute(
            select(LearningResource)
            .join(LearningResource.skills)
            .where(
                and_(
                    Skill.id.in_(weak_skill_ids),
                    LearningResource.is_active == True
                )
            )
            .options(selectinload(LearningResource.skills))
            .distinct()
            .limit(limit * 2)  # Get more than needed for filtering
        )
        resources = resources_result.scalars().all()

        # Build recommendations
        recommendations = []
        for resource in resources:
            # Check if resource is age-appropriate
            if resource.age_min and student.grade_level:
                # Rough age estimation from grade (grade + 5)
                student_age = int(student.grade_level) + 5 if student.grade_level.isdigit() else 10
                if student_age < resource.age_min or (resource.age_max and student_age > resource.age_max):
                    continue

            # Find which weak skills this resource addresses
            resource_skill_ids = {skill.id for skill in resource.skills}
            addressed_weak_skills = [
                skill for score, skill in weak_skills_data
                if skill.id in resource_skill_ids
            ]

            if not addressed_weak_skills:
                continue

            # Calculate relevance score based on:
            # 1. How many weak skills it addresses (more = better)
            # 2. Quality score of resource
            # 3. How weak the skills are (weaker = more relevant)
            avg_skill_weakness = sum(
                100 - score.score for score, skill in weak_skills_data
                if skill.id in resource_skill_ids
            ) / len(addressed_weak_skills)

            relevance_score = (
                (len(addressed_weak_skills) / len(weak_skill_ids)) * 0.4 +  # Coverage
                ((resource.quality_score or 50) / 100) * 0.3 +  # Quality
                (avg_skill_weakness / 100) * 0.3  # Weakness
            )

            # Generate reason
            skill_names = [skill.name for skill in addressed_weak_skills[:2]]
            reason = f"This resource helps you practice {', '.join(skill_names)}"
            if len(addressed_weak_skills) > 2:
                reason += f" and {len(addressed_weak_skills) - 2} more skills you're working on"

            recommendations.append(ResourceRecommendation(
                resource_id=resource.id,
                title=resource.title,
                resource_type=resource.resource_type.value,
                estimated_minutes=resource.estimated_minutes,
                relevance_score=min(1.0, relevance_score),
                reason=reason,
                target_skills=[skill.name for skill in addressed_weak_skills]
            ))

        # Sort by relevance score and return top recommendations
        recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
        return recommendations[:limit]

    @staticmethod
    async def _get_expansion_recommendations(
        student: Student,
        db: AsyncSession,
        limit: int = 5
    ) -> List[ResourceRecommendation]:
        """
        Get recommendations for skill expansion (when student has no weak skills).

        Recommends resources that teach new skills the student hasn't learned yet.
        """
        # Get skills student already has scores for
        student_skill_ids_result = await db.execute(
            select(SkillScore.skill_id).where(SkillScore.student_id == student.id)
        )
        student_skill_ids = [row[0] for row in student_skill_ids_result.all()]

        # Find resources for skills student hasn't learned
        resources_result = await db.execute(
            select(LearningResource)
            .join(LearningResource.skills)
            .where(
                and_(
                    LearningResource.is_active == True,
                    Skill.id.notin_(student_skill_ids) if student_skill_ids else True
                )
            )
            .options(selectinload(LearningResource.skills))
            .distinct()
            .limit(limit)
        )
        resources = resources_result.scalars().all()

        recommendations = []
        for resource in resources:
            new_skills = [skill for skill in resource.skills if skill.id not in student_skill_ids]

            if new_skills:
                skill_names = [skill.name for skill in new_skills[:2]]
                reason = f"Ready to learn something new? This introduces {', '.join(skill_names)}"

                recommendations.append(ResourceRecommendation(
                    resource_id=resource.id,
                    title=resource.title,
                    resource_type=resource.resource_type.value,
                    estimated_minutes=resource.estimated_minutes,
                    relevance_score=0.7,  # Default relevance for expansion
                    reason=reason,
                    target_skills=[skill.name for skill in new_skills]
                ))

        return recommendations

    @staticmethod
    async def ingest_from_public_source(
        content_data: dict,
        db: AsyncSession
    ) -> LearningResource:
        """
        Ingest content from public open educational resources.

        This is a stub for future implementation that would:
        1. Connect to OER APIs (Khan Academy, OpenStax, etc.)
        2. Parse and normalize content
        3. Auto-tag with subjects, skills, age groups
        4. Store in system

        Args:
            content_data: Dictionary with content from external source
            db: Database session

        Returns:
            Created LearningResource
        """
        # TODO: Implement actual OER API integration
        resource_data = {
            "title": content_data.get("title", "Untitled Resource"),
            "description": content_data.get("description"),
            "resource_type": ResourceType.EXTERNAL_LINK,
            "url": content_data.get("url"),
            "source_type": SourceType.PUBLIC_OPEN_CONTENT,
            "source_attribution": content_data.get("author") or content_data.get("platform"),
            "source_url": content_data.get("original_url"),
            "license_type": content_data.get("license", "Unknown"),
            "is_public": True,
            "subject": content_data.get("subject"),
            "language": content_data.get("language", "en")
        }

        return await CurriculumService.ingest_resource(resource_data, db)

    @staticmethod
    async def auto_tag_resource(
        resource_id: UUID,
        db: AsyncSession
    ) -> LearningResource:
        """
        Automatically tag a resource with skills based on its content.

        This is a stub for future AI-powered content analysis that would:
        1. Analyze resource title, description, content
        2. Use NLP/LLM to identify relevant skills
        3. Suggest appropriate age/grade levels
        4. Assign difficulty level

        Args:
            resource_id: ID of the resource to tag
            db: Database session

        Returns:
            Updated LearningResource
        """
        # TODO: Implement AI-powered auto-tagging
        resource_result = await db.execute(
            select(LearningResource).where(LearningResource.id == resource_id)
        )
        resource = resource_result.scalar_one_or_none()

        if resource:
            # Placeholder: In production, use LLM to analyze content and suggest tags
            resource.resource_metadata = resource.resource_metadata or {}
            resource.resource_metadata["auto_tagged"] = True
            resource.resource_metadata["needs_review"] = True

            await db.commit()
            await db.refresh(resource)

        return resource

    @staticmethod
    async def search_resources(
        db: AsyncSession,
        query: Optional[str] = None,
        subject: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
        grade_min: Optional[int] = None,
        grade_max: Optional[int] = None,
        source_type: Optional[SourceType] = None,
        is_public: Optional[bool] = None,
        school_id: Optional[UUID] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[LearningResource]:
        """
        Search for learning resources with filters.

        Args:
            db: Database session
            query: Text search in title/description
            subject: Filter by subject
            resource_type: Filter by resource type
            grade_min/grade_max: Filter by grade range
            source_type: Filter by source
            is_public: Filter by public/private
            school_id: Filter by school
            limit: Max results
            offset: Pagination offset

        Returns:
            List of matching LearningResource objects
        """
        filters = [LearningResource.is_active == True]

        if query:
            search_term = f"%{query}%"
            filters.append(
                or_(
                    LearningResource.title.ilike(search_term),
                    LearningResource.description.ilike(search_term)
                )
            )

        if subject:
            filters.append(LearningResource.subject == subject)

        if resource_type:
            filters.append(LearningResource.resource_type == resource_type)

        if grade_min is not None:
            filters.append(
                or_(
                    LearningResource.grade_min == None,
                    LearningResource.grade_min <= grade_min
                )
            )

        if grade_max is not None:
            filters.append(
                or_(
                    LearningResource.grade_max == None,
                    LearningResource.grade_max >= grade_max
                )
            )

        if source_type:
            filters.append(LearningResource.source_type == source_type)

        if is_public is not None:
            filters.append(LearningResource.is_public == is_public)

        if school_id:
            filters.append(LearningResource.school_id == school_id)

        result = await db.execute(
            select(LearningResource)
            .where(and_(*filters))
            .order_by(LearningResource.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return result.scalars().all()
