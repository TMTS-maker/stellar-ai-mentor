"""
Agent and Mentor Pydantic schemas.

These models define the structure of AI mentor personas and conversation contexts.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class TeachingStyle(str, Enum):
    """Teaching style approaches."""
    SOCRATIC = "socratic"
    DIRECT = "direct"
    EXPLORATORY = "exploratory"
    PROJECT_BASED = "project_based"


class LVOPhase(str, Enum):
    """Learn-Verify-Own pedagogical phases."""
    LEARN = "learn"
    VERIFY = "verify"
    OWN = "own"
    AUTO = "auto"  # Auto-detect phase based on context


class MentorPersona(BaseModel):
    """
    Complete definition of an AI mentor agent.

    Includes identity, expertise, pedagogical approach, and gold-standard system prompts.
    """
    # Identity
    id: str = Field(..., description="Unique identifier (e.g., 'stella', 'max')")
    display_name: str = Field(..., description="Human-readable name")
    emoji: str = Field(..., description="Representative emoji icon")

    # Expertise
    subjects: List[str] = Field(..., description="Subject areas of expertise")
    age_min: int = Field(..., description="Minimum recommended age")
    age_max: int = Field(..., description="Maximum recommended age")

    # Personality
    personality_traits: List[str] = Field(..., description="Key personality characteristics")
    voice_tone: str = Field(..., description="Communication tone and style")

    # Pedagogical Approach
    teaching_style: TeachingStyle = Field(default=TeachingStyle.SOCRATIC)

    # LVO Strategies (Learn-Verify-Own)
    lvo_learn_strategy: str = Field(..., description="How this mentor teaches new concepts")
    lvo_verify_strategy: str = Field(..., description="How this mentor checks understanding")
    lvo_own_strategy: str = Field(..., description="How this mentor promotes mastery")

    # Gold-Standard System Prompt
    system_prompt_template: str = Field(
        ...,
        description=(
            "Rich, pedagogically-grounded system prompt template. "
            "Supports placeholders: {age_min}, {age_max}, {subjects}, {context}, {language}"
        )
    )

    # Optional metadata
    gradient: Optional[str] = Field(None, description="UI gradient class for frontend")
    description: Optional[str] = Field(None, description="Short description for UI")
    languages: List[str] = Field(default=["English"], description="Supported languages")


class SupervisorPersona(BaseModel):
    """
    The Supervisor agent that routes to appropriate mentors.

    Meta-agent responsible for:
    - Understanding student needs
    - Selecting the right mentor
    - Maintaining conversation coherence
    """
    id: str = "supervisor"
    display_name: str = "Stellecta Supervisor"
    system_prompt_template: str


class StudentContext(BaseModel):
    """
    Student context for personalized mentoring.

    Provides information about the student for differentiation and adaptation.
    """
    age: Optional[int] = Field(None, description="Student's age")
    skill_level: Optional[str] = Field(None, description="Skill level (beginner/intermediate/advanced)")
    language: str = Field(default="English", description="Preferred communication language")
    current_subject: Optional[str] = Field(None, description="Current subject of study")
    lvo_phase: LVOPhase = Field(default=LVOPhase.AUTO, description="Current learning phase")
    history_summary: Optional[str] = Field(None, description="Summary of past interactions")
    active_goals: List[str] = Field(default_factory=list, description="Current learning goals")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class ConversationMessage(BaseModel):
    """Single message in a conversation."""
    role: str = Field(..., description="Message role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request to chat with a mentor."""
    mentor_id: Optional[str] = Field(None, description="Specific mentor ID, or None to use Supervisor")
    message: str = Field(..., description="User's message")
    student_context: Optional[StudentContext] = Field(None, description="Student context for personalization")
    conversation_history: List[ConversationMessage] = Field(
        default_factory=list,
        description="Previous messages in this conversation"
    )
    provider: Optional[str] = Field(None, description="LLM provider override")
    temperature: float = Field(default=0.7, description="LLM temperature")


class ChatResponse(BaseModel):
    """Response from a mentor."""
    mentor_id: str
    mentor_name: str
    message: str
    provider_used: str
    model_used: str
    lvo_phase_detected: Optional[LVOPhase] = None
    metadata: Optional[Dict[str, Any]] = None
