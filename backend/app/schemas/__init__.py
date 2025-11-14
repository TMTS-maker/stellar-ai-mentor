"""Pydantic schemas for request/response validation"""
from app.schemas.user import (
    UserCreate, UserResponse, UserLogin, Token, TokenPayload
)
from app.schemas.school import SchoolCreate, SchoolResponse
from app.schemas.teacher import TeacherCreate, TeacherResponse
from app.schemas.student import (
    StudentCreate, StudentResponse, StudentDashboard, StudentBulkCreate
)
from app.schemas.parent import ParentCreate, ParentResponse, ChildLinkRequest
from app.schemas.classroom import ClassroomCreate, ClassroomResponse
from app.schemas.subject import SubjectCreate, SubjectResponse
from app.schemas.task import TaskCreate, TaskResponse, TaskProgressResponse
from app.schemas.gamification import XPResponse, BadgeResponse, StudentBadgeResponse
from app.schemas.conversation import (
    ConversationSessionCreate, ConversationSessionResponse,
    ConversationMessageCreate, ConversationMessageResponse,
    TextConversationRequest, VoiceConversationRequest
)

# LVO schemas
from app.schemas.skill import (
    SkillCreate, SkillUpdate, SkillResponse,
    SkillScoreCreate, SkillScoreUpdate, SkillScoreResponse, SkillScoreWithSkill,
    StudentSkillsProfile
)
from app.schemas.learning_path import (
    LearningPathCreate, LearningPathUpdate, LearningPathResponse, LearningPathWithModules,
    LearningModuleCreate, LearningModuleUpdate, LearningModuleResponse,
    StudentLearningPathResponse, StudentLearningPathWithDetails,
    StudentModuleResponse, StudentModuleWithDetails,
    NextTaskRecommendation
)
from app.schemas.verification import (
    VerificationCreate, VerificationUpdate, VerificationResponse, VerificationWithDetails,
    VerificationRequest, SkillVerificationSummary, StudentVerificationProfile
)
from app.schemas.credential import (
    CredentialCreate, CredentialUpdate, CredentialResponse, CredentialWithBlockchain, CredentialWithDetails,
    MintCredentialRequest, MintCredentialResponse,
    StudentCredentialsPortfolio, ShareableCredential,
    OnChainCredentialResponse
)

__all__ = [
    "UserCreate", "UserResponse", "UserLogin", "Token", "TokenPayload",
    "SchoolCreate", "SchoolResponse",
    "TeacherCreate", "TeacherResponse",
    "StudentCreate", "StudentResponse", "StudentDashboard", "StudentBulkCreate",
    "ParentCreate", "ParentResponse", "ChildLinkRequest",
    "ClassroomCreate", "ClassroomResponse",
    "SubjectCreate", "SubjectResponse",
    "TaskCreate", "TaskResponse", "TaskProgressResponse",
    "XPResponse", "BadgeResponse", "StudentBadgeResponse",
    "ConversationSessionCreate", "ConversationSessionResponse",
    "ConversationMessageCreate", "ConversationMessageResponse",
    "TextConversationRequest", "VoiceConversationRequest",
    # LVO schemas
    "SkillCreate", "SkillUpdate", "SkillResponse",
    "SkillScoreCreate", "SkillScoreUpdate", "SkillScoreResponse", "SkillScoreWithSkill",
    "StudentSkillsProfile",
    "LearningPathCreate", "LearningPathUpdate", "LearningPathResponse", "LearningPathWithModules",
    "LearningModuleCreate", "LearningModuleUpdate", "LearningModuleResponse",
    "StudentLearningPathResponse", "StudentLearningPathWithDetails",
    "StudentModuleResponse", "StudentModuleWithDetails",
    "NextTaskRecommendation",
    "VerificationCreate", "VerificationUpdate", "VerificationResponse", "VerificationWithDetails",
    "VerificationRequest", "SkillVerificationSummary", "StudentVerificationProfile",
    "CredentialCreate", "CredentialUpdate", "CredentialResponse", "CredentialWithBlockchain", "CredentialWithDetails",
    "MintCredentialRequest", "MintCredentialResponse",
    "StudentCredentialsPortfolio", "ShareableCredential",
    "OnChainCredentialResponse",
]
