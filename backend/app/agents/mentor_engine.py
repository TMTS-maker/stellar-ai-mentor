"""
Mentor Engine - Assembles prompts and orchestrates mentor conversations.

This module handles:
- Prompt template rendering with context (including grade-specific adaptation)
- Conversation history management
- LLM routing and invocation
- LVO phase detection and adaptation
"""
from typing import List, Optional, Dict, Any
from .schemas import (
    MentorPersona,
    StudentContext,
    ConversationMessage,
    ChatResponse,
    LVOPhase
)
from .personas import get_mentor_by_id
from .config.mentor_grade_profiles import get_grade_band_for_grade
from ..llm.router import get_llm_router
from ..llm.providers.base import Message


class MentorEngine:
    """
    Core engine for mentor-student interactions.

    Handles prompt assembly, context injection, and LLM communication.
    """

    def __init__(self):
        self.llm_router = get_llm_router()

    def build_system_prompt(
        self,
        mentor: MentorPersona,
        student_context: Optional[StudentContext] = None
    ) -> str:
        """
        Build the complete system prompt for a mentor.

        Renders the template with:
        - Age range
        - Subjects
        - Student context (age, skill level, LVO phase, history)
        - Language preference

        Args:
            mentor: The mentor persona
            student_context: Student information for personalization

        Returns:
            Fully rendered system prompt
        """
        # Base template variables
        template_vars = {
            "age_min": mentor.age_min,
            "age_max": mentor.age_max,
            "subjects": ", ".join(mentor.subjects),
        }

        # Build context string
        context_parts = []

        if student_context:
            # Grade takes priority over age for pedagogical adaptation
            if student_context.grade:
                grade_band = get_grade_band_for_grade(student_context.grade)
                context_parts.append(f"Student grade: {student_context.grade} ({grade_band})")
                # Also mention age if available for additional context
                if student_context.age:
                    context_parts.append(f"Student age: {student_context.age}")
            elif student_context.age:
                # Only age provided
                context_parts.append(f"Student age: {student_context.age}")

            if student_context.skill_level:
                context_parts.append(f"Skill level: {student_context.skill_level}")

            if student_context.lvo_phase and student_context.lvo_phase != LVOPhase.AUTO:
                context_parts.append(f"Current learning phase: {student_context.lvo_phase.value.upper()}")

            if student_context.history_summary:
                context_parts.append(f"Conversation history: {student_context.history_summary}")

            if student_context.active_goals:
                goals = ", ".join(student_context.active_goals)
                context_parts.append(f"Learning goals: {goals}")

            if student_context.language and student_context.language != "English":
                context_parts.append(f"Preferred language: {student_context.language}")

        # Combine context
        context_string = "\n".join(context_parts) if context_parts else "First interaction with this student."

        template_vars["context"] = context_string
        template_vars["language"] = student_context.language if student_context else "English"

        # Render template
        return mentor.system_prompt_template.format(**template_vars)

    def assemble_messages(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: List[ConversationMessage]
    ) -> List[Message]:
        """
        Assemble the complete message list for the LLM.

        Args:
            system_prompt: Fully rendered system prompt
            user_message: Current user message
            conversation_history: Previous messages

        Returns:
            List of Message objects ready for LLM
        """
        messages = [Message(role="system", content=system_prompt)]

        # Add conversation history (exclude old system messages)
        for msg in conversation_history:
            if msg.role != "system":
                messages.append(Message(role=msg.role, content=msg.content))

        # Add current user message
        messages.append(Message(role="user", content=user_message))

        return messages

    async def chat(
        self,
        mentor_id: str,
        message: str,
        student_context: Optional[StudentContext] = None,
        conversation_history: Optional[List[ConversationMessage]] = None,
        provider: Optional[str] = None,
        temperature: float = 0.7
    ) -> ChatResponse:
        """
        Execute a chat interaction with a mentor.

        Args:
            mentor_id: ID of the mentor to use
            message: User's message
            student_context: Student context for personalization
            conversation_history: Previous messages
            provider: LLM provider override
            temperature: LLM temperature

        Returns:
            ChatResponse with mentor's reply

        Raises:
            ValueError: If mentor not found
        """
        # Get mentor persona
        mentor = get_mentor_by_id(mentor_id)
        if not mentor:
            raise ValueError(f"Mentor '{mentor_id}' not found")

        # Build system prompt
        system_prompt = self.build_system_prompt(mentor, student_context)

        # Assemble messages
        messages = self.assemble_messages(
            system_prompt=system_prompt,
            user_message=message,
            conversation_history=conversation_history or []
        )

        # Call LLM
        response = await self.llm_router.complete(
            messages=messages,
            provider=provider,
            temperature=temperature
        )

        # Detect LVO phase (simple heuristic - can be enhanced)
        detected_phase = self._detect_lvo_phase(message, response.content)

        return ChatResponse(
            mentor_id=mentor.id,
            mentor_name=mentor.display_name,
            message=response.content,
            provider_used=response.provider,
            model_used=response.model,
            lvo_phase_detected=detected_phase,
            metadata={
                "usage": response.usage,
                "temperature": temperature
            }
        )

    def _detect_lvo_phase(self, user_message: str, assistant_response: str) -> Optional[LVOPhase]:
        """
        Simple heuristic to detect which LVO phase the conversation is in.

        This is a basic implementation. Can be enhanced with ML-based classification.

        Args:
            user_message: User's message
            assistant_response: Mentor's response

        Returns:
            Detected LVO phase
        """
        user_lower = user_message.lower()
        response_lower = assistant_response.lower()

        # VERIFY indicators
        verify_keywords = ["quiz", "test", "check", "verify", "practice", "solve", "try this"]
        if any(keyword in response_lower for keyword in verify_keywords):
            return LVOPhase.VERIFY

        # OWN indicators
        own_keywords = ["teach", "explain to me", "create your own", "apply", "now you try"]
        if any(keyword in response_lower for keyword in own_keywords):
            return LVOPhase.OWN

        # LEARN indicators (questions, introductions)
        learn_keywords = ["what", "why", "how", "let's explore", "introduce", "learn about"]
        if any(keyword in user_lower for keyword in learn_keywords[:3]):  # question words
            return LVOPhase.LEARN

        # Default to LEARN for new topics
        return LVOPhase.LEARN


# Global engine instance
_mentor_engine: Optional[MentorEngine] = None


def get_mentor_engine() -> MentorEngine:
    """Get the global mentor engine instance (singleton)."""
    global _mentor_engine
    if _mentor_engine is None:
        _mentor_engine = MentorEngine()
    return _mentor_engine
