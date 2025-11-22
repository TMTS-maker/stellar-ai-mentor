"""
Conversation and Message Models
"""
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
from datetime import datetime


class ConversationSession(Base):
    """Chat session between student and mentor"""
    __tablename__ = "conversation_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    mentor_id = Column(String(50), nullable=False)  # stella, max, nova, etc.
    subject = Column(String(50), nullable=False)

    # Session info
    start_time = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    end_time = Column(TIMESTAMP, nullable=True)
    is_active = Column(Boolean, default=True)

    # Analytics
    message_count = Column(Integer, default=0)
    total_xp_earned = Column(Integer, default=0)

    # Metadata
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    """Individual message in a conversation"""
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id"), nullable=False)

    # Message details
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    mentor_id = Column(String(50), nullable=True)  # Only for assistant messages

    # LLM metadata
    llm_provider = Column(String(50), nullable=True)  # 'lucidai', 'openai', 'anthropic'
    tokens_used = Column(Integer, nullable=True)
    model_name = Column(String(100), nullable=True)

    # Learning metadata
    objective_id = Column(UUID(as_uuid=True), ForeignKey("curriculum_objectives.id"), nullable=True)
    xp_earned = Column(Integer, default=0)

    # Additional metadata
    extra_metadata = Column(JSON, nullable=True)

    # Timestamps
    timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship("ConversationSession", back_populates="messages")
    objective = relationship("CurriculumObjective")
