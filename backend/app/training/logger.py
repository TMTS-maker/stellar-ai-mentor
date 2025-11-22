"""
Stellecta LucidAI Backend - LLM Interaction Logger

Logs all LLM interactions for training data pipeline.

CRITICAL for LucidAI training:
- Captures every LLM request/response
- Stores routing decisions and evaluation results
- Links to conversations for context
- Feeds into anonymization pipeline

Privacy:
- Logs include conversation_id (can be linked to student)
- Anonymization happens in separate service
- Full data retained for X days (config), then anonymized
"""

from typing import Optional, Dict, Any
from uuid import UUID
import structlog

from app.database.engine import SessionLocal
from app.database.models import LLMInteraction
from app.llm.schemas import RouterResponse

logger = structlog.get_logger()


class LLMInteractionLogger:
    """
    LLM Interaction Logger.

    Logs all LLM interactions to database for:
    - Performance monitoring
    - Training data collection
    - Cost tracking
    - Routing policy optimization
    """

    async def log_interaction(
        self,
        conversation_id: UUID,
        message_id: UUID,
        router_response: RouterResponse,
        context: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """
        Log LLM interaction to database.

        Args:
            conversation_id: Conversation UUID
            message_id: Message UUID
            router_response: Complete router response
            context: Optional context

        Returns:
            UUID: LLMInteraction ID
        """

        db = SessionLocal()
        try:
            # Extract data from router response
            response = router_response.response
            routing_decision = router_response.routing_decision
            evaluation = router_response.evaluation

            # Prepare routing decision JSON
            routing_decision_dict = {
                "primary_llm": routing_decision.primary_llm,
                "fallback_llm": routing_decision.fallback_llm,
                "validate_with": routing_decision.validate_with,
                "reason": routing_decision.reason,
                "policy_applied": routing_decision.policy_applied,
                "confidence": routing_decision.confidence,
            }

            # Prepare evaluation scores JSON
            evaluation_scores_dict = None
            if evaluation:
                evaluation_scores_dict = {
                    "correctness": evaluation.evaluation_scores.correctness,
                    "didactic_quality": evaluation.evaluation_scores.didactic_quality,
                    "persona_alignment": evaluation.evaluation_scores.persona_alignment,
                    "safety": evaluation.evaluation_scores.safety,
                    "curriculum_alignment": evaluation.evaluation_scores.curriculum_alignment,
                }

            # Prepare alternative responses JSON
            alternative_responses_list = []
            if evaluation and evaluation.alternative_responses:
                for alt in evaluation.alternative_responses:
                    alternative_responses_list.append({
                        "llm": alt.llm_provider,
                        "response": alt.content,
                        "confidence": alt.confidence_score,
                    })

            # Determine LLMs queried
            llms_queried = [routing_decision.primary_llm]
            if routing_decision.validate_with:
                llms_queried.append(routing_decision.validate_with)

            # Create LLMInteraction record
            interaction = LLMInteraction(
                conversation_id=conversation_id,
                message_id=message_id,
                # Request metadata
                task_type=context.get("task_type") if context else None,
                risk_level=context.get("risk_level") if context else None,
                # Routing
                routing_decision=routing_decision_dict,
                llms_queried=llms_queried,
                # Response
                llm_used=response.llm_provider,
                model_version=response.model_version,
                response_text=response.content,
                confidence_score=response.confidence_score,
                # Evaluation
                evaluation_scores=evaluation_scores_dict,
                composite_score=evaluation.composite_score if evaluation else None,
                # Performance
                inference_time_ms=response.inference_time_ms,
                tokens_input=response.tokens_input,
                tokens_output=response.tokens_output,
                cost_usd=response.cost_usd,
                # Alternatives
                alternative_responses=alternative_responses_list if alternative_responses_list else None,
            )

            db.add(interaction)
            db.commit()
            db.refresh(interaction)

            logger.info(
                "LLM interaction logged",
                interaction_id=str(interaction.id),
                llm_used=response.llm_provider,
                conversation_id=str(conversation_id),
            )

            return interaction.id

        except Exception as e:
            logger.error("Failed to log LLM interaction", error=str(e))
            db.rollback()
            raise

        finally:
            db.close()
