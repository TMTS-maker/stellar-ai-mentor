"""
Chat API Schemas

Request and response models for chat endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


# ============================================================================
# Request Schemas
# ============================================================================


class SendMessageRequest(BaseModel):
    """Send message to mentor"""

    message: str = Field(..., min_length=1, max_length=5000, description="Student's message")
    session_id: Optional[uuid.UUID] = Field(None, description="Optional existing session ID")
    mentor_id: Optional[str] = Field(
        None, description="Optional preferred mentor (stella, max, etc.)"
    )


class CreateSessionRequest(BaseModel):
    """Create new chat session"""

    mentor_id: str = Field(..., description="Mentor ID")
    subject: Optional[str] = Field(None, description="Subject area")


# ============================================================================
# Response Schemas
# ============================================================================


class MessageResponse(BaseModel):
    """Single message in a conversation"""

    id: uuid.UUID
    role: str  # 'user' or 'assistant'
    content: str
    mentor_id: Optional[str] = None
    timestamp: datetime
    xp_earned: int = 0

    class Config:
        from_attributes = True


class SendMessageResponse(BaseModel):
    """Response after sending a message"""

    text: str  # Mentor's response text
    mentor_id: str
    mentor_name: str
    session_id: uuid.UUID
    message_id: uuid.UUID
    xp_earned: int
    total_xp: int
    current_level: int
    llm_provider: Optional[str] = None
    tokens_used: Optional[int] = None
    streak: Optional[dict] = None  # Streak information
    new_badges: Optional[list] = None  # Newly awarded badges


class SessionResponse(BaseModel):
    """Conversation session info"""

    id: uuid.UUID
    mentor_id: str
    subject: str
    start_time: datetime
    message_count: int
    total_xp_earned: int
    is_active: bool

    class Config:
        from_attributes = True


class SessionHistoryResponse(BaseModel):
    """Student's session history"""

    sessions: List[SessionResponse]
    total_sessions: int


class SessionMessagesResponse(BaseModel):
    """All messages in a session"""

    session_id: uuid.UUID
    messages: List[MessageResponse]
    total_messages: int


# ============================================================================
# Mentor Info Schemas
# ============================================================================


class MentorInfo(BaseModel):
    """Information about an AI mentor"""

    agent_id: str
    name: str
    subject: str
    personality: str
    created_at: str


class MentorListResponse(BaseModel):
    """List of all available mentors"""

    mentors: List[MentorInfo]
    total_mentors: int
