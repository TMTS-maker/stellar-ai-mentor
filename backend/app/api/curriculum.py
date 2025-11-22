"""
Curriculum API Endpoints

Provides REST API for curriculum management, LCT tracking, and student progress.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.session import get_db
from ..curriculum.service import CurriculumService
from ..curriculum.schemas import (
    CurriculumResponse,
    IngestCurriculumRequest,
    SubjectResponse,
    LearningObjectiveResponse,
    CompetencyRecordResponse,
    UpdateCompetencyRequest
)
from ..lct.trajectories import LCTEngine

router = APIRouter(prefix="/api/curriculum", tags=["curriculum"])


@router.get("/curricula", response_model=List[CurriculumResponse])
async def list_curricula(db: Session = Depends(get_db)):
    """Get all available curricula in the database."""
    service = CurriculumService(db)
    curricula = service.get_all_curricula()
    return curricula


@router.get("/curricula/{curriculum_code}", response_model=CurriculumResponse)
async def get_curriculum(curriculum_code: str, db: Session = Depends(get_db)):
    """Get curriculum by code."""
    service = CurriculumService(db)
    curriculum = service.get_curriculum_by_code(curriculum_code)
    if not curriculum:
        raise HTTPException(status_code=404, detail=f"Curriculum '{curriculum_code}' not found")
    return curriculum


@router.post("/ingest", response_model=CurriculumResponse)
async def ingest_curriculum(
    request: IngestCurriculumRequest,
    db: Session = Depends(get_db)
):
    """
    Ingest curriculum from a provider.

    Supported providers:
    - indian: CBSE, ICSE
    - uk: UK_NATIONAL, IGCSE, A_LEVEL
    - us: COMMON_CORE, NGSS

    This endpoint fetches curriculum data from the provider and
    imports it into the database.
    """
    service = CurriculumService(db)
    try:
        curriculum = await service.ingest_curriculum(
            request.provider_type,
            request.curriculum_code,
            request.version_code
        )
        return curriculum
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Curriculum data file not found. Please ensure curriculum JSON files are in place. {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting curriculum: {str(e)}")


@router.get("/providers")
async def list_providers(db: Session = Depends(get_db)):
    """List available curriculum providers."""
    service = CurriculumService(db)
    providers = service.list_available_providers()
    return {
        "providers": providers,
        "details": {
            "indian": "Indian curricula (CBSE, ICSE)",
            "uk": "UK curricula (National Curriculum, IGCSE, A-Level)",
            "us": "US curricula (Common Core, NGSS)"
        }
    }


@router.get("/subjects", response_model=List[SubjectResponse])
async def list_subjects(
    curriculum_code: str,
    grade: Optional[int] = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    """
    List subjects for a curriculum.

    Optionally filter by grade level.
    """
    service = CurriculumService(db)
    curriculum = service.get_curriculum_by_code(curriculum_code)
    if not curriculum:
        raise HTTPException(status_code=404, detail=f"Curriculum '{curriculum_code}' not found")

    # Get subjects (simplified - would need proper filtering)
    from ..database.models import Subject, GradeBand, CurriculumVersion
    query = (
        db.query(Subject)
        .join(GradeBand)
        .join(CurriculumVersion)
        .filter(CurriculumVersion.curriculum_id == curriculum.id)
    )

    if grade:
        query = query.filter(
            GradeBand.grade_min <= grade,
            GradeBand.grade_max >= grade
        )

    subjects = query.all()
    return subjects


@router.get("/objectives", response_model=List[LearningObjectiveResponse])
async def list_objectives(
    curriculum_id: int,
    grade: int = Query(..., ge=1, le=12),
    subject_code: str = Query(..., description="Subject code (e.g., MATH, SCIENCE)"),
    db: Session = Depends(get_db)
):
    """Get learning objectives for a specific grade and subject."""
    service = CurriculumService(db)
    objectives = service.get_objectives_for_grade_subject(
        curriculum_id, grade, subject_code
    )
    return objectives


# ============================================================================
# LCT (Learning Competency Trajectories) Endpoints
# ============================================================================


@router.get("/student/{student_id}/trajectory")
async def get_student_trajectory(
    student_id: int,
    subject_code: Optional[str] = None,
    timeframe_days: int = Query(90, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get student's learning competency trajectory (LCT).

    Returns:
    - Mastered objectives count
    - In-progress objectives count
    - Learning gaps (prerequisites not met)
    - Recommended next objectives
    - Progression rate (objectives/week)
    - Trajectory chart data
    """
    lct_engine = LCTEngine(db)
    trajectory = lct_engine.get_trajectory(student_id, subject_code, timeframe_days)
    return trajectory


@router.get("/student/{student_id}/competency", response_model=List[CompetencyRecordResponse])
async def get_student_competency_records(
    student_id: int,
    subject_code: Optional[str] = None,
    status: Optional[str] = Query(None, regex="^(not_started|in_progress|mastered|needs_review)$"),
    db: Session = Depends(get_db)
):
    """
    Get student's competency records.

    Optionally filter by subject and status.
    """
    from ..database.models import CompetencyRecord, LearningObjective, Topic, Unit, Subject
    from sqlalchemy import and_

    query = db.query(CompetencyRecord).filter(CompetencyRecord.student_id == student_id)

    if subject_code:
        query = (
            query.join(LearningObjective)
            .join(Topic)
            .join(Unit)
            .join(Subject)
            .filter(Subject.code == subject_code)
        )

    if status:
        query = query.filter(CompetencyRecord.status == status)

    records = query.order_by(CompetencyRecord.last_updated.desc()).limit(100).all()
    return records


@router.post("/student/{student_id}/competency")
async def update_student_competency(
    student_id: int,
    request: UpdateCompetencyRequest,
    db: Session = Depends(get_db)
):
    """
    Update student competency for a learning objective.

    This endpoint is called after practice, assessment, or when
    the student demonstrates mastery of an objective.
    """
    lct_engine = LCTEngine(db)

    try:
        record = lct_engine.update_competency(
            student_id=student_id,
            objective_id=request.objective_id,
            mastery_level=request.mastery_level,
            status=request.status,
            evaluation_score=request.evaluation_score
        )

        return {
            "message": "Competency updated successfully",
            "record_id": record.id,
            "status": record.status,
            "mastery_level": record.mastery_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating competency: {str(e)}")


@router.get("/student/{student_id}/recommendations")
async def get_recommendations(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get recommended next learning objectives for a student.

    Returns objectives where:
    - Prerequisites are mastered
    - Student hasn't started yet
    - Appropriate for student's grade level
    """
    lct_engine = LCTEngine(db)
    objective = lct_engine.recommend_next_objective(student_id)

    if not objective:
        return {
            "message": "No recommendations available",
            "objective": None
        }

    return {
        "message": "Recommendation generated",
        "objective": {
            "id": objective.id,
            "code": objective.code,
            "description": objective.description,
            "cognitive_level": objective.cognitive_level,
            "lvo_phase_emphasis": objective.lvo_phase_emphasis
        }
    }


@router.get("/student/{student_id}/review")
async def get_review_objectives(
    student_id: int,
    days_since_practice: int = Query(14, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """
    Get objectives needing review based on spaced repetition.

    Returns mastered objectives that haven't been practiced recently.
    Integrates with H-PEM practice strategy.
    """
    lct_engine = LCTEngine(db)
    objectives = lct_engine.suggest_review_objectives(student_id, days_since_practice)

    return {
        "count": len(objectives),
        "days_threshold": days_since_practice,
        "objectives": [
            {
                "id": obj.id,
                "code": obj.code,
                "description": obj.description,
                "cognitive_level": obj.cognitive_level
            }
            for obj in objectives
        ]
    }


@router.get("/student/{student_id}/gaps")
async def get_learning_gaps(
    student_id: int,
    subject_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Identify learning gaps (in-progress objectives with unmastered prerequisites).

    This helps identify where students might be struggling due to missing
    foundational knowledge.
    """
    lct_engine = LCTEngine(db)
    trajectory = lct_engine.get_trajectory(student_id, subject_code)

    return {
        "gaps_count": len(trajectory["learning_gaps"]),
        "gaps": trajectory["learning_gaps"]
    }


@router.get("/objective/{objective_id}/prerequisites/{student_id}")
async def check_prerequisites(
    objective_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Check if a student has mastered prerequisites for a specific objective.

    Returns:
    - prerequisites_met: bool
    - missing: List of missing prerequisite objectives
    - readiness_score: 0-100 percentage
    """
    lct_engine = LCTEngine(db)
    check_result = lct_engine.check_prerequisite_mastery(student_id, objective_id)

    return {
        "objective_id": objective_id,
        "student_id": student_id,
        "prerequisites_met": check_result["prerequisites_met"],
        "readiness_score": check_result["readiness_score"],
        "missing_prerequisites": [
            {
                "id": obj.id,
                "code": obj.code,
                "description": obj.description
            }
            for obj in check_result["missing"]
        ]
    }
