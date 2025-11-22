"""
Stellecta LucidAI Backend - Agent Schemas

Pydantic models for agent requests/responses and context.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class StudentContext(BaseModel):
    """
    Enriched student context for agent decision-making.

    Combines data from:
    - Student profile
    - H-PEM scores
    - Learning path
    - Recent activity
    """

    student_id: str
    age: Optional[int] = None
    grade_level: Optional[int] = None

    # H-PEM Metrics
    h_pem_proficiency: float = Field(default=0.5, ge=0.0, le=1.0)
    h_pem_resilience: float = Field(default=0.5, ge=0.0, le=1.0)
    h_pem_velocity: float = Field(default=0.5, ge=0.0, le=1.0)
    h_pem_engagement: float = Field(default=0.5, ge=0.0, le=1.0)
    h_pem_transfer: float = Field(default=0.5, ge=0.0, le=1.0)

    # Learning Context
    current_subject: Optional[str] = None
    weak_skills: List[str] = Field(default_factory=list)
    recent_achievements: List[str] = Field(default_factory=list)

    # Gamification
    xp: int = 0
    level: int = 1
    streak_days: int = 0

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ConversationContext(BaseModel):
    """
    Conversation-specific context.
    """

    conversation_id: str
    mentor_id: str
    subject: Optional[str] = None
    task_type: str = Field(default="tutoring")
    risk_level: str = Field(default="medium")

    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    """Recent conversation messages for context"""

    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentRequest(BaseModel):
    """
    Request to agent (Supervisor or Mentor).
    """

    student_id: str
    message: str
    conversation_id: Optional[str] = None
    mentor_id: Optional[str] = None
    """If specified, route to this mentor directly"""

    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """
    Response from agent.
    """

    message: str
    mentor_id: str
    conversation_id: str

    # Metadata
    llm_used: Optional[str] = None
    """Which LLM generated the response"""

    confidence_score: Optional[float] = None
    routing_decision: Optional[Dict[str, Any]] = None
    evaluation_scores: Optional[Dict[str, Any]] = None

    flag_for_review: bool = False
    """Whether this response should be reviewed by a teacher"""

    metadata: Dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=datetime.utcnow)
