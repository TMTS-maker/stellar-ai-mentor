"""
Stellecta LucidAI Backend - Supervisor Agent

Orchestration layer for all agent interactions.

The Supervisor Agent:
1. Receives all student requests
2. Performs safety checks
3. Selects appropriate mentor
4. Delegates to Mentor Engine
5. Validates response quality
6. Handles escalation (to teachers)
7. Logs interactions

Flow:
    Student Request
      → Supervisor: Safety Check
      → Supervisor: Select Mentor
      → Mentor Engine: Generate Response (via Router)
      → Supervisor: Quality Validation
      → Supervisor: Return or Escalate
"""

from typing import Optional, Dict, Any
import structlog

from app.agents.schemas import AgentRequest, AgentResponse, StudentContext, ConversationContext
from app.agents.mentor_engine import MentorEngine
from app.agents.personas import get_all_mentors

logger = structlog.get_logger()


class SupervisorAgent:
    """
    Supervisor Agent.

    Central orchestration layer for all student-mentor interactions.

    Responsibilities:
    1. Safety controller (content filtering)
    2. Mentor selection (based on subject, context)
    3. Quality validation (check response quality)
    4. Escalation handler (route to teachers if needed)
    5. Interaction logging
    """

    def __init__(self, mentor_engine: MentorEngine):
        """
        Initialize Supervisor Agent.

        Args:
            mentor_engine: Mentor Engine instance
        """
        self.mentor_engine = mentor_engine
        self.mentors = get_all_mentors()

        logger.info("SupervisorAgent initialized", mentors=len(self.mentors))

    async def process_conversation(
        self,
        request: AgentRequest,
        student_context: StudentContext,
        conversation_context: Optional[ConversationContext] = None,
    ) -> AgentResponse:
        """
        Process student conversation request.

        Main entry point for all student interactions.

        Args:
            request: Student request
            student_context: Student context (loaded from DB)
            conversation_context: Optional conversation context

        Returns:
            AgentResponse with mentor response

        Raises:
            ValueError: If request is invalid or unsafe
        """

        logger.info(
            "Processing conversation",
            student_id=request.student_id,
            message_length=len(request.message),
        )

        # Step 1: Safety check
        safety_result = await self._check_safety(request.message, "student")
        if not safety_result["safe"]:
            return await self._handle_unsafe_content(request, safety_result)

        # Step 2: Select mentor
        if request.mentor_id:
            # Explicit mentor requested
            mentor_id = request.mentor_id
        else:
            # Auto-select based on context
            mentor_id = await self._select_mentor(request, student_context, conversation_context)

        # Step 3: Build conversation context if not provided
        if conversation_context is None:
            conversation_context = ConversationContext(
                conversation_id=request.conversation_id or "new",
                mentor_id=mentor_id,
                subject=self._infer_subject(mentor_id),
                task_type="tutoring",
                risk_level="medium",
            )

        # Step 4: Generate mentor response
        mentor_response = await self.mentor_engine.generate_response(
            mentor_id=mentor_id,
            user_message=request.message,
            student_context=student_context,
            conversation_context=conversation_context,
        )

        # Step 5: Quality validation
        quality_ok = await self._validate_quality(mentor_response)

        # Step 6: Check if escalation needed
        should_escalate = await self._should_escalate(mentor_response, student_context)

        # Step 7: Build response
        agent_response = AgentResponse(
            message=mentor_response["message"],
            mentor_id=mentor_id,
            conversation_id=conversation_context.conversation_id,
            llm_used=mentor_response.get("llm_used"),
            confidence_score=mentor_response.get("confidence_score"),
            routing_decision=mentor_response.get("routing_decision"),
            evaluation_scores=mentor_response.get("evaluation"),
            flag_for_review=should_escalate,
            metadata={
                "quality_validated": quality_ok,
                **mentor_response.get("metadata", {})
            }
        )

        # TODO: Log interaction to database
        # await self._log_interaction(request, agent_response, student_context)

        logger.info(
            "Conversation processed",
            mentor_id=mentor_id,
            escalate=should_escalate,
            quality_ok=quality_ok,
        )

        return agent_response

    async def _check_safety(self, content: str, sender: str) -> Dict[str, Any]:
        """
        Check content safety.

        Performs basic safety checks:
        - Prohibited content detection
        - Age-appropriateness
        - PII detection (for student messages)

        Phase 0: Rule-based checks
        Phase 2: ML-based safety classifier

        Args:
            content: Message content
            sender: "student" or "mentor"

        Returns:
            dict: {"safe": bool, "reason": str, "flags": [...]}
        """

        flags = []

        # Basic prohibited content check
        prohibited_keywords = [
            "violence", "weapon", "drug", "alcohol", "explicit",
            # Add more as needed
        ]

        content_lower = content.lower()
        for keyword in prohibited_keywords:
            if keyword in content_lower:
                flags.append(f"prohibited_keyword:{keyword}")

        # TODO (Phase 2): ML-based content safety classifier
        # TODO (Phase 2): Age-appropriateness check
        # TODO (Phase 2): PII detection for student messages

        safe = len(flags) == 0

        return {
            "safe": safe,
            "reason": flags[0] if flags else "passed",
            "flags": flags,
        }

    async def _handle_unsafe_content(
        self,
        request: AgentRequest,
        safety_result: Dict[str, Any],
    ) -> AgentResponse:
        """
        Handle unsafe content.

        Returns a safe, educational response and flags for review.

        Args:
            request: Original request
            safety_result: Safety check result

        Returns:
            AgentResponse with safe message
        """

        logger.warning(
            "Unsafe content detected",
            student_id=request.student_id,
            flags=safety_result["flags"],
        )

        # Return educational, safe response
        safe_message = """I noticed your message contains content that I'm not able to discuss.

Let's focus on your learning journey instead! Is there a specific subject or topic you'd like help with today?

If you're experiencing difficulties or need to talk about something serious, please reach out to your teacher or a trusted adult."""

        return AgentResponse(
            message=safe_message,
            mentor_id="system",
            conversation_id=request.conversation_id or "safety_block",
            flag_for_review=True,
            metadata={
                "safety_block": True,
                "safety_flags": safety_result["flags"],
            }
        )

    async def _select_mentor(
        self,
        request: AgentRequest,
        student_context: StudentContext,
        conversation_context: Optional[ConversationContext],
    ) -> str:
        """
        Select appropriate mentor based on context.

        Selection criteria:
        1. Explicit subject in request
        2. Student's current subject (from learning path)
        3. Conversation context
        4. Default to general mentor

        Phase 0: Simple keyword matching
        Phase 2: ML-based intent classification

        Args:
            request: Student request
            student_context: Student context
            conversation_context: Optional conversation context

        Returns:
            str: Mentor ID
        """

        message_lower = request.message.lower()

        # Subject keyword matching (simplified for Phase 0)
        subject_keywords = {
            "stella": ["math", "algebra", "geometry", "calculus", "equation", "solve", "number"],
            "max": ["physics", "force", "energy", "motion", "gravity", "experiment"],
            "nova": ["chemistry", "molecule", "reaction", "element", "compound", "lab"],
            "darwin": ["biology", "cell", "organism", "evolution", "ecosystem", "gene"],
            "lexis": ["english", "grammar", "writing", "story", "essay", "literature"],
            "neo": ["coding", "programming", "python", "ai", "algorithm", "computer"],
            "luna": ["art", "music", "painting", "drawing", "creative", "design"],
            "atlas": ["history", "geography", "culture", "civilization", "map"],
        }

        # Check for subject keywords
        for mentor_id, keywords in subject_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                logger.info("Mentor selected by keyword", mentor_id=mentor_id)
                return mentor_id

        # Use student's current subject if available
        if student_context.current_subject:
            subject_to_mentor = {
                "math": "stella",
                "physics": "max",
                "chemistry": "nova",
                "biology": "darwin",
                "english": "lexis",
                "technology": "neo",
                "arts": "luna",
                "history": "atlas",
            }
            mentor_id = subject_to_mentor.get(student_context.current_subject.lower())
            if mentor_id:
                logger.info("Mentor selected by current subject", mentor_id=mentor_id)
                return mentor_id

        # Default: Stella (most general)
        logger.info("Mentor selected by default", mentor_id="stella")
        return "stella"

    async def _validate_quality(self, mentor_response: Dict[str, Any]) -> bool:
        """
        Validate mentor response quality.

        Checks:
        - Response is not empty
        - Evaluation score is acceptable
        - No safety flags

        Args:
            mentor_response: Mentor response dict

        Returns:
            bool: True if quality is acceptable
        """

        # Check non-empty
        if not mentor_response.get("message"):
            return False

        # Check evaluation score (if available)
        evaluation = mentor_response.get("evaluation", {})
        composite_score = evaluation.get("composite_score")

        if composite_score is not None and composite_score < 0.6:
            logger.warning("Low quality response", composite_score=composite_score)
            return False

        return True

    async def _should_escalate(
        self,
        mentor_response: Dict[str, Any],
        student_context: StudentContext,
    ) -> bool:
        """
        Determine if interaction should be escalated to teacher.

        Escalate if:
        - Response flagged for review by evaluation service
        - Student is struggling significantly (H-PEM very low)
        - Safety concerns
        - Multiple failed attempts

        Args:
            mentor_response: Mentor response
            student_context: Student context

        Returns:
            bool: True if should escalate
        """

        # Check evaluation flag
        evaluation = mentor_response.get("evaluation", {})
        if evaluation.get("flag_for_review"):
            return True

        # Check student struggle (very low proficiency)
        if student_context.h_pem_proficiency < 0.3:
            logger.info("Escalating due to low proficiency", proficiency=student_context.h_pem_proficiency)
            return True

        # TODO: Check attempt history (multiple failures)
        # TODO: Check teacher intervention requests

        return False

    def _infer_subject(self, mentor_id: str) -> str:
        """
        Infer subject from mentor ID.

        Args:
            mentor_id: Mentor ID

        Returns:
            str: Subject
        """

        mentor_to_subject = {
            "stella": "math",
            "max": "physics",
            "nova": "chemistry",
            "darwin": "biology",
            "lexis": "english",
            "neo": "technology",
            "luna": "arts",
            "atlas": "history",
        }

        return mentor_to_subject.get(mentor_id, "general")
