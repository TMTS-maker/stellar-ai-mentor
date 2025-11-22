"""
Stellecta LucidAI Backend - Mentor Engine

Mentor agent implementation with persona-based prompt building.

The Mentor Engine:
1. Selects appropriate mentor persona
2. Builds context-enriched system prompts
3. Calls Multi-LLM Router
4. Returns responses with full metadata

Integration with Multi-LLM Router:
- Mentors NEVER call LLMs directly
- All calls go through router.generate()
- Routing hints provided based on context
"""

from typing import Optional, Dict, Any
import structlog

from app.agents.personas import MentorPersona, get_mentor_by_id
from app.agents.schemas import StudentContext, ConversationContext
from app.llm.router import MultiLLMRouter
from app.llm.schemas import LLMRequest, RoutingHints

logger = structlog.get_logger()


class MentorEngine:
    """
    Mentor Engine.

    Manages mentor personas and generates contextually-enriched responses.

    Each mentor has:
    - Unique personality and voice
    - Subject expertise
    - Teaching methodology
    - System prompt template

    The engine:
    1. Builds persona-specific system prompts
    2. Enriches with student context (H-PEM, weak skills, etc.)
    3. Adds routing hints for Multi-LLM Router
    4. Returns response with full metadata
    """

    def __init__(self, router: MultiLLMRouter):
        """
        Initialize Mentor Engine.

        Args:
            router: Multi-LLM Router instance
        """
        self.router = router
        logger.info("MentorEngine initialized")

    async def generate_response(
        self,
        mentor_id: str,
        user_message: str,
        student_context: StudentContext,
        conversation_context: ConversationContext,
    ) -> Dict[str, Any]:
        """
        Generate mentor response.

        Args:
            mentor_id: Mentor persona ID (e.g., 'stella', 'max')
            user_message: Student's message/question
            student_context: Student context (H-PEM, age, etc.)
            conversation_context: Conversation context

        Returns:
            dict: Response with message and metadata

        Raises:
            ValueError: If mentor not found
        """

        # Get mentor persona
        mentor = get_mentor_by_id(mentor_id)
        if not mentor:
            raise ValueError(f"Mentor '{mentor_id}' not found")

        # Build system prompt with context
        system_prompt = self._build_system_prompt(mentor, student_context, conversation_context)

        # Build routing hints
        routing_hints = self._build_routing_hints(mentor, student_context, conversation_context)

        # Create LLM request
        llm_request = LLMRequest(
            system_prompt=system_prompt,
            conversation_history=conversation_context.conversation_history,
            user_message=user_message,
            temperature=0.7,  # Balanced (not too creative, not too deterministic)
            max_tokens=2000,
            routing_hints=routing_hints,
            metadata={
                "mentor_id": mentor_id,
                "student_id": student_context.student_id,
                "conversation_id": conversation_context.conversation_id,
            }
        )

        # Call Multi-LLM Router
        logger.info(
            "Generating mentor response",
            mentor_id=mentor_id,
            student_id=student_context.student_id,
        )

        router_response = await self.router.generate(
            request=llm_request,
            context={
                "mentor_id": mentor_id,
                "student_age": student_context.age,
                "h_pem_proficiency": student_context.h_pem_proficiency,
                "subject": conversation_context.subject,
                "task_type": conversation_context.task_type,
            }
        )

        # Extract response
        return {
            "message": router_response.response.content,
            "mentor_id": mentor_id,
            "llm_used": router_response.response.llm_provider,
            "confidence_score": router_response.response.confidence_score,
            "routing_decision": {
                "primary_llm": router_response.routing_decision.primary_llm,
                "policy": router_response.routing_decision.policy_applied,
                "reason": router_response.routing_decision.reason,
            },
            "evaluation": {
                "composite_score": router_response.evaluation.composite_score if router_response.evaluation else None,
                "flag_for_review": router_response.evaluation.flag_for_review if router_response.evaluation else False,
            },
            "metadata": {
                "tokens_input": router_response.response.tokens_input,
                "tokens_output": router_response.response.tokens_output,
                "inference_time_ms": router_response.response.inference_time_ms,
                "cost_usd": router_response.response.cost_usd,
            }
        }

    def _build_system_prompt(
        self,
        mentor: MentorPersona,
        student_context: StudentContext,
        conversation_context: ConversationContext,
    ) -> str:
        """
        Build context-enriched system prompt for mentor.

        Fills in mentor's system prompt template with:
        - Student demographics (age, grade)
        - H-PEM scores
        - Weak skills and recent achievements
        - Current learning objectives

        Args:
            mentor: Mentor persona
            student_context: Student context
            conversation_context: Conversation context

        Returns:
            str: Complete system prompt
        """

        # Build student context description
        context_parts = []

        # Demographics
        if student_context.age:
            context_parts.append(f"- Student age: {student_context.age} years old")
        if student_context.grade_level:
            context_parts.append(f"- Grade level: {student_context.grade_level}")

        # H-PEM proficiency
        proficiency_level = self._proficiency_to_description(student_context.h_pem_proficiency)
        context_parts.append(f"- Proficiency level: {proficiency_level} ({student_context.h_pem_proficiency:.2f})")

        # Weak skills
        if student_context.weak_skills:
            weak_skills_str = ", ".join(student_context.weak_skills[:3])  # Top 3
            context_parts.append(f"- Needs support with: {weak_skills_str}")

        # Recent achievements
        if student_context.recent_achievements:
            achievements_str = ", ".join(student_context.recent_achievements[:2])  # Recent 2
            context_parts.append(f"- Recent achievements: {achievements_str}")

        # Gamification (for motivation)
        context_parts.append(f"- Current level: {student_context.level} (XP: {student_context.xp})")
        if student_context.streak_days > 0:
            context_parts.append(f"- Learning streak: {student_context.streak_days} days 🔥")

        # Current topic
        if conversation_context.subject:
            context_parts.append(f"- Current subject: {conversation_context.subject}")

        student_context_str = "\n".join(context_parts)

        # Fill in template
        system_prompt = mentor.system_prompt_template.format(
            student_context=student_context_str
        )

        return system_prompt

    def _build_routing_hints(
        self,
        mentor: MentorPersona,
        student_context: StudentContext,
        conversation_context: ConversationContext,
    ) -> RoutingHints:
        """
        Build routing hints for Multi-LLM Router.

        Provides context-based hints to help router make better decisions.

        Args:
            mentor: Mentor persona
            student_context: Student context
            conversation_context: Conversation context

        Returns:
            RoutingHints
        """

        # Determine task type
        task_type = conversation_context.task_type

        # Determine risk level
        risk_level = conversation_context.risk_level

        # Prefer LucidAI for struggling students (scaffolding expert)
        prefer_lucidai = student_context.h_pem_proficiency < 0.5

        # Require validation for high-risk tasks
        require_validation = risk_level == "high"

        return RoutingHints(
            task_type=task_type,
            risk_level=risk_level,
            prefer_lucidai=prefer_lucidai,
            require_validation=require_validation,
            reason=f"Mentor {mentor.id} request with H-PEM={student_context.h_pem_proficiency:.2f}",
        )

    def _proficiency_to_description(self, proficiency: float) -> str:
        """
        Convert H-PEM proficiency score to human-readable description.

        Args:
            proficiency: Proficiency score (0-1)

        Returns:
            str: Description
        """

        if proficiency >= 0.9:
            return "Advanced (mastery level)"
        elif proficiency >= 0.7:
            return "Proficient (strong understanding)"
        elif proficiency >= 0.5:
            return "Developing (making progress)"
        elif proficiency >= 0.3:
            return "Emerging (needs support)"
        else:
            return "Beginning (requires significant scaffolding)"
