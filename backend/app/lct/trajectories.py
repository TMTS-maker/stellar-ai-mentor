"""
LCT - Learning Competency Trajectories

Tracks student progression through curriculum learning objectives.
Integrates with:
- Curriculum learning objectives
- LVO phases
- H-PEM strategies
- Competency records
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..database.models import (
    CompetencyRecord, LearningObjective, Student,
    Topic, Unit, Subject
)


class LCTEngine:
    """
    LCT engine for tracking and predicting learning trajectories.

    Responsibilities:
    - Track competency progression
    - Identify learning gaps
    - Recommend next objectives
    - Predict mastery timelines
    - Integrate with H-PEM for spaced practice
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_trajectory(
        self,
        student_id: int,
        subject_code: Optional[str] = None,
        timeframe_days: int = 90
    ) -> Dict[str, Any]:
        """
        Get student's learning trajectory over a timeframe.

        Args:
            student_id: Student ID
            subject_code: Optional subject filter
            timeframe_days: Timeframe in days (default 90)

        Returns:
            Trajectory data with:
            - Current competency levels
            - Progression rate
            - Predicted mastery dates
            - Recommended focus areas
        """
        cutoff_date = datetime.utcnow() - timedelta(days=timeframe_days)

        # Fetch competency records
        records = self._fetch_records(student_id, subject_code, cutoff_date)

        # Analyze progression
        progression_rate = self._calculate_progression_rate(records)
        mastery_count = len([r for r in records if r.status == "mastered"])
        in_progress_count = len([r for r in records if r.status == "in_progress"])
        needs_review_count = len([r for r in records if r.status == "needs_review"])

        # Identify gaps (prerequisites not mastered)
        gaps = self._identify_gaps(student_id, records)

        # Recommend next objectives
        recommendations = self._recommend_next_objectives(student_id, records)

        # Build trajectory chart data
        trajectory_chart = self._build_trajectory_chart(records, timeframe_days)

        return {
            "student_id": student_id,
            "timeframe_days": timeframe_days,
            "mastered_count": mastery_count,
            "in_progress_count": in_progress_count,
            "needs_review_count": needs_review_count,
            "progression_rate": progression_rate,
            "learning_gaps": gaps,
            "recommended_next": recommendations,
            "trajectory_chart": trajectory_chart
        }

    def _fetch_records(
        self,
        student_id: int,
        subject_code: Optional[str],
        cutoff_date: datetime
    ) -> List[CompetencyRecord]:
        """Fetch competency records for a student."""
        query = self.db.query(CompetencyRecord).filter(
            and_(
                CompetencyRecord.student_id == student_id,
                CompetencyRecord.last_updated >= cutoff_date
            )
        )

        if subject_code:
            # Join to filter by subject
            query = (
                query.join(LearningObjective)
                .join(Topic)
                .join(Unit)
                .join(Subject)
                .filter(Subject.code == subject_code)
            )

        return query.order_by(CompetencyRecord.last_updated.desc()).all()

    def _calculate_progression_rate(self, records: List[CompetencyRecord]) -> float:
        """
        Calculate progression rate (objectives mastered per week).

        Args:
            records: List of competency records

        Returns:
            Progression rate (objectives/week)
        """
        if not records:
            return 0.0

        mastered_records = [r for r in records if r.status == "mastered" and r.mastered_at]

        if not mastered_records:
            return 0.0

        # Calculate time span
        earliest = min(r.mastered_at for r in mastered_records)
        latest = max(r.mastered_at for r in mastered_records)
        days_span = (latest - earliest).days or 1

        # Calculate rate
        mastered_count = len(mastered_records)
        weeks_span = days_span / 7.0
        rate = mastered_count / weeks_span if weeks_span > 0 else mastered_count

        return round(rate, 2)

    def _identify_gaps(
        self,
        student_id: int,
        records: List[CompetencyRecord]
    ) -> List[Dict[str, Any]]:
        """
        Identify learning gaps (in-progress objectives with unmastered prerequisites).

        Args:
            student_id: Student ID
            records: Competency records

        Returns:
            List of gap dictionaries
        """
        gaps = []

        # Get mastered objective IDs
        mastered_ids = {r.objective_id for r in records if r.status == "mastered"}

        # Check in-progress objectives
        in_progress_records = [r for r in records if r.status == "in_progress"]

        for record in in_progress_records:
            objective = self.db.query(LearningObjective).filter(
                LearningObjective.id == record.objective_id
            ).first()

            if not objective:
                continue

            # Check prerequisites
            topic = objective.topic
            if topic and topic.prerequisite_topic_ids:
                # Get objectives from prerequisite topics
                prereq_objectives = self.db.query(LearningObjective).filter(
                    LearningObjective.topic_id.in_(topic.prerequisite_topic_ids)
                ).all()

                unmastered_prereqs = [
                    obj for obj in prereq_objectives
                    if obj.id not in mastered_ids
                ]

                if unmastered_prereqs:
                    gaps.append({
                        "objective_id": objective.id,
                        "objective_code": objective.code,
                        "objective_name": objective.description[:50] + "...",
                        "missing_prerequisites": [
                            {
                                "id": prereq.id,
                                "code": prereq.code,
                                "description": prereq.description[:50] + "..."
                            }
                            for prereq in unmastered_prereqs
                        ]
                    })

        return gaps[:5]  # Return top 5 gaps

    def _recommend_next_objectives(
        self,
        student_id: int,
        records: List[CompetencyRecord]
    ) -> List[Dict[str, Any]]:
        """
        Recommend next learning objectives based on progression.

        Args:
            student_id: Student ID
            records: Competency records

        Returns:
            List of recommended objective dictionaries
        """
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return []

        # Get mastered objective IDs
        mastered_ids = {r.objective_id for r in records if r.status == "mastered"}

        # Get in-progress objective IDs
        in_progress_ids = {r.objective_id for r in records if r.status == "in_progress"}

        # Find objectives where:
        # 1. Student hasn't started yet
        # 2. Prerequisites are met
        # 3. Appropriate for student's grade

        # Get all objectives for student's subjects
        if not student.current_subjects:
            return []

        candidate_objectives = (
            self.db.query(LearningObjective)
            .join(Topic)
            .join(Unit)
            .join(Subject)
            .filter(Subject.id.in_(student.current_subjects))
            .all()
        )

        recommendations = []
        for obj in candidate_objectives:
            # Skip if already mastered or in progress
            if obj.id in mastered_ids or obj.id in in_progress_ids:
                continue

            # Check prerequisites
            if obj.topic and obj.topic.prerequisite_topic_ids:
                prereq_objectives = self.db.query(LearningObjective).filter(
                    LearningObjective.topic_id.in_(obj.topic.prerequisite_topic_ids)
                ).all()

                # Check if all prerequisites are mastered
                prereqs_met = all(prereq.id in mastered_ids for prereq in prereq_objectives)
                if not prereqs_met:
                    continue

            # Add to recommendations
            recommendations.append({
                "id": obj.id,
                "code": obj.code,
                "description": obj.description,
                "cognitive_level": obj.cognitive_level,
                "lvo_phase_emphasis": obj.lvo_phase_emphasis,
                "difficulty": obj.topic.difficulty_level if obj.topic else "intermediate"
            })

            # Limit to top 5 recommendations
            if len(recommendations) >= 5:
                break

        return recommendations

    def _build_trajectory_chart(
        self,
        records: List[CompetencyRecord],
        timeframe_days: int
    ) -> Dict[str, Any]:
        """
        Build trajectory chart data for visualization.

        Args:
            records: Competency records
            timeframe_days: Timeframe in days

        Returns:
            Chart data dictionary
        """
        # Group records by week
        cutoff = datetime.utcnow() - timedelta(days=timeframe_days)
        weeks = []
        current_date = cutoff

        while current_date <= datetime.utcnow():
            week_end = current_date + timedelta(days=7)

            # Count objectives mastered this week
            week_mastered = len([
                r for r in records
                if r.status == "mastered"
                and r.mastered_at
                and current_date <= r.mastered_at < week_end
            ])

            weeks.append({
                "week_start": current_date.strftime("%Y-%m-%d"),
                "objectives_mastered": week_mastered
            })

            current_date = week_end

        return {
            "weeks": weeks,
            "total_mastered": len([r for r in records if r.status == "mastered"]),
            "average_per_week": sum(w["objectives_mastered"] for w in weeks) / len(weeks) if weeks else 0
        }

    def recommend_next_objective(
        self,
        student_id: int,
        current_objective_id: Optional[int] = None
    ) -> Optional[LearningObjective]:
        """
        Recommend next single learning objective.

        Args:
            student_id: Student ID
            current_objective_id: Optional current objective

        Returns:
            Recommended LearningObjective or None
        """
        records = self._fetch_records(student_id, None, datetime.utcnow() - timedelta(days=365))
        recommendations = self._recommend_next_objectives(student_id, records)

        if recommendations:
            # Return the first recommendation as a LearningObjective
            rec = recommendations[0]
            return self.db.query(LearningObjective).filter(
                LearningObjective.id == rec["id"]
            ).first()

        return None

    def check_prerequisite_mastery(
        self,
        student_id: int,
        objective_id: int
    ) -> Dict[str, Any]:
        """
        Check if student has mastered prerequisites for an objective.

        Args:
            student_id: Student ID
            objective_id: Learning objective ID

        Returns:
            Prerequisite check result with:
            - prerequisites_met: bool
            - missing: List[LearningObjective]
            - readiness_score: 0-100
        """
        objective = self.db.query(LearningObjective).filter(
            LearningObjective.id == objective_id
        ).first()

        if not objective or not objective.topic or not objective.topic.prerequisite_topic_ids:
            return {
                "prerequisites_met": True,
                "missing": [],
                "readiness_score": 100
            }

        # Get mastered objectives for student
        mastered_records = self.db.query(CompetencyRecord).filter(
            and_(
                CompetencyRecord.student_id == student_id,
                CompetencyRecord.status == "mastered"
            )
        ).all()

        mastered_ids = {r.objective_id for r in mastered_records}

        # Get prerequisite objectives
        prereq_objectives = self.db.query(LearningObjective).filter(
            LearningObjective.topic_id.in_(objective.topic.prerequisite_topic_ids)
        ).all()

        missing_prereqs = [
            obj for obj in prereq_objectives
            if obj.id not in mastered_ids
        ]

        # Calculate readiness score
        total_prereqs = len(prereq_objectives)
        mastered_prereqs = total_prereqs - len(missing_prereqs)
        readiness_score = int((mastered_prereqs / total_prereqs * 100)) if total_prereqs > 0 else 100

        return {
            "prerequisites_met": len(missing_prereqs) == 0,
            "missing": missing_prereqs,
            "readiness_score": readiness_score
        }

    def suggest_review_objectives(
        self,
        student_id: int,
        days_since_practice: int = 14
    ) -> List[LearningObjective]:
        """
        Suggest objectives for review based on spaced repetition.

        Integrates with H-PEM practice strategy.

        Args:
            student_id: Student ID
            days_since_practice: Days since last practice (default 14)

        Returns:
            List of objectives needing review
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_since_practice)

        # Find mastered objectives not practiced recently
        records = self.db.query(CompetencyRecord).filter(
            and_(
                CompetencyRecord.student_id == student_id,
                CompetencyRecord.status == "mastered"
            )
        ).all()

        # Filter by last practice date
        review_records = [
            r for r in records
            if not r.last_practiced_at or r.last_practiced_at < cutoff_date
        ]

        # Sort by oldest practice date first
        review_records.sort(
            key=lambda r: r.last_practiced_at or datetime.min
        )

        # Return objectives for top 5 records
        return [
            record.objective for record in review_records[:5]
            if record.objective
        ]

    def update_competency(
        self,
        student_id: int,
        objective_id: int,
        mastery_level: int,
        status: str,
        evaluation_score: Optional[int] = None
    ) -> CompetencyRecord:
        """
        Update student's competency record for an objective.

        Args:
            student_id: Student ID
            objective_id: Learning objective ID
            mastery_level: Mastery level 0-100
            status: Status (not_started, in_progress, mastered, needs_review)
            evaluation_score: Optional assessment score

        Returns:
            Updated CompetencyRecord
        """
        record = self.db.query(CompetencyRecord).filter(
            and_(
                CompetencyRecord.student_id == student_id,
                CompetencyRecord.objective_id == objective_id
            )
        ).first()

        if not record:
            # Create new record
            record = CompetencyRecord(
                student_id=student_id,
                objective_id=objective_id,
                status=status,
                mastery_level=mastery_level,
                started_at=datetime.utcnow(),
                practice_count=1,
                last_practiced_at=datetime.utcnow()
            )
            self.db.add(record)
        else:
            # Update existing record
            record.mastery_level = mastery_level
            record.status = status
            record.practice_count += 1
            record.last_practiced_at = datetime.utcnow()

            if status == "mastered" and not record.mastered_at:
                record.mastered_at = datetime.utcnow()

        if evaluation_score is not None:
            record.evaluation_score = evaluation_score

        self.db.commit()
        self.db.refresh(record)

        return record
