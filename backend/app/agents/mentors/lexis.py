"""
Lexis - Language & Literature Mentor

Expressive and articulate language arts guide who fosters love of reading and writing
"""
from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter
from typing import Dict, Any


class LexisMentor(BaseAgent):
    """Lexis - Language & Literature Mentor"""

    def __init__(self):
        super().__init__(
            agent_id="lexis",
            name="Lexis",
            subject="LANGUAGE",
            personality="Expressive and articulate, fosters love of reading, writing, and communication"
        )
        self.llm_router = MultiLLMRouter()

    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        student = context.get('student', {})
        curriculum = context.get('curriculum', {})

        return f"""You are Lexis, an expressive and articulate language arts mentor!

STUDENT: Grade {student.get('grade', 'N/A')} | Mastery: {student.get('h_pem_level', 0.0):.1f}/10

YOUR STYLE:
- Celebrate the **power of words** and storytelling
- Make grammar and writing engaging, not tedious
- Use literary examples and quotes
- Encourage creative expression
- Build vocabulary through context
- Foster critical reading and analysis

TEACHING APPROACH:
1. Start with an engaging quote or literary example
2. Explain the language concept clearly
3. Show how it's used by great writers
4. Encourage the student to try it themselves
5. Provide constructive feedback

Focus areas:
- Reading comprehension
- Writing skills (essays, creative writing)
- Grammar and syntax
- Vocabulary development
- Literary analysis
- Communication skills

Make language beautiful and empowering! Help them find their voice!"""

    async def generate_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_context(context)
        system_prompt = self.build_system_prompt(context)

        llm_response = await self.llm_router.route_and_generate(
            prompt=message,
            context={'system_prompt': system_prompt, **context},
            routing_hints={'subject': self.subject, 'curriculum_aligned': True, 'complexity': 'medium'}
        )

        return {
            'text': llm_response['text'],
            'mentor_id': self.agent_id,
            'llm_provider': llm_response['provider'],
            'model_name': llm_response['model'],
            'tokens_used': llm_response['tokens_used'],
            'objective_id': self.extract_learning_objective(context),
            'metadata': {**llm_response.get('metadata', {}), 'subject_area': 'language_arts'}
        }
