"""
Supervisor Agent - Routes students to the appropriate mentor.

The Supervisor is a meta-agent that:
- Analyzes student questions
- Determines the best mentor for the task
- Routes conversations appropriately
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
            if student_context.age:
                context_parts.append(f"Student age: {student_context.age}")

            if student_context.current_subject:
                context_parts.append(f"Current subject: {student_context.current_subject}")

            if student_context.history_summary:
                context_parts.append(f"History: {student_context.history_summary}")

        context_string = "\n".join(context_parts) if context_parts else "New student interaction."

        return self.supervisor_persona.system_prompt_template.format(context=context_string)

    async def route(
        self,
        message: str,
        student_context: Optional[StudentContext] = None,
        conversation_history: Optional[List[ConversationMessage]] = None,
        provider: Optional[str] = None
    ) -> ChatResponse:
        """
        Route a student's message to the appropriate mentor or handle directly.

        Args:
            message: Student's message
            student_context: Student context
            conversation_history: Previous messages
            provider: LLM provider override

        Returns:
            ChatResponse (either supervisor's direct response or routed to mentor)
        """
        # Build supervisor system prompt
        system_prompt = self.build_supervisor_prompt(student_context)

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
