"""
Base Agent Abstract Class

Defines the interface that all mentor agents must implement
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime


class BaseAgent(ABC):
    """
    Abstract base class for all AI mentor agents

    All mentor agents (Stella, Max, Nova, etc.) inherit from this class
    and must implement the required methods.
    """

    def __init__(self, agent_id: str, name: str, subject: str, personality: str):
        """
        Initialize base agent

        Args:
            agent_id: Unique identifier (e.g., 'stella', 'max')
            name: Display name (e.g., 'Stella', 'Max')
            subject: Primary subject area (e.g., 'MATH', 'PHYSICS')
            personality: Personality description
        """
        self.agent_id = agent_id
        self.name = name
        self.subject = subject
        self.personality = personality
        self.created_at = datetime.utcnow()

    @abstractmethod
    async def generate_response(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate response to student message

        Args:
            message: Student's message text
            context: Context including student info, curriculum, session data

        Returns:
            Dict containing:
                - text: Response message
                - mentor_id: This agent's ID
                - llm_provider: Which LLM was used
                - tokens_used: Token count
                - objective_id: Related curriculum objective (if any)
                - metadata: Additional response metadata
        """
        pass

    @abstractmethod
    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        """
        Build system prompt with context

        Args:
            context: Student and curriculum context

        Returns:
            System prompt string for LLM
        """
        pass

    def get_persona_description(self) -> str:
        """
        Get persona description for this agent

        Returns:
            Formatted persona description
        """
        return f"{self.name} - {self.subject} Mentor\n{self.personality}"

    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get agent information

        Returns:
            Dict with agent details
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "subject": self.subject,
            "personality": self.personality,
            "created_at": self.created_at.isoformat()
        }

    def validate_context(self, context: Dict[str, Any]) -> bool:
        """
        Validate that context has required fields

        Args:
            context: Context dictionary

        Returns:
            True if valid, raises ValueError if not
        """
        required_fields = ['student', 'curriculum']

        for field in required_fields:
            if field not in context:
                raise ValueError(f"Context missing required field: {field}")

        return True

    def extract_learning_objective(self, context: Dict[str, Any]) -> Optional[str]:
        """
        Extract current learning objective from context

        Args:
            context: Context dictionary

        Returns:
            Objective ID or None
        """
        curriculum = context.get('curriculum', {})
        objectives = curriculum.get('current_objectives', [])

        if objectives and len(objectives) > 0:
            return objectives[0].get('id')

        return None
