"""
Stellecta LucidAI Backend - Evaluation Service

Multi-dimensional quality evaluation of LLM responses.

Based on Architecture Document Section 3: Evaluation & Scoring Layer

This service evaluates LLM responses across multiple dimensions:
1. Factual Correctness (0-1)
2. Didactic Quality (0-1) - scaffolding, Socratic method, growth mindset
3. Persona Alignment (0-1) - mentor voice consistency
4. Safety & Compliance (0-1) - age-appropriate, content filters
5. Curriculum Alignment (0-1) - maps to learning objectives

Composite Score:
    0.3 * correctness +
    0.3 * didactic_quality +
    0.2 * persona_alignment +
    0.1 * safety +
    0.1 * curriculum_alignment
"""

from typing import List, Optional, Dict, Any
import re

from app.llm.schemas import (
    LLMResponse,
    EvaluationScores,
    EvaluationResult,
)


class EvaluationService:
    """
    LLM Response Evaluation Service.

    Evaluates responses on multiple quality dimensions and selects
    the best response when multiple candidates are available.

    Phase 0: Rule-based and heuristic evaluation
    Phase 2+: ML-based evaluation models
    """

    def __init__(self):
        """Initialize evaluation service."""
        self.weights = {
            "correctness": 0.3,
            "didactic_quality": 0.3,
            "persona_alignment": 0.2,
            "safety": 0.1,
            "curriculum_alignment": 0.1,
        }

    async def evaluate_single(
        self,
        response: LLMResponse,
        context: Optional[Dict[str, Any]] = None,
    ) -> EvaluationResult:
        """
        Evaluate a single LLM response.

        Args:
            response: LLM response to evaluate
            context: Optional context (student, mentor, task info)

        Returns:
            EvaluationResult with scores and composite
        """

        # Calculate scores across all dimensions
        scores = await self._calculate_scores(response, context)

        # Calculate composite score
        composite = self._calculate_composite(scores)

        # Determine if flagging for review is needed
        flag_for_review = self._should_flag_for_review(scores, composite, context)

        return EvaluationResult(
            selected_response=response,
            evaluation_scores=scores,
            composite_score=composite,
            reason="Single response evaluation",
            flag_for_review=flag_for_review,
            alternative_responses=[],
            metadata={
                "evaluator": "rule_based",
                "context_available": context is not None,
            }
        )

    async def compare_responses(
        self,
        responses: List[LLMResponse],
        context: Optional[Dict[str, Any]] = None,
    ) -> EvaluationResult:
        """
        Compare multiple LLM responses and select the best.

        Used in hybrid/dual-LLM mode.

        Args:
            responses: List of LLM responses to compare
            context: Optional context

        Returns:
            EvaluationResult with best response selected
        """

        if not responses:
            raise ValueError("No responses to evaluate")

        if len(responses) == 1:
            return await self.evaluate_single(responses[0], context)

        # Evaluate all responses
        evaluations = []
        for response in responses:
            scores = await self._calculate_scores(response, context)
            composite = self._calculate_composite(scores)
            evaluations.append({
                "response": response,
                "scores": scores,
                "composite": composite,
            })

        # Sort by composite score (descending)
        evaluations.sort(key=lambda x: x["composite"], reverse=True)

        best = evaluations[0]
        alternatives = [e["response"] for e in evaluations[1:]]

        # Check consensus (how similar are the top responses?)
        consensus = self._calculate_consensus(evaluations)

        # Determine flagging
        flag_for_review = self._should_flag_for_review(
            best["scores"],
            best["composite"],
            context,
            consensus=consensus
        )

        return EvaluationResult(
            selected_response=best["response"],
            evaluation_scores=best["scores"],
            composite_score=best["composite"],
            reason=f"Best of {len(responses)} responses (consensus: {consensus:.2f})",
            flag_for_review=flag_for_review,
            alternative_responses=alternatives,
            metadata={
                "evaluator": "comparative",
                "responses_compared": len(responses),
                "consensus": consensus,
                "all_scores": [e["composite"] for e in evaluations],
            }
        )

    async def _calculate_scores(
        self,
        response: LLMResponse,
        context: Optional[Dict[str, Any]] = None,
    ) -> EvaluationScores:
        """
        Calculate all evaluation scores for a response.

        Phase 0: Rule-based heuristics
        Phase 2+: ML-based evaluation

        Args:
            response: LLM response
            context: Optional context

        Returns:
            EvaluationScores with all dimensions
        """

        # 1. Correctness (rule-based for Phase 0)
        correctness = await self._score_correctness(response, context)

        # 2. Didactic Quality
        didactic_quality = await self._score_didactic_quality(response, context)

        # 3. Persona Alignment
        persona_alignment = await self._score_persona_alignment(response, context)

        # 4. Safety
        safety = await self._score_safety(response, context)

        # 5. Curriculum Alignment
        curriculum_alignment = await self._score_curriculum_alignment(response, context)

        return EvaluationScores(
            correctness=correctness,
            didactic_quality=didactic_quality,
            persona_alignment=persona_alignment,
            safety=safety,
            curriculum_alignment=curriculum_alignment,
        )

    async def _score_correctness(
        self,
        response: LLMResponse,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Score factual correctness.

        Phase 0: Heuristic-based (response length, coherence, confidence)
        Phase 2: Cross-reference with knowledge base, verified solutions

        Returns:
            float: 0-1 score
        """

        score = 0.5  # Default neutral score

        # Heuristic 1: Non-empty response
        if response.content and len(response.content.strip()) > 10:
            score += 0.2

        # Heuristic 2: LLM self-reported confidence (if available)
        if response.confidence_score is not None:
            score = max(score, response.confidence_score)

        # Heuristic 3: Response structure (has explanation, examples)
        if self._has_explanation_structure(response.content):
            score += 0.1

        # TODO (Phase 2): Cross-reference with curriculum knowledge base
        # TODO (Phase 2): Check against verified solution keys
        # TODO (Phase 2): Use ML correctness classifier

        return min(1.0, score)

    async def _score_didactic_quality(
        self,
        response: LLMResponse,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Score pedagogical/didactic quality.

        Evaluates:
        - Scaffolding appropriateness
        - Socratic questioning (vs. direct answers)
        - Encouragement and growth mindset language
        - Age-appropriate vocabulary

        Phase 0: Rule-based heuristics
        Phase 2: ML-based didactic quality model

        Returns:
            float: 0-1 score
        """

        score = 0.5  # Default

        content = response.content.lower()

        # Heuristic 1: Contains encouraging language
        encouraging_phrases = [
            "great job", "well done", "excellent", "keep going",
            "you're on the right track", "good thinking", "try",
        ]
        if any(phrase in content for phrase in encouraging_phrases):
            score += 0.15

        # Heuristic 2: Uses questions (Socratic method)
        if "?" in response.content:
            question_count = response.content.count("?")
            score += min(0.15, question_count * 0.05)

        # Heuristic 3: Step-by-step explanation
        step_indicators = ["first", "then", "next", "finally", "step", "let's"]
        if any(word in content for word in step_indicators):
            score += 0.1

        # Heuristic 4: Avoids overwhelming the student (not too long)
        if 50 < len(response.content) < 500:
            score += 0.1

        # TODO (Phase 2): Analyze scaffolding level vs. student H-PEM
        # TODO (Phase 2): Growth mindset language detection
        # TODO (Phase 2): Age-appropriate vocabulary check
        # TODO (Phase 2): ML didactic quality classifier

        return min(1.0, score)

    async def _score_persona_alignment(
        self,
        response: LLMResponse,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Score alignment with expected mentor persona.

        Evaluates consistency with mentor voice:
        - Stella (math): systematic, patient, visual
        - Max (physics): hands-on, experimental, curious
        - Nova (chemistry): precise, safety-conscious, energetic
        - etc.

        Phase 0: Basic keyword matching
        Phase 2: Fine-tuned persona classification model

        Returns:
            float: 0-1 score
        """

        score = 0.7  # Default: assume decent alignment

        # If no mentor context, return default
        if not context or "mentor_id" not in context:
            return score

        mentor_id = context.get("mentor_id")
        content = response.content.lower()

        # Persona-specific keywords (simplified for Phase 0)
        persona_keywords = {
            "stella": ["step", "equation", "visualize", "pattern", "solve"],
            "max": ["experiment", "observe", "forces", "energy", "discover"],
            "nova": ["reaction", "molecule", "safety", "element", "bond"],
            "darwin": ["organism", "evolution", "ecosystem", "cell", "adapt"],
            "lexis": ["story", "word", "express", "write", "meaning"],
            "neo": ["code", "algorithm", "data", "ai", "logic"],
            "luna": ["create", "design", "color", "rhythm", "express"],
            "atlas": ["history", "culture", "map", "civilization", "explore"],
        }

        keywords = persona_keywords.get(mentor_id, [])
        matches = sum(1 for keyword in keywords if keyword in content)

        if matches > 0:
            score += min(0.2, matches * 0.05)

        # TODO (Phase 2): Use fine-tuned persona classifier
        # TODO (Phase 2): Analyze tone, vocabulary, teaching style

        return min(1.0, score)

    async def _score_safety(
        self,
        response: LLMResponse,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Score safety and age-appropriateness.

        Checks:
        - No prohibited content (violence, adult themes, etc.)
        - Age-appropriate language
        - No PII leakage
        - COPPA/GDPR compliance

        Phase 0: Basic keyword filtering
        Phase 2: ML-based content safety classifier

        Returns:
            float: 0-1 score (1 = completely safe, 0 = unsafe)
        """

        score = 1.0  # Assume safe unless flagged

        content = response.content.lower()

        # Prohibited content keywords (simplified)
        prohibited = [
            "violence", "weapon", "drug", "alcohol", "explicit",
            # Add more as needed
        ]

        if any(word in content for word in prohibited):
            score = 0.0  # Immediate fail

        # Check for potential PII leakage
        # Simplified: check for email patterns, phone numbers
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content):
            score -= 0.5  # Potential PII

        if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', content):
            score -= 0.5  # Potential phone number

        # Use provider safety ratings if available (e.g., Gemini safety_ratings)
        if "safety_ratings" in response.metadata:
            # Gemini provides safety ratings - use them
            ratings = response.metadata["safety_ratings"]
            for rating in ratings:
                if rating.get("probability") in ["HIGH", "MEDIUM"]:
                    score -= 0.3

        # TODO (Phase 2): Advanced content safety classifier
        # TODO (Phase 2): Age-appropriate language model
        # TODO (Phase 2): PII detection model

        return max(0.0, score)

    async def _score_curriculum_alignment(
        self,
        response: LLMResponse,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Score alignment with curriculum objectives.

        Checks if response maps to active learning objectives
        and competency frameworks.

        Phase 0: Placeholder (always returns 0.5)
        Phase 2: Link to competency database

        Returns:
            float: 0-1 score
        """

        # TODO (Phase 2): Implement curriculum mapping
        # - Check if response addresses competency in context
        # - Verify grade-level appropriateness
        # - Check alignment with school curriculum settings

        return 0.5  # Neutral placeholder

    def _calculate_composite(self, scores: EvaluationScores) -> float:
        """
        Calculate weighted composite score.

        Composite = 0.3*correctness + 0.3*didactic + 0.2*persona + 0.1*safety + 0.1*curriculum

        Args:
            scores: Individual dimension scores

        Returns:
            float: Composite score (0-1)
        """

        composite = (
            self.weights["correctness"] * scores.correctness +
            self.weights["didactic_quality"] * scores.didactic_quality +
            self.weights["persona_alignment"] * scores.persona_alignment +
            self.weights["safety"] * scores.safety +
            self.weights["curriculum_alignment"] * scores.curriculum_alignment
        )

        return composite

    def _calculate_consensus(self, evaluations: List[Dict]) -> float:
        """
        Calculate consensus score between multiple evaluations.

        High consensus (>0.8): Responses agree
        Low consensus (<0.5): Responses contradict

        Args:
            evaluations: List of evaluation dicts with 'composite' scores

        Returns:
            float: Consensus score (0-1)
        """

        if len(evaluations) < 2:
            return 1.0

        scores = [e["composite"] for e in evaluations]
        avg_score = sum(scores) / len(scores)

        # Calculate variance
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5

        # Normalize: low std_dev = high consensus
        # If std_dev = 0 (all same), consensus = 1
        # If std_dev = 0.5 (huge spread), consensus = 0
        consensus = max(0.0, 1.0 - (std_dev * 2))

        return consensus

    def _should_flag_for_review(
        self,
        scores: EvaluationScores,
        composite: float,
        context: Optional[Dict[str, Any]] = None,
        consensus: Optional[float] = None,
    ) -> bool:
        """
        Determine if response should be flagged for human review.

        Flag if:
        - Safety score is low (<0.7)
        - Composite score is low (<0.6)
        - Consensus is low (<0.5) in multi-response comparison
        - High-stakes task (mastery verification) with medium confidence

        Args:
            scores: Evaluation scores
            composite: Composite score
            context: Optional context
            consensus: Optional consensus score (multi-response)

        Returns:
            bool: True if should flag for review
        """

        # Safety: always flag if unsafe
        if scores.safety < 0.7:
            return True

        # Low composite score
        if composite < 0.6:
            return True

        # Low consensus in multi-response mode
        if consensus is not None and consensus < 0.5:
            return True

        # High-stakes tasks with borderline scores
        if context and context.get("task_type") == "mastery_verification":
            if composite < 0.85:
                return True

        return False

    def _has_explanation_structure(self, content: str) -> bool:
        """
        Check if response has explanation structure.

        Looks for:
        - Multiple sentences
        - Examples or demonstrations
        - Step-by-step indicators

        Args:
            content: Response content

        Returns:
            bool: True if has structure
        """

        # Multiple sentences
        if content.count(".") < 2:
            return False

        # Has examples
        if "example" in content.lower() or "for instance" in content.lower():
            return True

        # Has steps
        if any(word in content.lower() for word in ["first", "second", "step 1", "step 2"]):
            return True

        return False
