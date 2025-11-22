"""
H-PEM Framework Integration

H-PEM represents four key pedagogical strategies:
- History: Leverage past learning and build continuity
- Practice: Provide varied, spaced practice opportunities
- Evaluation: Continuous formative assessment
- Metacognition: Promote self-awareness and reflection

This module provides utilities for integrating H-PEM into mentor interactions.
"""
from typing import Optional, Dict, Any


class HPEMStrategy:
    """
    H-PEM strategy manager.

    Provides guidance for implementing History, Practice, Evaluation, and Metacognition
    in mentor-student interactions.
    """

    @staticmethod
    def generate_history_prompt(previous_topics: list) -> str:
        """
        Generate a prompt snippet that references learning history.

        Args:
            previous_topics: List of previously covered topics

        Returns:
            History-aware prompt snippet
        """
        if not previous_topics:
            return ""

        topics_str = ", ".join(previous_topics[:3])  # Last 3 topics
        return f"Building on what we've covered ({topics_str}), "

    @staticmethod
    def generate_practice_suggestion(skill: str, difficulty: str = "medium") -> str:
        """
        Generate practice recommendations.

        Args:
            skill: The skill to practice
            difficulty: Difficulty level (easy, medium, hard)

        Returns:
            Practice suggestion text
        """
        suggestions = {
            "easy": f"Try some basic {skill} exercises to build confidence.",
            "medium": f"Practice {skill} with varied problems to deepen understanding.",
            "hard": f"Challenge yourself with advanced {skill} applications."
        }
        return suggestions.get(difficulty, suggestions["medium"])

    @staticmethod
    def generate_evaluation_questions(topic: str) -> list:
        """
        Generate formative evaluation questions for a topic.

        Args:
            topic: The topic being evaluated

        Returns:
            List of evaluation question templates
        """
        return [
            f"Can you explain {topic} in your own words?",
            f"What's the key idea behind {topic}?",
            f"How would you apply {topic} to a real-world problem?",
            f"What questions do you still have about {topic}?"
        ]

    @staticmethod
    def generate_metacognitive_prompts(context: str = "learning") -> list:
        """
        Generate metacognitive reflection prompts.

        Args:
            context: Context for reflection (learning, problem-solving, etc.)

        Returns:
            List of metacognitive prompts
        """
        prompts = {
            "learning": [
                "What strategies helped you understand this?",
                "What was the most challenging part?",
                "How confident do you feel about this topic?",
                "What would you do differently next time?"
            ],
            "problem-solving": [
                "How did you approach this problem?",
                "What strategies did you try?",
                "If you got stuck, what helped you move forward?",
                "What did you learn from solving this?"
            ],
            "general": [
                "How did you figure that out?",
                "What was your thinking process?",
                "What clues helped you?",
                "How does this connect to what you already know?"
            ]
        }
        return prompts.get(context, prompts["general"])

    @staticmethod
    def build_hpem_context(
        history: Optional[str] = None,
        practice_level: str = "medium",
        evaluation_needed: bool = True,
        metacognition_enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Build a complete H-PEM context dictionary.

        Args:
            history: Historical context string
            practice_level: Difficulty level for practice
            evaluation_needed: Whether to include evaluation
            metacognition_enabled: Whether to include metacognitive prompts

        Returns:
            H-PEM context dictionary
        """
        return {
            "history": history or "",
            "practice_level": practice_level,
            "evaluation_needed": evaluation_needed,
            "metacognition_enabled": metacognition_enabled
        }
