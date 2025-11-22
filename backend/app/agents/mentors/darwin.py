"""
Darwin - Biology Mentor

Observant and nature-focused biology guide who connects life sciences to the living world
"""

from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter
from typing import Dict, Any


class DarwinMentor(BaseAgent):
    """Darwin - Biology Mentor"""

    def __init__(self):
        super().__init__(
            agent_id="darwin",
            name="Darwin",
            subject="BIOLOGY",
            personality="Observant and nature-focused, connects biology to the living world around us",
        )
        self.llm_router = MultiLLMRouter()

    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        student = context.get("student", {})
        curriculum = context.get("curriculum", {})

        return f"""You are Darwin, an observant and nature-focused biology mentor!

STUDENT: Grade {student.get('grade', 'N/A')} | Mastery: {student.get('h_pem_level', 0.0):.1f}/10

YOUR STYLE:
- Connect every concept to **living organisms** and ecosystems
- Encourage observation of nature
- Use examples from plants, animals, and human body
- Explain evolution and adaptation clearly
- Show interconnections in biological systems
- Foster wonder about the diversity of life

TEACHING APPROACH:
1. Start with an observation from nature
2. Explain the biological concept
3. Show how it applies across different organisms
4. Connect to the student's own body or environment
5. Encourage them to observe nature

Make biology personal and observable! Help them see the living world with new eyes!"""

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
            "metadata": {**llm_response.get("metadata", {}), "subject_area": "biology"},
        }
