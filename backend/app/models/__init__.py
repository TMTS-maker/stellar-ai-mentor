"""Database models for Stellar AI"""
from app.models.user import User
from app.models.school import School
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.parent import Parent, ParentStudent
from app.models.classroom import Classroom, ClassSubject, Enrollment
from app.models.subject import Subject
from app.models.task import Task, StudentTaskProgress
from app.models.gamification import XPEvent, Badge, StudentBadge
from app.models.conversation import ConversationSession, ConversationMessage

# LVO models
from app.models.skill import Skill, SkillScore
from app.models.learning_path import LearningPath, LearningModule, StudentLearningPath, StudentModule
from app.models.verification import Verification
from app.models.credential import Credential, OnChainCredential

# Curriculum models
from app.models.curriculum import LearningResource

__all__ = [
    "User",
    "School",
    "Teacher",
    "Student",
    "Parent",
    "ParentStudent",
    "Classroom",
    "ClassSubject",
    "Enrollment",
    "Subject",
    "Task",
    "StudentTaskProgress",
    "XPEvent",
    "Badge",
    "StudentBadge",
    "ConversationSession",
    "ConversationMessage",
    # LVO models
    "Skill",
    "SkillScore",
    "LearningPath",
    "LearningModule",
    "StudentLearningPath",
    "StudentModule",
    "Verification",
    "Credential",
    "OnChainCredential",
    # Curriculum models
    "LearningResource",
]
