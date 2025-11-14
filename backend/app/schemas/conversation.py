"""Conversation-related Pydantic schemas"""
from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.models.conversation import MessageSender


class ConversationSessionCreate(BaseModel):
    """Schema for conversation session creation"""
    task_id: Optional[UUID] = None
    avatar_type: Optional[str] = None


class ConversationSessionResponse(BaseModel):
    """Schema for conversation session response"""
    id: UUID
    student_id: UUID
    task_id: Optional[UUID] = None
    avatar_type: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConversationMessageCreate(BaseModel):
    """Schema for conversation message creation"""
    session_id: UUID
    sender: MessageSender
    text: str
    audio_url: Optional[str] = None
    metadata: Optional[dict] = None


class ConversationMessageResponse(BaseModel):
    """Schema for conversation message response"""
    id: UUID
    session_id: UUID
    sender: MessageSender
    text: str
    audio_url: Optional[str] = None
    timestamp: datetime
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True


class TextConversationRequest(BaseModel):
    """Schema for text conversation request"""
    task_id: Optional[UUID] = None
    message: str


class TextConversationResponse(BaseModel):
    """Schema for text conversation response"""
    reply: str
    xp_bonus: int = 0
    session_id: UUID


class VoiceConversationRequest(BaseModel):
    """Schema for voice conversation request (multipart with audio file)"""
    task_id: Optional[UUID] = None


class VoiceConversationResponse(BaseModel):
    """Schema for voice conversation response"""
    transcription: str
    reply: str
    audio_url: Optional[str] = None
    avatar_video_url: Optional[str] = None
    xp_bonus: int = 0
    session_id: UUID
