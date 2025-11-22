"""
Supervisor Agent - Routes students to the appropriate mentor.

The Supervisor is a meta-agent that:
- Analyzes student questions
- Determines the best mentor for the task
- Routes conversations appropriately (with grade-aware logic)
- Handles general platform questions
"""
from typing import Optional, Dict, Any, List
import re
from .schemas import (
    StudentContext,
    ConversationMessage,
    ChatResponse,
    LVOPhase
)
from .personas import get_supervisor, MENTOR_PERSONAS
from .mentor_engine import get_mentor_engine
from .config.mentor_grade_profiles import get_recommended_mentors_for_grade, get_grade_band_for_grade
from ..llm.router import get_llm_router
from ..llm.providers.base import Message


class SupervisorAgent:
    """
    Supervisor agent for intelligent routing.

    Uses the LLM to determine which mentor is best suited for a student's question.
    """

    def __init__(self):
        self.supervisor_persona = get_supervisor()
        self.llm_router = get_llm_router()
        self.mentor_engine = get_mentor_engine()

    def build_supervisor_prompt(
        self,
        student_context: Optional[StudentContext] = None
    ) -> str:
        """
        Build the supervisor's system prompt with context.

        Args:
            student_context: Student information

        Returns:
            Rendered supervisor prompt
        """
        context_parts = []

        if student_context:
            if student_context.grade:
                grade_band = get_grade_band_for_grade(student_context.grade)
                context_parts.append(f"Student grade: {student_context.grade} ({grade_band})")

            if student_context.age:
                context_parts.append(f"Student age: {student_context.age}")

            if student_context.current_subject:
                context_parts.append(f"Current subject: {student_context.current_subject}")

            if student_context.history_summary:
                context_parts.append(f"History: {student_context.history_summary}")

        context_string = "\n".join(context_parts) if context_parts else "New student interaction."

        return self.supervisor_persona.system_prompt_template.format(context=context_string)

    def _get_grade_aware_recommendations(
        self,
        student_context: Optional[StudentContext],
        message: str
    ) -> List[str]:
        """
        Get grade-aware mentor recommendations based on student context.

        This provides pre-filtering to help the supervisor choose appropriate mentors.

        Args:
            student_context: Student context
            message: User's message (for subject detection)

        Returns:
            List of recommended mentor IDs
        """
        if not student_context or not student_context.grade:
            return []

        # Extract subject from context or message
        subject = student_context.current_subject or None
        if not subject:
            # Simple keyword matching in message
            message_lower = message.lower()
            if any(word in message_lower for word in ["math", "algebra", "geometry", "calculus"]):
                subject = "math"
            elif any(word in message_lower for word in ["physics", "force", "energy", "motion"]):
                subject = "physics"
            elif any(word in message_lower for word in ["chemistry", "chemical", "molecule", "atom"]):
                subject = "chemistry"
            elif any(word in message_lower for word in ["biology", "cell", "organism", "genetics"]):
                subject = "biology"
            elif any(word in message_lower for word in ["english", "reading", "writing", "literature"]):
                subject = "english"
            elif any(word in message_lower for word in ["coding", "program", "ai", "technology", "python"]):
                subject = "tech"
            elif any(word in message_lower for word in ["art", "music", "draw", "paint", "sing"]):
                subject = "art"
            elif any(word in message_lower for word in ["history", "geography", "ancient", "war"]):
                subject = "history"

        recommended = get_recommended_mentors_for_grade(student_context.grade, subject)
        return recommended

    async def route(
        self,
        message: str,
        student_context: Optional[StudentContext] = None,
        conversation_history: Optional[List[ConversationMessage]] = None,
        provider: Optional[str] = None
    ) -> ChatResponse:
        """
        Route a student's message to the appropriate mentor or handle directly.

        Uses grade-aware logic when grade is provided for better routing decisions.

        Args:
            message: Student's message
            student_context: Student context (including optional grade)
            conversation_history: Previous messages
            provider: LLM provider override

        Returns:
            ChatResponse (either supervisor's direct response or routed to mentor)
        """
        # Get grade-aware recommendations (if applicable)
        recommended_mentors = self._get_grade_aware_recommendations(student_context, message)

        # Build supervisor system prompt
        system_prompt = self.build_supervisor_prompt(student_context)

        # If we have grade-aware recommendations, add them to the context
        if recommended_mentors:
            rec_string = ", ".join(recommended_mentors)
            system_prompt += f"\n\nRECOMMENDED MENTORS for this grade level: {rec_string}"

        # Assemble messages
        messages = [Message(role="system", content=system_prompt)]

        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                if msg.role != "system":
                    messages.append(Message(role=msg.role, content=msg.content))

        # Add current message
        messages.append(Message(role="user", content=message))

        # Get supervisor's response
        response = await self.llm_router.complete(
            messages=messages,
            provider=provider,
            temperature=0.7
        )

        supervisor_response = response.content

        # Check if supervisor is routing to a specific mentor
        route_match = re.search(r'\[ROUTE_TO:\s*(\w+)\]', supervisor_response)

        if route_match:
            mentor_id = route_match.group(1).lower()

            # Verify mentor exists
            if mentor_id not in MENTOR_PERSONAS:
                # Supervisor hallucinated a mentor - handle gracefully
                return ChatResponse(
                    mentor_id="supervisor",
                    mentor_name="Stellecta Supervisor",
                    message=f"I'd like to connect you with a mentor, but I need to understand your question better. Could you tell me more about what you'd like to learn?",
                    provider_used=response.provider,
                    model_used=response.model,
                    metadata={"routing_error": "Invalid mentor ID"}
                )

            # Extract the supervisor's message (remove routing tag)
            supervisor_message = re.sub(r'\[ROUTE_TO:\s*\w+\]\s*', '', supervisor_response).strip()

            # Route to the mentor
            mentor_response = await self.mentor_engine.chat(
                mentor_id=mentor_id,
                message=message,
                student_context=student_context,
                conversation_history=conversation_history,
                provider=provider
            )

            # Prepend supervisor's introduction if present
            if supervisor_message:
                mentor_response.message = f"{supervisor_message}\n\n{mentor_response.message}"

            return mentor_response

        else:
            # Supervisor is handling the question directly
            return ChatResponse(
                mentor_id="supervisor",
                mentor_name="Stellecta Supervisor",
                message=supervisor_response,
                provider_used=response.provider,
                model_used=response.model,
                metadata={"direct_response": True}
            )


# Global supervisor instance
_supervisor_agent: Optional[SupervisorAgent] = None


def get_supervisor_agent() -> SupervisorAgent:
    """Get the global supervisor agent instance (singleton)."""
    global _supervisor_agent
    if _supervisor_agent is None:
        _supervisor_agent = SupervisorAgent()
    return _supervisor_agent
