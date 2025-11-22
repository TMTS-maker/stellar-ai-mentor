"""
Agent and Mentor Pydantic schemas.

These models define the structure of AI mentor personas and conversation contexts.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# ==============================================================================
# GRADE-TO-AGE MAPPING
# ==============================================================================

def grade_to_age(grade: int) -> int:
    """
    Map grade level (1-12) to typical age.

    Standard US grade-to-age mapping:
    - Grade 1: Age 6-7 (use 6)
    - Grade 2: Age 7-8 (use 7)
    - ...
    - Grade 12: Age 17-18 (use 17)

    Args:
        grade: Grade level (1-12)

    Returns:
        Typical age for that grade
    """
    if not 1 <= grade <= 12:
        raise ValueError(f"Grade must be between 1 and 12, got {grade}")

    # Grade 1 starts at age 6
    return grade + 5


def age_to_grade_range(age: int) -> tuple:
    """
    Map age to typical grade range (since ages can span two grades).

    Args:
        age: Student's age

    Returns:
        Tuple of (min_grade, max_grade)
    """
    if age < 6:
        return (1, 1)  # Pre-school/Kindergarten → treat as Grade 1
    elif age >= 18:
        return (12, 12)  # Post-high school → treat as Grade 12

    # Age 6 could be K or G1, use G1 as minimum
    # Age 7 could be G1 or G2, etc.
    min_grade = max(1, age - 5)
    max_grade = min(12, age - 4)

    return (min_grade, max_grade)


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
    grade_min: int = Field(..., description="Minimum recommended grade (1-12)")
    grade_max: int = Field(..., description="Maximum recommended grade (1-12)")

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
    grade: Optional[int] = Field(None, description="Student's grade level (1-12)", ge=1, le=12)
    skill_level: Optional[str] = Field(None, description="Skill level (beginner/intermediate/advanced)")
    language: str = Field(default="English", description="Preferred communication language")
    current_subject: Optional[str] = Field(None, description="Current subject of study")
    lvo_phase: LVOPhase = Field(default=LVOPhase.AUTO, description="Current learning phase")
    history_summary: Optional[str] = Field(None, description="Summary of past interactions")
    active_goals: List[str] = Field(default_factory=list, description="Current learning goals")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")

    def get_effective_age(self) -> Optional[int]:
        """
        Get the effective age for routing, preferring grade-based age if grade is provided.

        Returns:
            Age (uses grade-to-age mapping if grade is provided, otherwise raw age)
        """
        if self.grade is not None:
            return grade_to_age(self.grade)
        return self.age


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
