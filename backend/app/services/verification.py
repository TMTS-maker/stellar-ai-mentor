"""
VerificationService for managing skill verifications.

This service implements the core "VERIFY" phase of the LVO architecture.
"""

from uuid import UUID
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.student import Student
from app.models.skill import Skill, SkillScore
from app.models.verification import Verification, VerificationSource, VerificationStatus
from app.models.learning_path import LearningModule
from app.models.task import Task
from app.services.ai.llm_service import LLMService


class VerificationService:
    """Service for creating and managing skill verifications."""

    @staticmethod
    async def create_verification(
        student_id: UUID,
        skill_id: UUID,
        source: VerificationSource,
        db: AsyncSession,
        score: Optional[float] = None,
        evidence: Optional[dict] = None,
        notes: Optional[str] = None,
        module_id: Optional[UUID] = None,
        task_id: Optional[UUID] = None,
        verified_by_user_id: Optional[UUID] = None,
        auto_approve: bool = False
    ) -> Verification:
        """
        Create a new verification for a student's skill.

        Args:
            student_id: ID of the student
            skill_id: ID of the skill being verified
            source: Source of verification (AI, teacher, system, etc.)
            db: Database session
            score: Optional score (0-100)
            evidence: Optional JSON evidence
            notes: Optional notes
            module_id: Optional module that triggered verification
            task_id: Optional task that triggered verification
            verified_by_user_id: Optional ID of verifying user (for teacher reviews)
            auto_approve: If True, automatically set status to VERIFIED
        """
        # Create verification
        verification = Verification(
            student_id=student_id,
            skill_id=skill_id,
            source=source,
            status=VerificationStatus.VERIFIED if auto_approve else VerificationStatus.PENDING,
            score=score,
            evidence=evidence,
            notes=notes,
            module_id=module_id,
            task_id=task_id,
            verified_by_user_id=verified_by_user_id,
            verified_at=datetime.utcnow() if auto_approve else None
        )

        db.add(verification)
        await db.commit()
        await db.refresh(verification)

        # Update skill score if verification is approved
        if verification.status == VerificationStatus.VERIFIED:
            await VerificationService.update_skill_score_from_verification(
                verification=verification,
                db=db
            )

        return verification

    @staticmethod
    async def verify_from_ai_assessment(
        student_id: UUID,
        skill_id: UUID,
        conversation_id: str,
        assessment_text: str,
        db: AsyncSession,
        task_id: Optional[UUID] = None,
        module_id: Optional[UUID] = None
    ) -> Optional[Verification]:
        """
        Create verification from AI assessment of student work.

        Uses LLM to analyze conversation and determine if skill was demonstrated.

        Args:
            student_id: ID of the student
            skill_id: ID of the skill
            conversation_id: ID of the conversation session
            assessment_text: Student's response/work to assess
            db: Database session
            task_id: Optional task ID
            module_id: Optional module ID

        Returns:
            Verification if student demonstrated competency, None otherwise
        """
        # Get skill details
        skill_result = await db.execute(
            select(Skill).where(Skill.id == skill_id)
        )
        skill = skill_result.scalar_one_or_none()
        if not skill:
            return None

        # Use AI to assess competency
        competency_score, reasoning = await VerificationService._ai_assess_skill(
            skill=skill,
            student_response=assessment_text
        )

        # Only create verification if student demonstrated competency (score >= 60)
        if competency_score >= 60:
            evidence = {
                "conversation_id": conversation_id,
                "assessment_text": assessment_text[:500],  # Truncate for storage
                "ai_reasoning": reasoning,
                "ai_score": competency_score
            }

            return await VerificationService.create_verification(
                student_id=student_id,
                skill_id=skill_id,
                source=VerificationSource.AI_ASSESSMENT,
                db=db,
                score=competency_score,
                evidence=evidence,
                notes=f"AI Assessment: {reasoning}",
                module_id=module_id,
                task_id=task_id,
                auto_approve=True  # AI assessments are automatically approved
            )

        return None

    @staticmethod
    async def verify_from_module_completion(
        student_id: UUID,
        module_id: UUID,
        module_score: float,
        db: AsyncSession
    ) -> list[Verification]:
        """
        Create verifications for all skills in a module upon completion.

        Args:
            student_id: ID of the student
            module_id: ID of the completed module
            module_score: Score achieved in the module
            db: Database session

        Returns:
            List of created verifications
        """
        # Get module and associated skills
        module_result = await db.execute(
            select(LearningModule).where(LearningModule.id == module_id)
        )
        module = module_result.scalar_one_or_none()
        if not module or not module.skill_ids:
            return []

        verifications = []
        for skill_id_str in module.skill_ids:
            skill_id = UUID(skill_id_str)

            evidence = {
                "module_id": str(module_id),
                "module_name": module.name,
                "module_score": module_score,
                "completion_date": datetime.utcnow().isoformat()
            }

            verification = await VerificationService.create_verification(
                student_id=student_id,
                skill_id=skill_id,
                source=VerificationSource.SYSTEM_CHECK,
                db=db,
                score=module_score,
                evidence=evidence,
                notes=f"Module '{module.name}' completed with score {module_score:.0f}%",
                module_id=module_id,
                auto_approve=True
            )
            verifications.append(verification)

        return verifications

    @staticmethod
    async def verify_from_teacher_review(
        student_id: UUID,
        skill_id: UUID,
        teacher_user_id: UUID,
        score: float,
        notes: str,
        db: AsyncSession,
        task_id: Optional[UUID] = None
    ) -> Verification:
        """
        Create verification from teacher manual review.

        Args:
            student_id: ID of the student
            skill_id: ID of the skill
            teacher_user_id: ID of the teacher
            score: Teacher's assessment score (0-100)
            notes: Teacher's notes
            db: Database session
            task_id: Optional task ID

        Returns:
            Created verification
        """
        evidence = {
            "teacher_id": str(teacher_user_id),
            "review_date": datetime.utcnow().isoformat()
        }

        return await VerificationService.create_verification(
            student_id=student_id,
            skill_id=skill_id,
            source=VerificationSource.TEACHER_REVIEW,
            db=db,
            score=score,
            evidence=evidence,
            notes=notes,
            task_id=task_id,
            verified_by_user_id=teacher_user_id,
            auto_approve=True  # Teacher reviews are automatically approved
        )

    @staticmethod
    async def update_skill_score_from_verification(
        verification: Verification,
        db: AsyncSession
    ) -> SkillScore:
        """
        Update student's skill score based on a new verification.

        Uses weighted averaging to incorporate new evidence.
        """
        # Get existing skill score
        skill_score_result = await db.execute(
            select(SkillScore)
            .where(
                and_(
                    SkillScore.student_id == verification.student_id,
                    SkillScore.skill_id == verification.skill_id
                )
            )
        )
        skill_score = skill_score_result.scalar_one_or_none()

        if not skill_score:
            # Create new skill score
            skill_score = SkillScore(
                student_id=verification.student_id,
                skill_id=verification.skill_id,
                score=verification.score or 60.0,  # Default to proficient if no score
                confidence=0.7,
                assessment_count=1,
                last_practiced_at=datetime.utcnow()
            )
            db.add(skill_score)
        else:
            # Update existing score using weighted average
            # More assessments = higher confidence in the score
            old_weight = min(skill_score.assessment_count, 5)  # Cap at 5 for stability
            new_score = verification.score or skill_score.score

            weighted_score = (
                (skill_score.score * old_weight) + new_score
            ) / (old_weight + 1)

            skill_score.score = weighted_score
            skill_score.assessment_count += 1
            skill_score.confidence = min(0.95, skill_score.confidence + 0.05)  # Increase confidence
            skill_score.last_practiced_at = datetime.utcnow()
            skill_score.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(skill_score)

        return skill_score

    @staticmethod
    async def _ai_assess_skill(
        skill: Skill,
        student_response: str
    ) -> tuple[float, str]:
        """
        Use AI to assess if student demonstrated a skill.

        Returns:
            Tuple of (competency_score, reasoning)
        """
        try:
            prompt = f"""You are an educational AI assessing student competency.

Skill to assess: {skill.name}
Description: {skill.description or "N/A"}
Category: {skill.category.value}
Level: {skill.level or "General"}

Student's response:
{student_response[:1000]}

Assess whether the student demonstrated this skill. Respond in this exact format:
SCORE: <number 0-100>
REASONING: <brief explanation in one sentence>

Be encouraging but honest. Score 60+ means competency demonstrated."""

            messages = [{"role": "user", "content": prompt}]
            response = await LLMService.generate_response(messages, max_tokens=150)

            # Parse response
            score = 50.0  # Default
            reasoning = "Assessment could not be completed"

            lines = response.strip().split('\n')
            for line in lines:
                if line.startswith("SCORE:"):
                    try:
                        score = float(line.replace("SCORE:", "").strip())
                        score = max(0, min(100, score))  # Clamp to 0-100
                    except ValueError:
                        pass
                elif line.startswith("REASONING:"):
                    reasoning = line.replace("REASONING:", "").strip()

            return score, reasoning

        except Exception as e:
            # Fallback: assume competency if student provided substantial response
            if len(student_response) > 50:
                return 65.0, "Student provided a detailed response"
            return 50.0, "Unable to assess competency"

    @staticmethod
    async def get_student_verifications(
        student_id: UUID,
        db: AsyncSession,
        skill_id: Optional[UUID] = None,
        status: Optional[VerificationStatus] = None
    ) -> list[Verification]:
        """
        Get all verifications for a student, optionally filtered.

        Args:
            student_id: ID of the student
            db: Database session
            skill_id: Optional filter by skill
            status: Optional filter by status
        """
        query = select(Verification).where(Verification.student_id == student_id)

        if skill_id:
            query = query.where(Verification.skill_id == skill_id)
        if status:
            query = query.where(Verification.status == status)

        query = query.order_by(Verification.created_at.desc())

        result = await db.execute(query)
        return result.scalars().all()
