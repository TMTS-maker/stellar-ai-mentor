"""
LVO Phase Management

Learn-Verify-Own is a pedagogical framework that structures learning into three phases:
- LEARN: Introduction and exploration of new concepts
- VERIFY: Practice and assessment to check understanding
- OWN: Mastery and application of learned skills

This module provides utilities for managing LVO phases in conversations.
"""
from typing import Optional, List
from ..agents.schemas import LVOPhase, ConversationMessage


class LVOPhaseManager:
    """
    Manages LVO phase detection and transitions.

    Future enhancements:
    - ML-based phase classification
    - Automatic phase progression
    - Personalized pacing
    """

    @staticmethod
    def detect_phase(
        message: str,
        conversation_history: Optional[List[ConversationMessage]] = None
    ) -> LVOPhase:
        """
        Detect the current LVO phase based on conversation content.

        This is a simple heuristic-based implementation.
        Can be enhanced with ML classification.

        Args:
            message: Current user message
            conversation_history: Previous messages

        Returns:
            Detected LVO phase
        """
        message_lower = message.lower()

        # VERIFY phase indicators
        verify_keywords = [
            "test", "quiz", "practice", "check", "solve",
            "how do i", "can you check", "is this correct"
        ]
        if any(keyword in message_lower for keyword in verify_keywords):
            return LVOPhase.VERIFY

        # OWN phase indicators
        own_keywords = [
            "explain", "teach", "how would i", "apply",
            "create", "build", "design", "my own"
        ]
        if any(keyword in message_lower for keyword in own_keywords):
            return LVOPhase.OWN

        # LEARN phase (default for questions and new topics)
        learn_keywords = ["what is", "why", "how does", "tell me about", "introduce"]
        if any(keyword in message_lower for keyword in learn_keywords):
            return LVOPhase.LEARN

        # Default to LEARN
        return LVOPhase.LEARN

    @staticmethod
    def suggest_next_phase(current_phase: LVOPhase) -> LVOPhase:
        """
        Suggest the next logical phase in the LVO progression.

        Args:
            current_phase: Current phase

        Returns:
            Suggested next phase
        """
        phase_progression = {
            LVOPhase.LEARN: LVOPhase.VERIFY,
            LVOPhase.VERIFY: LVOPhase.OWN,
            LVOPhase.OWN: LVOPhase.LEARN,  # Cycle to new topic
            LVOPhase.AUTO: LVOPhase.LEARN
        }
        return phase_progression.get(current_phase, LVOPhase.LEARN)

    @staticmethod
    def get_phase_guidance(phase: LVOPhase) -> str:
        """
        Get guidance text for a specific LVO phase.

        Args:
            phase: The LVO phase

        Returns:
            Guidance string for mentors
        """
        guidance = {
            LVOPhase.LEARN: (
                "Focus on introducing concepts clearly, using examples and analogies. "
                "Check understanding frequently with formative questions."
            ),
            LVOPhase.VERIFY: (
                "Provide practice opportunities and assessment tasks. "
                "Use Socratic questioning to probe understanding. "
                "Identify and address misconceptions."
            ),
            LVOPhase.OWN: (
                "Encourage application and creative use of learned concepts. "
                "Have students teach back or apply to new contexts. "
                "Celebrate mastery and independence."
            ),
            LVOPhase.AUTO: "Automatically detect the appropriate phase based on context."
        }
        return guidance.get(phase, "")
