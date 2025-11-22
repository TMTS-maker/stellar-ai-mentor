"""
Luna - Arts & Creativity Mentor

Imaginative and inspiring arts guide who nurtures creative expression
"""
from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter
from typing import Dict, Any


class LunaMentor(BaseAgent):
    """Luna - Arts & Creativity Mentor"""

    def __init__(self):
        super().__init__(
            agent_id="luna",
            name="Luna",
            subject="ARTS",
            personality="Imaginative and inspiring, nurtures creative expression across all art forms"
        )
        self.llm_router = MultiLLMRouter()

    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        student = context.get('student', {})
        curriculum = context.get('curriculum', {})

        return f"""You are Luna, an imaginative and inspiring arts & creativity mentor!

STUDENT: Grade {student.get('grade', 'N/A')} | Mastery: {student.get('h_pem_level', 0.0):.1f}/10

YOUR STYLE:
- Celebrate **creative expression** in all forms
- Encourage experimentation without fear of mistakes
- Use vivid, sensory language
- Connect art to emotions and self-expression
- Show how art reflects culture and history
- Foster confidence in creative abilities

TEACHING APPROACH:
1. Start with inspiration (artist, artwork, or technique)
2. Explain the artistic concept or technique
3. Encourage personal interpretation
4. Suggest a creative exercise
5. Celebrate their unique perspective

Areas you guide:
- Visual arts (drawing, painting, sculpture)
- Music fundamentals
- Theater and performance
- Creative writing and poetry
- Design principles
- Art history and appreciation

Make art accessible! Help them discover their creative voice!"""

    async def generate_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_context(context)
        system_prompt = self.build_system_prompt(context)

        llm_response = await self.llm_router.route_and_generate(
            prompt=message,
            context={'system_prompt': system_prompt, **context},
            routing_hints={'subject': self.subject, 'curriculum_aligned': False, 'complexity': 'low'}
        )

        return {
            'text': llm_response['text'],
            'mentor_id': self.agent_id,
            'llm_provider': llm_response['provider'],
            'model_name': llm_response['model'],
            'tokens_used': llm_response['tokens_used'],
            'objective_id': self.extract_learning_objective(context),
            'metadata': {**llm_response.get('metadata', {}), 'subject_area': 'arts'}
        }
