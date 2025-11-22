"""
Gamification Service

Manages badges, streaks, leaderboards, and achievements
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
import uuid

from app.database.models.user import Student
from app.database.models.gamification import Badge, StudentBadge, StudentXPLog, StudentStreak


class GamificationService:
    """
    Gamification Service - Manages badges, streaks, and leaderboards
    """

    def __init__(self, db: Session):
        self.db = db

    # ========================================================================
    # Badge Management
    # ========================================================================

    async def check_and_award_badges(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Check if student qualifies for any badges and award them

        Args:
            student_id: Student UUID

        Returns:
            List of newly awarded badges
        """
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return []

        # Get all active badges
        all_badges = self.db.query(Badge).filter(Badge.is_active == True).all()

        # Get student's already earned badges
        earned_badge_ids = {
            sb.badge_id for sb in self.db.query(StudentBadge).filter(
                StudentBadge.student_id == student_id
            ).all()
        }

        newly_awarded = []

        for badge in all_badges:
            # Skip if already earned
            if badge.id in earned_badge_ids:
                continue

            # Check if student qualifies
            if await self._check_badge_qualification(student, badge):
                # Award badge
                student_badge = StudentBadge(
                    student_id=student_id,
                    badge_id=badge.id
                )
                self.db.add(student_badge)

                newly_awarded.append({
                    "badge_id": str(badge.id),
                    "name": badge.name,
                    "description": badge.description,
                    "rarity": badge.rarity,
                    "icon_url": badge.icon_url,
                    "category": badge.category,
                })

        if newly_awarded:
            self.db.commit()

        return newly_awarded

    async def _check_badge_qualification(self, student: Student, badge: Badge) -> bool:
        """
        Check if student qualifies for a specific badge

        Args:
            student: Student model
            badge: Badge model

        Returns:
            True if qualified
        """
        # XP-based badges
        if badge.xp_required and student.total_xp >= badge.xp_required:
            return True

        # Streak-based badges
        if badge.streak_required:
            streak = await self.get_student_streak(str(student.id))
            if streak and streak['current_streak'] >= badge.streak_required:
                return True

        # Category-specific checks
        if badge.category == 'first_message':
            # Check if student has sent at least 1 message
            message_count = self.db.query(StudentXPLog).filter(
                StudentXPLog.student_id == student.id,
                StudentXPLog.source == 'message'
            ).count()
            return message_count >= 1

        if badge.category == 'level_milestone':
            # Level-based badges (e.g., level 5, 10, 25)
            if badge.condition_json:
                import json
                try:
                    conditions = json.loads(badge.condition_json)
                    required_level = conditions.get('level')
                    if required_level and student.current_level >= required_level:
                        return True
                except:
                    pass

        return False

    async def get_student_badges(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get all badges earned by student

        Args:
            student_id: Student UUID

        Returns:
            List of earned badges
        """
        student_badges = self.db.query(StudentBadge).join(Badge).filter(
            StudentBadge.student_id == student_id
        ).order_by(desc(StudentBadge.earned_at)).all()

        return [
            {
                "id": str(sb.id),
                "badge_id": str(sb.badge_id),
                "name": sb.badge.name,
                "description": sb.badge.description,
                "icon_url": sb.badge.icon_url,
                "category": sb.badge.category,
                "rarity": sb.badge.rarity,
                "earned_at": sb.earned_at.isoformat(),
            }
            for sb in student_badges
        ]

    async def get_all_badges(self) -> List[Dict[str, Any]]:
        """
        Get all available badges

        Returns:
            List of all badges
        """
        badges = self.db.query(Badge).filter(Badge.is_active == True).all()

        return [
            {
                "id": str(badge.id),
                "name": badge.name,
                "description": badge.description,
                "icon_url": badge.icon_url,
                "category": badge.category,
                "rarity": badge.rarity,
                "xp_required": badge.xp_required,
                "streak_required": badge.streak_required,
            }
            for badge in badges
        ]

    # ========================================================================
    # Streak Management
    # ========================================================================

    async def update_streak(self, student_id: str) -> Dict[str, Any]:
        """
        Update student's daily activity streak

        Called when student sends a message or completes an activity

        Args:
            student_id: Student UUID

        Returns:
            Updated streak information
        """
        today = date.today()

        # Get or create streak record
        streak = self.db.query(StudentStreak).filter(
            StudentStreak.student_id == student_id
        ).first()

        if not streak:
            # Create new streak
            streak = StudentStreak(
                student_id=student_id,
                current_streak=1,
                longest_streak=1,
                last_active_date=today
            )
            self.db.add(streak)
            self.db.commit()

            return {
                "student_id": student_id,
                "current_streak": 1,
                "longest_streak": 1,
                "last_active_date": today.isoformat(),
                "streak_continued": False,
                "streak_broken": False,
            }

        # Check if activity is today
        if streak.last_active_date == today:
            # Already active today, no change
            return {
                "student_id": student_id,
                "current_streak": streak.current_streak,
                "longest_streak": streak.longest_streak,
                "last_active_date": streak.last_active_date.isoformat(),
                "streak_continued": False,
                "streak_broken": False,
            }

        # Check if activity is consecutive (yesterday)
        yesterday = today - timedelta(days=1)

        if streak.last_active_date == yesterday:
            # Streak continues!
            streak.current_streak += 1
            streak.last_active_date = today

            # Update longest streak if needed
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak

            self.db.commit()

            return {
                "student_id": student_id,
                "current_streak": streak.current_streak,
                "longest_streak": streak.longest_streak,
                "last_active_date": streak.last_active_date.isoformat(),
                "streak_continued": True,
                "streak_broken": False,
            }

        else:
            # Streak broken - reset to 1
            old_streak = streak.current_streak
            streak.current_streak = 1
            streak.last_active_date = today
            self.db.commit()

            return {
                "student_id": student_id,
                "current_streak": 1,
                "longest_streak": streak.longest_streak,
                "last_active_date": streak.last_active_date.isoformat(),
                "streak_continued": False,
                "streak_broken": True,
                "previous_streak": old_streak,
            }

    async def get_student_streak(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student's current streak

        Args:
            student_id: Student UUID

        Returns:
            Streak information or None
        """
        streak = self.db.query(StudentStreak).filter(
            StudentStreak.student_id == student_id
        ).first()

        if not streak:
            return None

        return {
            "student_id": student_id,
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "last_active_date": streak.last_active_date.isoformat(),
        }

    # ========================================================================
    # Leaderboard Management
    # ========================================================================

    async def get_leaderboard(
        self,
        school_id: Optional[str] = None,
        classroom_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get leaderboard rankings by XP

        Args:
            school_id: Optional school filter
            classroom_id: Optional classroom filter
            limit: Number of top students to return

        Returns:
            List of leaderboard entries
        """
        query = self.db.query(Student).filter(Student.is_active == True)

        # Apply filters
        if classroom_id:
            # Filter by classroom (would need to join with classroom_students table)
            # Simplified for now
            pass
        elif school_id:
            query = query.filter(Student.school_id == school_id)

        # Order by XP descending
        query = query.order_by(desc(Student.total_xp)).limit(limit)

        students = query.all()

        leaderboard = []
        for rank, student in enumerate(students, start=1):
            # Get badge count
            badge_count = self.db.query(StudentBadge).filter(
                StudentBadge.student_id == student.id
            ).count()

            # Get streak
            streak = await self.get_student_streak(str(student.id))

            leaderboard.append({
                "rank": rank,
                "student_id": str(student.id),
                "student_name": student.user.full_name if student.user else "Unknown",
                "total_xp": student.total_xp,
                "current_level": student.current_level,
                "badge_count": badge_count,
                "current_streak": streak['current_streak'] if streak else 0,
            })

        return leaderboard

    async def get_student_rank(self, student_id: str, school_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get student's rank in leaderboard

        Args:
            student_id: Student UUID
            school_id: Optional school filter

        Returns:
            Student's rank information
        """
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return {"error": "Student not found"}

        # Count students with higher XP
        query = self.db.query(func.count(Student.id)).filter(
            Student.is_active == True,
            Student.total_xp > student.total_xp
        )

        if school_id:
            query = query.filter(Student.school_id == school_id)

        rank = query.scalar() + 1  # +1 because rank starts at 1

        # Get total students
        total_query = self.db.query(func.count(Student.id)).filter(Student.is_active == True)
        if school_id:
            total_query = total_query.filter(Student.school_id == school_id)

        total_students = total_query.scalar()

        return {
            "student_id": student_id,
            "rank": rank,
            "total_students": total_students,
            "total_xp": student.total_xp,
            "current_level": student.current_level,
            "percentile": round((1 - (rank / total_students)) * 100, 1) if total_students > 0 else 0,
        }

    # ========================================================================
    # Statistics
    # ========================================================================

    async def get_student_statistics(self, student_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for student

        Args:
            student_id: Student UUID

        Returns:
            Complete gamification statistics
        """
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return {"error": "Student not found"}

        # Get badges
        badges = await self.get_student_badges(student_id)

        # Get streak
        streak = await self.get_student_streak(student_id)

        # Get rank
        rank_info = await self.get_student_rank(student_id, str(student.school_id) if student.school_id else None)

        # Get XP earned today
        today_start = datetime.combine(date.today(), datetime.min.time())
        xp_today = self.db.query(func.sum(StudentXPLog.xp_amount)).filter(
            StudentXPLog.student_id == student_id,
            StudentXPLog.timestamp >= today_start
        ).scalar() or 0

        # Get total messages sent
        total_messages = self.db.query(func.count(StudentXPLog.id)).filter(
            StudentXPLog.student_id == student_id,
            StudentXPLog.source == 'message'
        ).scalar() or 0

        return {
            "student_id": student_id,
            "total_xp": student.total_xp,
            "current_level": student.current_level,
            "xp_to_next_level": 100 - (student.total_xp % 100),
            "xp_earned_today": xp_today,
            "badges": {
                "total_earned": len(badges),
                "badges": badges[:5],  # Top 5 recent badges
            },
            "streak": streak or {
                "current_streak": 0,
                "longest_streak": 0,
            },
            "rank": rank_info,
            "total_messages": total_messages,
        }
