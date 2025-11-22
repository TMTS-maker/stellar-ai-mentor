"""
Database Models Package

Import all models here for Alembic migrations
"""
from app.database.models.user import User, Student, Teacher, Parent
from app.database.models.school import School, Classroom
from app.database.models.conversation import ConversationSession, Message
from app.database.models.curriculum import (
    Curriculum,
    CurriculumObjective,
    Skill,
    StudentSkillProgress
)
from app.database.models.gamification import (
    Badge,
    StudentBadge,
    StudentXPLog,
    StudentStreak
)
from app.database.models.blockchain import HPEMCredential

__all__ = [
    # User models
    "User",
    "Student",
    "Teacher",
    "Parent",
    # School models
    "School",
    "Classroom",
    # Conversation models
    "ConversationSession",
    "Message",
    # Curriculum models
    "Curriculum",
    "CurriculumObjective",
    "Skill",
    "StudentSkillProgress",
    # Gamification models
    "Badge",
    "StudentBadge",
    "StudentXPLog",
    "StudentStreak",
    # Blockchain models
    "HPEMCredential",
]
