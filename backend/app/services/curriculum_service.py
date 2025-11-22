"""
Curriculum Service

Manages curriculum data, student progress, and integration with AI mentors
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import uuid

from app.database.models.curriculum import (
    Curriculum,
    CurriculumObjective,
    Skill,
    StudentSkillProgress,
)
from app.database.models.user import Student
from app.curriculum.providers import get_curriculum_provider, list_available_curricula
from app.curriculum.base_provider import CurriculumObjectiveData


class CurriculumService:
    """
    Curriculum Service - Manages curriculum and student progress
    """

    def __init__(self, db: Session):
        self.db = db

    async def get_student_curriculum_context(self, student_id: str, subject: str) -> Dict[str, Any]:
        """
        Build curriculum context for student

        Used by AI mentors to align responses with curriculum

        Args:
            student_id: Student UUID
            subject: Subject code

        Returns:
            Curriculum context dictionary
        """
        # 1. Get student
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student or not student.curriculum_id:
            return self._get_default_context(subject)

        # 2. Get curriculum
        curriculum = (
            self.db.query(Curriculum).filter(Curriculum.id == student.curriculum_id).first()
        )

        if not curriculum:
            return self._get_default_context(subject)

        # 3. Get curriculum provider
        try:
            provider = get_curriculum_provider(curriculum.curriculum_type)
        except KeyError:
            return self._get_default_context(subject)

        # 4. Get current objectives for student's grade and subject
        current_objectives = provider.get_objectives_for_grade_subject(
            grade_level=student.grade_level, subject=subject
        )

        # 5. Get student's skill progress
        skill_progress = await self._get_student_progress(student_id, subject)

        # 6. Recommend next objectives based on progress
        recommended_objectives = self._recommend_next_objectives(
            provider, current_objectives, skill_progress
        )

        return {
            "curriculum_id": str(curriculum.id),
            "curriculum_name": curriculum.curriculum_name,
            "curriculum_type": curriculum.curriculum_type,
            "current_objectives": [
                {
                    "id": obj.objective_code,
                    "objective_code": obj.objective_code,
                    "objective_text": obj.objective_text,
                    "topic": obj.topic,
                    "subtopic": obj.subtopic,
                    "difficulty_level": obj.difficulty_level,
                }
                for obj in recommended_objectives[:3]  # Top 3 recommendations
            ],
        }

    def _get_default_context(self, subject: str) -> Dict[str, Any]:
        """Get default context when student has no curriculum assigned"""
        return {
            "curriculum_id": None,
            "curriculum_name": "General Curriculum",
            "curriculum_type": None,
            "current_objectives": [],
        }

    async def _get_student_progress(
        self, student_id: str, subject: str
    ) -> Dict[str, Dict[str, float]]:
        """
        Get student's progress on skills

        Returns:
            Dict mapping objective_id to progress dict
        """
        progress_records = (
            self.db.query(StudentSkillProgress)
            .join(Skill)
            .join(CurriculumObjective)
            .filter(
                StudentSkillProgress.student_id == student_id,
                CurriculumObjective.subject == subject,
            )
            .all()
        )

        progress_map = {}
        for record in progress_records:
            skill = record.skill
            objective = skill.objective

            if objective.id not in progress_map:
                progress_map[str(objective.id)] = {"learn": 0, "verify": 0, "own": 0, "mastery": 0}

            # Aggregate progress across skills for the objective
            current = progress_map[str(objective.id)]
            current["learn"] = max(current["learn"], record.learn_progress)
            current["verify"] = max(current["verify"], record.verify_progress)
            current["own"] = max(current["own"], record.own_progress)
            current["mastery"] = max(current["mastery"], record.mastery_score)

        return progress_map

    def _recommend_next_objectives(
        self,
        provider,
        all_objectives: List[CurriculumObjectiveData],
        progress: Dict[str, Dict[str, float]],
    ) -> List[CurriculumObjectiveData]:
        """
        Recommend next objectives based on student progress

        Returns objectives in order of recommendation
        """
        if not all_objectives:
            return []

        # Score each objective
        scored_objectives = []

        for obj in all_objectives:
            score = 0

            # Check if already mastered
            obj_progress = progress.get(obj.objective_code, {})
            mastery = obj_progress.get("mastery", 0)

            if mastery >= 80:
                # Already mastered, lower priority
                score -= 100
            elif mastery >= 50:
                # Partially learned, medium priority
                score += 50
            else:
                # Not started or low progress, check prerequisites
                prereqs_met = True
                for prereq_code in obj.prerequisite_codes:
                    prereq_progress = progress.get(prereq_code, {})
                    if prereq_progress.get("mastery", 0) < 70:
                        prereqs_met = False
                        break

                if prereqs_met:
                    # Prerequisites met, high priority
                    score += 100
                else:
                    # Prerequisites not met, low priority
                    score += 10

            # Prefer lower difficulty for beginners
            score -= (obj.difficulty_level - 5) * 5

            scored_objectives.append((score, obj))

        # Sort by score (descending)
        scored_objectives.sort(key=lambda x: x[0], reverse=True)

        return [obj for score, obj in scored_objectives]

    async def initialize_curriculum_data(self, curriculum_type: str) -> str:
        """
        Initialize curriculum in database from provider

        Args:
            curriculum_type: Type of curriculum to initialize

        Returns:
            Curriculum ID
        """
        # Check if curriculum already exists
        existing = (
            self.db.query(Curriculum).filter(Curriculum.curriculum_type == curriculum_type).first()
        )

        if existing:
            return str(existing.id)

        # Get provider
        provider = get_curriculum_provider(curriculum_type)

        # Create curriculum record
        curriculum = Curriculum(
            curriculum_type=provider.curriculum_type,
            curriculum_name=provider.curriculum_name,
            country=provider.country,
            board=provider.board,
            description=f"Curriculum for {provider.curriculum_name}",
        )
        self.db.add(curriculum)
        self.db.flush()

        # Add objectives from provider
        # In a real implementation, this would load all objectives
        # For now, we'll just acknowledge the curriculum exists
        self.db.commit()

        return str(curriculum.id)

    async def search_objectives(
        self,
        curriculum_type: str,
        query: str,
        subject: Optional[str] = None,
        grade_level: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search curriculum objectives

        Args:
            curriculum_type: Curriculum type
            query: Search query
            subject: Optional subject filter
            grade_level: Optional grade filter

        Returns:
            List of matching objectives
        """
        provider = get_curriculum_provider(curriculum_type)
        results = provider.search_objectives(query, subject, grade_level)

        return [
            {
                "objective_code": obj.objective_code,
                "objective_text": obj.objective_text,
                "subject": obj.subject,
                "grade_level": obj.grade_level,
                "topic": obj.topic,
                "subtopic": obj.subtopic,
                "difficulty_level": obj.difficulty_level,
            }
            for obj in results
        ]

    async def get_objective_details(
        self, curriculum_type: str, objective_code: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific objective

        Args:
            curriculum_type: Curriculum type
            objective_code: Objective code

        Returns:
            Objective details or None
        """
        provider = get_curriculum_provider(curriculum_type)
        obj = provider.get_objective_by_code(objective_code)

        if not obj:
            return None

        return {
            "objective_code": obj.objective_code,
            "objective_text": obj.objective_text,
            "subject": obj.subject,
            "grade_level": obj.grade_level,
            "topic": obj.topic,
            "subtopic": obj.subtopic,
            "difficulty_level": obj.difficulty_level,
            "blooms_level": obj.blooms_level,
            "description": obj.description,
            "example_questions": obj.example_questions,
            "prerequisites": obj.prerequisite_codes,
            "next_objectives": provider.get_next_objectives(objective_code),
        }

    def list_curricula(self) -> List[str]:
        """
        List all available curriculum types

        Returns:
            List of curriculum type identifiers
        """
        return list_available_curricula()
