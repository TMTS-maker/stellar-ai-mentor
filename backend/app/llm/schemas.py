"""
Stellecta LucidAI Backend - LLM Schemas

Pydantic models for LLM requests, responses, routing, and evaluation.
"""

from typing import Optional, Literal, Dict, List, Any
from pydantic import BaseModel, Field
from datetime import datetime


# ============================================================================
# ROUTING SCHEMAS
# ============================================================================

class RoutingHints(BaseModel):
    """
    Routing hints from agents to the Multi-LLM Router.

    Agents can provide hints about task context to help routing decisions,
    but the Router makes final decisions based on policies.
    """

    task_type: Literal[
        "tutoring",
        "mastery_verification",
        "creative_exploration",
        "code_generation",
        "factual_explanation"
    ] = Field(default="tutoring")

    risk_level: Literal["low", "medium", "high"] = Field(default="medium")
    """
    Risk level of the task:
    - low: Exploration, casual learning
    - medium: Standard tutoring
    - high: Mastery verification, credential decisions
    """

    prefer_lucidai: bool = Field(default=False)
    """Hint that LucidAI should be preferred (if available)"""

    require_validation: bool = Field(default=False)
    """Hint that hybrid validation mode should be used"""

    allow_external: bool = Field(default=True)
    """Allow external LLMs to be used"""

    reason: Optional[str] = None
    """Explanation for routing hints"""


class RoutingDecision(BaseModel):
    """
    Multi-LLM Router's decision on which LLM(s) to use.
    """

    primary_llm: Literal["lucidai", "gemini", "openai", "claude", "perplexity", "deepseek"]
    """Primary LLM to query"""

    fallback_llm: Optional[Literal["lucidai", "gemini", "openai", "claude", "perplexity", "deepseek"]] = None
    """Fallback LLM if primary fails"""

    validate_with: Optional[Literal["lucidai", "gemini", "openai", "claude"]] = None
    """Secondary LLM for hybrid validation mode"""

    reason: str
    """Explanation of routing decision"""

    policy_applied: str
    """Policy name that produced this decision"""

    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    """Confidence in this routing decision"""


# ============================================================================
# LLM REQUEST/RESPONSE SCHEMAS
# ============================================================================

class LLMRequest(BaseModel):
    """
    Standardized LLM inference request.

    All LLM providers accept this format.
    """

    system_prompt: str
    """System prompt (mentor persona + context)"""

    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    """
    Conversation history:
    [
        {"role": "user", "content": "How do I solve 2x + 3 = 7?"},
        {"role": "assistant", "content": "Let's solve step by step..."}
    ]
    """

    user_message: str
    """Current user message/question"""

    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    """Sampling temperature (0 = deterministic, 2 = very random)"""

    max_tokens: int = Field(default=2000, ge=1, le=8000)
    """Maximum tokens to generate"""

    routing_hints: Optional[RoutingHints] = None
    """Optional routing hints for Multi-LLM Router"""

    metadata: Dict[str, Any] = Field(default_factory=dict)
    """Additional context metadata"""


class LLMResponse(BaseModel):
    """
    Standardized LLM inference response.

    All LLM providers return this format.
    """

    content: str
    """Generated response text"""

    llm_provider: str
    """LLM that generated this response (lucidai, gemini, openai, etc.)"""

    model_version: str
    """Specific model version used"""

    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    """Self-reported confidence (if available)"""

    tokens_input: Optional[int] = None
    """Input tokens"""

    tokens_output: Optional[int] = None
    """Output tokens"""

    inference_time_ms: Optional[int] = None
    """Inference latency in milliseconds"""

    cost_usd: Optional[float] = None
    """Estimated cost in USD"""

    metadata: Dict[str, Any] = Field(default_factory=dict)
    """Additional response metadata"""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    """Response timestamp"""


# ============================================================================
# EVALUATION SCHEMAS
# ============================================================================

class EvaluationScores(BaseModel):
    """
    Multi-dimensional quality evaluation scores.

    Based on architecture doc Section 3 (Evaluation & Scoring Layer).
    """

    correctness: float = Field(..., ge=0.0, le=1.0)
    """Factual correctness (0-1)"""

    didactic_quality: float = Field(..., ge=0.0, le=1.0)
    """
    Pedagogical quality (0-1):
    - Scaffolding appropriateness
    - Socratic method usage
    - Growth mindset language
    """

    persona_alignment: float = Field(..., ge=0.0, le=1.0)
    """Match to expected mentor voice (0-1)"""

    safety: float = Field(..., ge=0.0, le=1.0)
    """Safety and age-appropriateness (0-1)"""

    curriculum_alignment: float = Field(default=0.5, ge=0.0, le=1.0)
    """Alignment with curriculum (0-1)"""


class EvaluationResult(BaseModel):
    """
    Result of evaluating one or more LLM responses.
    """

    selected_response: LLMResponse
    """The response selected as best"""

    evaluation_scores: EvaluationScores
    """Quality scores"""

    composite_score: float = Field(..., ge=0.0, le=1.0)
    """
    Weighted composite score:
    0.3 * correctness +
    0.3 * didactic_quality +
    0.2 * persona_alignment +
    0.1 * safety +
    0.1 * curriculum_alignment
    """

    reason: str
    """Explanation of selection decision"""

    flag_for_review: bool = Field(default=False)
    """Whether to flag for human review"""

    alternative_responses: List[LLMResponse] = Field(default_factory=list)
    """Other responses considered (for hybrid mode)"""

    metadata: Dict[str, Any] = Field(default_factory=dict)
    """Additional evaluation metadata"""


# ============================================================================
# MULTI-LLM ROUTER RESPONSE
# ============================================================================

class RouterResponse(BaseModel):
    """
    Complete response from Multi-LLM Router.

    Includes:
    - Final response
    - Routing decision
    - Evaluation results
    - Performance metrics
    """

    response: LLMResponse
    """Final selected response"""

    routing_decision: RoutingDecision
    """Which LLM(s) were used and why"""

    evaluation: Optional[EvaluationResult] = None
    """Evaluation results (if multiple responses compared)"""

    metadata: Dict[str, Any] = Field(default_factory=dict)
    """Additional routing metadata"""
