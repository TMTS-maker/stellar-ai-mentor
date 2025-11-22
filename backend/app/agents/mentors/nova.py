"""
Nova - Chemistry Mentor

Curious and experimental chemistry guide who makes reactions fascinating
"""

from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter
from typing import Dict, Any


class NovaMentor(BaseAgent):
    """Nova - Chemistry Mentor"""

    def __init__(self):
        super().__init__(
            agent_id="nova",
            name="Nova",
            subject="CHEMISTRY",
            personality="Curious and experimental, uses vivid descriptions of chemical reactions",
        )
        self.llm_router = MultiLLMRouter()

    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        student = context.get("student", {})
        curriculum = context.get("curriculum", {})

        return f"""You are Nova, a curious and experimental chemistry mentor!

STUDENT: Grade {student.get('grade', 'N/A')} | Mastery: {student.get('h_pem_level', 0.0):.1f}/10

YOUR STYLE:
- Make chemistry **visual and exciting** with vivid descriptions
- Explain reactions like telling a story
- Connect chemistry to everyday life (cooking, cleaning, nature)
- Use analogies with colors, smells, and transformations
- Emphasize safety when discussing experiments
- Show how atoms and molecules interact like characters in a story

APPROACH:
1. Start with a fascinating example or phenomenon
2. Explain the chemistry behind it clearly
3. Describe what's happening at the molecular level
4. Connect to real-world applications
5. Suggest safe observations they can make

Make chemistry come alive! Show them the magic in everyday reactions!"""

    async def generate_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_context(context)
        system_prompt = self.build_system_prompt(context)

        llm_response = await self.llm_router.route_and_generate(
            prompt=message,
            context={"system_prompt": system_prompt, **context},
            routing_hints={"subject": self.subject, "curriculum_aligned": True},
        )

        return {
            "text": llm_response["text"],
            "mentor_id": self.agent_id,
            "llm_provider": llm_response["provider"],
            "model_name": llm_response["model"],
            "tokens_used": llm_response["tokens_used"],
            "objective_id": self.extract_learning_objective(context),
            "metadata": {**llm_response.get("metadata", {}), "subject_area": "chemistry"},
        }
