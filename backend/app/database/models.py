"""
Database models (SQLAlchemy).

This is a basic stub. Full implementation would include:
- User model
- Conversation model
- Message model
- Progress tracking
- Gamification data (XP, achievements)
- LVO phase tracking
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model (stub)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    active = Column(Boolean, default=True)

    # Relationships
    conversations = relationship("Conversation", back_populates="user")


class Conversation(Base):
    """Conversation model (stub)."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentor_id = Column(String(50), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    lvo_phase = Column(String(20), default="learn")

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    """Message model (stub)."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    provider = Column(String(50))
    model = Column(String(100))

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Achievement(Base):
    """Achievement model (stub)."""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_name = Column(String(100), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)
    xp_awarded = Column(Integer, default=0)
