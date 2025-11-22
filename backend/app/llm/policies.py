"""
Stellecta LucidAI Backend - Routing Policies

Intelligent routing policies for Multi-LLM Router.

Based on Architecture Document Section 6.1: Multi-LLM Routing

Routing decisions based on:
- Task type (tutoring, verification, creative, code_gen)
- Risk level (low, medium, high)
- Student context (H-PEM, age, proficiency)
- Domain specificity (core subjects vs. niche)
- LucidAI confidence and availability
- System load
"""

from typing import Optional, Dict, Any, Literal
from app.llm.schemas import RoutingDecision, RoutingHints
from app.config import settings


class RoutingPolicyEngine:
    """
    Routing Policy Engine.

    Makes intelligent decisions about which LLM(s) to use based on:
    - Task context
    - Student state
    - LLM availability
    - Performance history

    Implements the decision tree from Architecture Document Section 6.1.
    """

    def __init__(self):
        """Initialize routing policy engine."""
        self.default_provider = settings.default_llm_provider
        self.fallback_provider = settings.fallback_llm_provider
        self.enable_hybrid = settings.enable_hybrid_mode
        self.confidence_threshold = settings.routing_confidence_threshold

    async def decide_routing(
        self,
        hints: Optional[RoutingHints] = None,
        context: Optional[Dict[str, Any]] = None,
        llm_availability: Optional[Dict[str, bool]] = None,
    ) -> RoutingDecision:
        """
        Make routing decision based on task context and hints.

        Args:
            hints: Optional routing hints from agents
            context: Student/task context (H-PEM, age, subject, etc.)
            llm_availability: Dict of {provider_name: is_available}

        Returns:
            RoutingDecision with selected LLM(s)
        """

        # Default availability (assume all configured)
        if llm_availability is None:
            llm_availability = {
                "lucidai": False,  # Stub for Phase 0
                "gemini": True,
                "openai": True,
                "claude": True,
                "perplexity": False,
                "deepseek": False,
            }

        # Extract task type and risk level
        task_type = hints.task_type if hints else "tutoring"
        risk_level = hints.risk_level if hints else "medium"

        # ====================================================================
        # DECISION TREE (from Architecture Doc Section 6.1)
        # ====================================================================

        # Path 1: MASTERY VERIFICATION (High Risk)
        if task_type == "mastery_verification" or risk_level == "high":
            return await self._route_high_risk_task(hints, context, llm_availability)

        # Path 2: CREATIVE EXPLORATION
        if task_type == "creative_exploration":
            return await self._route_creative_task(hints, context, llm_availability)

        # Path 3: CODE GENERATION
        if task_type == "code_generation":
            return await self._route_code_task(hints, context, llm_availability)

        # Path 4: STANDARD TUTORING (Most common)
        return await self._route_tutoring_task(hints, context, llm_availability)

    async def _route_high_risk_task(
        self,
        hints: Optional[RoutingHints],
        context: Optional[Dict[str, Any]],
        llm_availability: Dict[str, bool],
    ) -> RoutingDecision:
        """
        Route high-risk tasks (mastery verification, credential decisions).

        Strategy:
        - Prefer LucidAI if confidence > 0.9
        - Use hybrid validation (LucidAI + external) if confidence 0.7-0.9
        - Use external + escalate if LucidAI confidence < 0.7
        """

        # Check if LucidAI is available
        if llm_availability.get("lucidai"):
            # TODO (Phase 2): Get LucidAI confidence prediction
            # For Phase 0, assume medium confidence
            lucidai_confidence = 0.75

            if lucidai_confidence > 0.9:
                # High confidence: Use LucidAI solo
                return RoutingDecision(
                    primary_llm="lucidai",
                    fallback_llm="gemini" if llm_availability.get("gemini") else None,
                    validate_with=None,
                    reason="High-risk task with high LucidAI confidence",
                    policy_applied="high_risk_lucidai_solo",
                    confidence=lucidai_confidence,
                )
            elif lucidai_confidence >= 0.7:
                # Medium confidence: Hybrid validation
                validate_with = "gemini" if llm_availability.get("gemini") else "openai"
                return RoutingDecision(
                    primary_llm="lucidai",
                    fallback_llm="gemini",
                    validate_with=validate_with,
                    reason="High-risk task: hybrid validation (LucidAI + external)",
                    policy_applied="high_risk_hybrid",
                    confidence=lucidai_confidence,
                )

        # LucidAI unavailable or low confidence: Use external + flag for review
        primary = "gemini" if llm_availability.get("gemini") else "openai"
        return RoutingDecision(
            primary_llm=primary,
            fallback_llm="openai" if primary != "openai" else "claude",
            validate_with=None,
            reason="High-risk task: LucidAI unavailable, using external with review flag",
            policy_applied="high_risk_external_escalate",
            confidence=0.7,
        )

    async def _route_creative_task(
        self,
        hints: Optional[RoutingHints],
        context: Optional[Dict[str, Any]],
        llm_availability: Dict[str, bool],
    ) -> RoutingDecision:
        """
        Route creative/exploratory tasks.

        Strategy:
        - External LLMs (GPT-4, Claude) excel at creativity
        - LucidAI if task is within core subjects
        """

        # Check if task is core subject (math, science, language)
        subject = context.get("subject") if context else None
        core_subjects = ["math", "physics", "chemistry", "biology", "language", "english"]

        if subject and subject.lower() in core_subjects:
            # Core subject creativity: LucidAI can handle if available
            if llm_availability.get("lucidai"):
                return RoutingDecision(
                    primary_llm="lucidai",
                    fallback_llm="gpt4",
                    validate_with=None,
                    reason="Creative task in core subject: LucidAI capable",
                    policy_applied="creative_core_lucidai",
                    confidence=0.8,
                )

        # General creativity: Prefer GPT-4 or Claude
        if llm_availability.get("openai"):
            return RoutingDecision(
                primary_llm="openai",
                fallback_llm="claude" if llm_availability.get("claude") else "gemini",
                validate_with=None,
                reason="Creative task: GPT-4 excels at open-ended generation",
                policy_applied="creative_gpt4",
                confidence=0.85,
            )

        # Fallback to Gemini
        return RoutingDecision(
            primary_llm="gemini",
            fallback_llm="lucidai" if llm_availability.get("lucidai") else None,
            validate_with=None,
            reason="Creative task: Using Gemini (GPT-4 unavailable)",
            policy_applied="creative_gemini",
            confidence=0.75,
        )

    async def _route_code_task(
        self,
        hints: Optional[RoutingHints],
        context: Optional[Dict[str, Any]],
        llm_availability: Dict[str, bool],
    ) -> RoutingDecision:
        """
        Route code generation tasks.

        Strategy:
        - GPT-4 or Claude (best for code)
        - LucidAI for educational code (teaching programming concepts)
        """

        # Educational coding (teaching concepts): LucidAI if available
        if context and context.get("educational_code"):
            if llm_availability.get("lucidai"):
                return RoutingDecision(
                    primary_llm="lucidai",
                    fallback_llm="openai",
                    validate_with=None,
                    reason="Educational coding: LucidAI trained on teaching programming",
                    policy_applied="code_educational_lucidai",
                    confidence=0.8,
                )

        # General code generation: GPT-4 or Claude
        if llm_availability.get("openai"):
            return RoutingDecision(
                primary_llm="openai",
                fallback_llm="claude" if llm_availability.get("claude") else "gemini",
                validate_with=None,
                reason="Code generation: GPT-4 excels at programming tasks",
                policy_applied="code_gpt4",
                confidence=0.9,
            )

        if llm_availability.get("claude"):
            return RoutingDecision(
                primary_llm="claude",
                fallback_llm="gemini",
                validate_with=None,
                reason="Code generation: Claude strong at coding",
                policy_applied="code_claude",
                confidence=0.85,
            )

        # Fallback
        return RoutingDecision(
            primary_llm="gemini",
            fallback_llm=None,
            validate_with=None,
            reason="Code generation: Gemini fallback",
            policy_applied="code_gemini",
            confidence=0.7,
        )

    async def _route_tutoring_task(
        self,
        hints: Optional[RoutingHints],
        context: Optional[Dict[str, Any]],
        llm_availability: Dict[str, bool],
    ) -> RoutingDecision:
        """
        Route standard tutoring tasks (most common).

        Strategy:
        - Struggling students (H-PEM < 0.5): LucidAI (scaffolding expert)
        - Normal students (H-PEM 0.5-0.9): LucidAI primary, external fallback
        - Advanced students (H-PEM > 0.9): External for enrichment
        """

        # Extract student H-PEM if available
        h_pem = None
        if context:
            h_pem = context.get("h_pem_proficiency")

        # Struggling students: LucidAI excels at scaffolding
        if h_pem is not None and h_pem < 0.5:
            if llm_availability.get("lucidai"):
                return RoutingDecision(
                    primary_llm="lucidai",
                    fallback_llm="gemini",
                    validate_with=None,
                    reason="Struggling student (H-PEM<0.5): LucidAI scaffolding expert",
                    policy_applied="tutoring_struggling_lucidai",
                    confidence=0.85,
                )

        # Advanced students: External for enrichment
        if h_pem is not None and h_pem > 0.9:
            primary = "openai" if llm_availability.get("openai") else "gemini"
            return RoutingDecision(
                primary_llm=primary,
                fallback_llm="claude" if llm_availability.get("claude") else None,
                validate_with=None,
                reason="Advanced student (H-PEM>0.9): External LLM for enrichment",
                policy_applied="tutoring_advanced_external",
                confidence=0.8,
            )

        # Normal students: LucidAI primary if available
        if llm_availability.get("lucidai"):
            return RoutingDecision(
                primary_llm="lucidai",
                fallback_llm="gemini",
                validate_with=None,
                reason="Standard tutoring: LucidAI primary",
                policy_applied="tutoring_normal_lucidai",
                confidence=0.8,
            )

        # LucidAI unavailable: Use configured default
        return RoutingDecision(
            primary_llm=self.default_provider,
            fallback_llm=self.fallback_provider,
            validate_with=None,
            reason=f"Standard tutoring: Using configured default ({self.default_provider})",
            policy_applied="tutoring_default",
            confidence=0.75,
        )

    async def should_use_hybrid_mode(
        self,
        task_type: str,
        risk_level: str,
        confidence: float,
    ) -> bool:
        """
        Determine if hybrid validation mode should be used.

        Hybrid mode:
        - Query both LucidAI and external LLM
        - Compare responses
        - Select best or blend

        Use when:
        - High-risk tasks
        - Medium confidence (0.7-0.9)
        - Hybrid mode enabled in config

        Args:
            task_type: Type of task
            risk_level: Risk level
            confidence: Confidence in single-LLM decision

        Returns:
            bool: True if hybrid mode should be used
        """

        if not self.enable_hybrid:
            return False

        # Always use hybrid for high-risk
        if risk_level == "high":
            return True

        # Use hybrid if confidence is borderline
        if 0.7 <= confidence < self.confidence_threshold:
            return True

        return False
