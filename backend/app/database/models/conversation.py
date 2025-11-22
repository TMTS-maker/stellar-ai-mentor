"""
Stellecta LucidAI Backend - Conversation Models

Conversation and message tracking.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.database.engine import Base


class ConversationStatus(str, enum.Enum):
    """Conversation status enum"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ESCALATED = "escalated"


class MessageSender(str, enum.Enum):
    """Message sender enum"""
    STUDENT = "student"
    MENTOR = "mentor"
    SYSTEM = "system"


class Conversation(Base):
    """
    Conversation entity.

    Represents a learning conversation between a student and a mentor.
    """

    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False, index=True)

    # Conversation Details
    mentor_id = Column(String(50), nullable=False, index=True)
    """Mentor persona ID (e.g., 'stella', 'max', 'nova')"""

    status = Column(SQLEnum(ConversationStatus), default=ConversationStatus.ACTIVE, nullable=False)

    # Subject & Context
    subject = Column(String(100), nullable=True, index=True)
    """Subject domain (e.g., 'math', 'physics', 'chemistry')"""

    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")
    llm_interactions = relationship("LLMInteraction", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.id}, student_id={self.student_id}, mentor={self.mentor_id})>"


class ConversationMessage(Base):
    """
    Conversation message entity.

    Individual messages within a conversation.
    """

    __tablename__ = "conversation_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True)

    # Message Details
    sender = Column(SQLEnum(MessageSender), nullable=False)
    message = Column(Text, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    llm_interaction = relationship("LLMInteraction", back_populates="message", uselist=False)

    def __repr__(self):
        return f"<ConversationMessage(id={self.id}, sender={self.sender})>"
