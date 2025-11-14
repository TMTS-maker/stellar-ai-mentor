"""
LearningPathService for managing learning paths and AI-powered task recommendations.

This service implements the core "LEARN" phase of the LVO architecture.
"""

from uuid import UUID
from typing import Optional
from datetime import datetime
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.student import Student
from app.models.skill import Skill, SkillScore
from app.models.learning_path import (
    LearningPath, LearningModule, StudentLearningPath, StudentModule,
    PathStatus, ModuleStatus
)
from app.models.task import Task, StudentTaskProgress, TaskStatus
from app.schemas.learning_path import NextTaskRecommendation
from app.services.ai.llm_service import LLMService


class LearningPathService:
    """Service for managing learning paths and AI task recommendations."""

    @staticmethod
    async def get_next_best_task_for_student(
        student_id: UUID,
        db: AsyncSession,
        use_ai: bool = True
    ) -> Optional[NextTaskRecommendation]:
        """
        Get AI-powered recommendation for the next best task for a student.

        Strategy:
        1. Analyze student's current skill profile
        2. Identify knowledge gaps and weak skills
        3. Check current learning paths and modules
        4. Find tasks that:
           - Address weak skills
           - Match student's age/level
           - Build on completed work
           - Follow learning path progression
        5. Use AI to provide reasoning and confidence score

        Args:
            student_id: ID of the student
            db: Database session
            use_ai: Whether to use AI for reasoning (falls back to rule-based if False)

        Returns:
            NextTaskRecommendation or None if no suitable task found
        """
        # Get student with all related data
        student_result = await db.execute(
            select(Student)
            .options(selectinload(Student.skill_scores))
            .where(Student.id == student_id)
        )
        student = student_result.scalar_one_or_none()
        if not student:
            return None

        # Get student's skill scores
        skill_scores_result = await db.execute(
            select(SkillScore, Skill)
            .join(Skill, SkillScore.skill_id == Skill.id)
            .where(SkillScore.student_id == student_id)
            .order_by(SkillScore.score.asc())
        )
        skill_scores = skill_scores_result.all()

        # Get completed task IDs
        completed_tasks_result = await db.execute(
            select(StudentTaskProgress.task_id)
            .where(
                and_(
                    StudentTaskProgress.student_id == student_id,
                    StudentTaskProgress.status == TaskStatus.COMPLETED
                )
            )
        )
        completed_task_ids = [row[0] for row in completed_tasks_result.all()]

        # Get current learning paths
        student_paths_result = await db.execute(
            select(StudentLearningPath, LearningPath)
            .join(LearningPath, StudentLearningPath.learning_path_id == LearningPath.id)
            .where(
                and_(
                    StudentLearningPath.student_id == student_id,
                    StudentLearningPath.status == PathStatus.IN_PROGRESS
                )
            )
        )
        student_paths = student_paths_result.all()

        # Strategy 1: Continue current learning path
        if student_paths:
            for student_path, learning_path in student_paths:
                # Get next module in this path
                modules_result = await db.execute(
                    select(LearningModule)
                    .where(LearningModule.learning_path_id == learning_path.id)
                    .order_by(LearningModule.order.asc())
                )
                modules = modules_result.scalars().all()

                for module in modules:
                    # Check if module is unlocked or in progress
                    student_module_result = await db.execute(
                        select(StudentModule)
                        .where(
                            and_(
                                StudentModule.student_id == student_id,
                                StudentModule.module_id == module.id
                            )
                        )
                    )
                    student_module = student_module_result.scalar_one_or_none()

                    if student_module and student_module.status == ModuleStatus.COMPLETED:
                        continue  # Skip completed modules

                    # Get tasks from this module
                    if module.task_ids:
                        for task_id_str in module.task_ids:
                            task_id = UUID(task_id_str)
                            if task_id in completed_task_ids:
                                continue  # Skip completed tasks

                            # Get task details
                            task_result = await db.execute(
                                select(Task)
                                .options(selectinload(Task.skills))
                                .where(Task.id == task_id)
                            )
                            task = task_result.scalar_one_or_none()
                            if not task:
                                continue

                            # Build recommendation
                            return await LearningPathService._build_recommendation(
                                task=task,
                                module=module,
                                learning_path=learning_path,
                                student=student,
                                skill_scores=skill_scores,
                                use_ai=use_ai,
                                db=db
                            )

        # Strategy 2: Find tasks that address weak skills
        if skill_scores:
            # Get skills with lowest scores (need improvement)
            weak_skills = [skill for score, skill in skill_scores if score.score < 60][:3]

            if weak_skills:
                weak_skill_ids = [skill.id for skill in weak_skills]

                # Find tasks that teach these skills
                tasks_result = await db.execute(
                    select(Task)
                    .join(Task.skills)
                    .options(selectinload(Task.skills))
                    .where(
                        and_(
                            Skill.id.in_(weak_skill_ids),
                            Task.id.notin_(completed_task_ids) if completed_task_ids else True
                        )
                    )
                    .limit(1)
                )
                task = tasks_result.scalar_one_or_none()

                if task:
                    return await LearningPathService._build_recommendation(
                        task=task,
                        module=None,
                        learning_path=None,
                        student=student,
                        skill_scores=skill_scores,
                        use_ai=use_ai,
                        db=db,
                        reason_context="This task focuses on skills where you need practice"
                    )

        # Strategy 3: Get any uncompleted task
        tasks_result = await db.execute(
            select(Task)
            .options(selectinload(Task.skills))
            .where(Task.id.notin_(completed_task_ids) if completed_task_ids else True)
            .limit(1)
        )
        task = tasks_result.scalar_one_or_none()

        if task:
            return await LearningPathService._build_recommendation(
                task=task,
                module=None,
                learning_path=None,
                student=student,
                skill_scores=skill_scores,
                use_ai=use_ai,
                db=db,
                reason_context="This is a new challenge for you to explore"
            )

        return None

    @staticmethod
    async def _build_recommendation(
        task: Task,
        module: Optional[LearningModule],
        learning_path: Optional[LearningPath],
        student: Student,
        skill_scores: list,
        use_ai: bool,
        db: AsyncSession,
        reason_context: Optional[str] = None
    ) -> NextTaskRecommendation:
        """Build a NextTaskRecommendation with AI reasoning."""

        # Get skill names
        skill_names = [skill.name for skill in task.skills] if task.skills else []

        # Generate AI reason if enabled
        if use_ai:
            reason, confidence = await LearningPathService._generate_ai_reason(
                task=task,
                student=student,
                skill_scores=skill_scores,
                skill_names=skill_names,
                context=reason_context
            )
        else:
            # Fallback to rule-based reason
            if reason_context:
                reason = reason_context
            elif module:
                reason = f"Next step in your {learning_path.name if learning_path else 'learning journey'}"
            else:
                reason = "This task will help you develop new skills"
            confidence = 0.7

        return NextTaskRecommendation(
            task_id=task.id,
            task_title=task.title,
            task_description=task.description,
            module_id=module.id if module else None,
            module_name=module.name if module else None,
            learning_path_id=learning_path.id if learning_path else None,
            learning_path_name=learning_path.name if learning_path else None,
            skill_ids=[str(skill.id) for skill in task.skills] if task.skills else [],
            xp_reward=task.xp_reward,
            estimated_minutes=module.estimated_minutes if module else None,
            reason=reason,
            confidence=confidence
        )

    @staticmethod
    async def _generate_ai_reason(
        task: Task,
        student: Student,
        skill_scores: list,
        skill_names: list[str],
        context: Optional[str]
    ) -> tuple[str, float]:
        """
        Use AI to generate a personalized reason for recommending this task.

        Returns:
            Tuple of (reason_text, confidence_score)
        """
        try:
            # Build context for AI
            weak_skills_text = ""
            if skill_scores:
                weak_skills = [f"{skill.name} (score: {score.score:.0f})"
                              for score, skill in skill_scores[:3] if score.score < 60]
                if weak_skills:
                    weak_skills_text = f"Skills needing practice: {', '.join(weak_skills)}"

            skill_text = f"This task focuses on: {', '.join(skill_names)}" if skill_names else "This is a general learning task"

            prompt = f"""You are an educational AI recommending tasks to students.

Student context:
{weak_skills_text}

Task to recommend:
- Title: {task.title}
- {skill_text}
- XP Reward: {task.xp_reward}

Context: {context or 'General recommendation'}

Generate a single, encouraging sentence (max 20 words) explaining why this task is a good next step for the student. Be warm, positive, and specific."""

            messages = [{"role": "user", "content": prompt}]
            reason = await LLMService.generate_response(messages, max_tokens=100)

            # Clean up response
            reason = reason.strip().strip('"').strip("'")
            if not reason:
                reason = context or "This task matches your current learning level"

            # Confidence based on context
            confidence = 0.85 if weak_skills_text else 0.75

            return reason, confidence

        except Exception as e:
            # Fallback to context or generic message
            return context or "This task will help you grow your skills", 0.7

    @staticmethod
    async def update_module_progress(
        student_id: UUID,
        module_id: UUID,
        db: AsyncSession
    ) -> Optional[StudentModule]:
        """
        Update student's progress in a module after completing a task.

        Automatically:
        - Updates task completion count
        - Calculates module score
        - Marks module as completed if threshold met
        - Unlocks next module in path
        """
        # Get or create student module record
        student_module_result = await db.execute(
            select(StudentModule)
            .where(
                and_(
                    StudentModule.student_id == student_id,
                    StudentModule.module_id == module_id
                )
            )
        )
        student_module = student_module_result.scalar_one_or_none()

        # Get module details
        module_result = await db.execute(
            select(LearningModule).where(LearningModule.id == module_id)
        )
        module = module_result.scalar_one_or_none()
        if not module:
            return None

        # Count completed tasks in this module
        if module.task_ids:
            completed_count = 0
            total_score = 0.0

            for task_id_str in module.task_ids:
                task_id = UUID(task_id_str)
                progress_result = await db.execute(
                    select(StudentTaskProgress)
                    .where(
                        and_(
                            StudentTaskProgress.student_id == student_id,
                            StudentTaskProgress.task_id == task_id
                        )
                    )
                )
                progress = progress_result.scalar_one_or_none()

                if progress and progress.status == TaskStatus.COMPLETED:
                    completed_count += 1
                    if progress.score:
                        total_score += progress.score

            # Calculate average score
            avg_score = total_score / completed_count if completed_count > 0 else 0

            # Update or create student module
            if not student_module:
                student_module = StudentModule(
                    student_id=student_id,
                    module_id=module_id,
                    status=ModuleStatus.IN_PROGRESS,
                    tasks_total=len(module.task_ids),
                    tasks_completed=completed_count,
                    score=avg_score,
                    started_at=datetime.utcnow()
                )
                db.add(student_module)
            else:
                student_module.tasks_completed = completed_count
                student_module.score = avg_score
                student_module.updated_at = datetime.utcnow()

                # Check completion
                if completed_count >= len(module.task_ids) and avg_score >= module.completion_threshold:
                    student_module.status = ModuleStatus.COMPLETED
                    student_module.completed_at = datetime.utcnow()

            await db.commit()
            await db.refresh(student_module)

        return student_module
