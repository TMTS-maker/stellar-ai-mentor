"""
Curriculum Context Builder

Builds curriculum context strings for injection into mentor prompts.
Integrates curriculum data, learning objectives, and LCT trajectories.
"""
from typing import Optional
from sqlalchemy.orm import Session

from .service import CurriculumService
from ..lct.trajectories import LCTEngine


def build_curriculum_context(
    db: Session,
    student_id: int,
    subject_code: Optional[str] = None
) -> str:
    """
    Build curriculum context string for a student.

    Args:
        db: Database session
        student_id: Student ID
        subject_code: Optional subject filter

    Returns:
        Formatted curriculum context string
    """
    curriculum_service = CurriculumService(db)
    lct_engine = LCTEngine(db)

    # Get student's curriculum
    curriculum = curriculum_service.get_curriculum_for_student(student_id)
    if not curriculum:
        return ""

    # Get learning trajectory
    trajectory = lct_engine.get_trajectory(student_id, subject_code, timeframe_days=90)

    # Build context string
    context_parts = [
        f"Curriculum: {curriculum.name} ({curriculum.code}, {curriculum.country_code})",
        f"Objectives mastered: {trajectory['mastered_count']}",
        f"Objectives in progress: {trajectory['in_progress_count']}"
    ]

    # Add progression rate
    if trajectory['progression_rate'] > 0:
        context_parts.append(
            f"Learning pace: {trajectory['progression_rate']} objectives/week"
        )

    # Add learning gaps if any
    if trajectory['learning_gaps']:
        gaps_count = len(trajectory['learning_gaps'])
        context_parts.append(
            f"⚠️ Learning gaps identified: {gaps_count} (prerequisites not mastered)"
        )
        # Include first gap detail
        first_gap = trajectory['learning_gaps'][0]
        context_parts.append(
            f"   - Working on: {first_gap['objective_code']} but missing prerequisites"
        )

    # Add recommended next objectives
    if trajectory['recommended_next']:
        next_objectives = trajectory['recommended_next'][:3]
        context_parts.append("\nRecommended next objectives:")
        for obj in next_objectives:
            context_parts.append(
                f"   - {obj['code']}: {obj['description'][:60]}... "
                f"[{obj['cognitive_level']}, {obj['lvo_phase_emphasis']} phase]"
            )

    # Add needs review suggestions
    review_objectives = lct_engine.suggest_review_objectives(student_id, days_since_practice=14)
    if review_objectives:
        context_parts.append(f"\n📚 Objectives needing review (not practiced in 14+ days): {len(review_objectives)}")
        for obj in review_objectives[:2]:
            context_parts.append(f"   - {obj.code}: {obj.description[:50]}...")

    return "\n".join(context_parts)


def build_objective_context(
    db: Session,
    student_id: int,
    objective_id: int
) -> str:
    """
    Build context string for a specific learning objective.

    Args:
        db: Database session
        student_id: Student ID
        objective_id: Learning objective ID

    Returns:
        Formatted objective context string
    """
    lct_engine = LCTEngine(db)

    # Check prerequisite mastery
    prereq_check = lct_engine.check_prerequisite_mastery(student_id, objective_id)

    context_parts = []

    if not prereq_check["prerequisites_met"]:
        context_parts.append(
            f"⚠️ Prerequisites not fully met (Readiness: {prereq_check['readiness_score']}%)"
        )
        missing_count = len(prereq_check["missing"])
        context_parts.append(f"Missing {missing_count} prerequisite(s):")
        for prereq in prereq_check["missing"][:3]:
            context_parts.append(f"   - {prereq.code}: {prereq.description[:50]}...")
    else:
        context_parts.append("✅ All prerequisites mastered - student is ready!")

    return "\n".join(context_parts)
