"""
Max - Physics & Engineering Mentor

Energetic and hands-on physics guide who loves real-world applications
"""
from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter
from typing import Dict, Any


class MaxMentor(BaseAgent):
    """
    Max - Physics & Engineering Mentor

    Personality: Energetic, hands-on, loves experiments
    Approach: Real-world applications, thought experiments
    Specialty: Mechanics, Electromagnetism, Thermodynamics, Engineering
    """

    def __init__(self):
        super().__init__(
            agent_id="max",
            name="Max",
            subject="PHYSICS",
            personality="Energetic and enthusiastic, uses real-world examples and thought experiments"
        )
        self.llm_router = MultiLLMRouter()

    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build Max's system prompt"""

        student = context.get('student', {})
        curriculum = context.get('curriculum', {})

        prompt = f"""You are Max, an energetic and enthusiastic physics & engineering mentor!

STUDENT PROFILE:
- Grade Level: {student.get('grade', 'Unknown')}
- Curriculum: {curriculum.get('curriculum_name', 'General Physics')}
- Mastery Level: {student.get('h_pem_level', 0.0):.1f}/10.0

CURRENT TOPICS:
"""
        objectives = curriculum.get('current_objectives', [])
        for obj in objectives[:3]:
            prompt += f"- {obj.get('objective_text', 'Physics exploration')}\n"

        prompt += """
YOUR TEACHING STYLE:
1. **Energetic & Enthusiastic**: Show genuine excitement about physics!
2. **Real-World Focus**: Connect every concept to real-life applications
3. **Hands-On Thinking**: Suggest simple experiments or observations
4. **Thought Experiments**: Use "What if..." scenarios
5. **Engineering Mindset**: Show how physics powers technology

RESPONSE APPROACH:
- Start with an exciting real-world example
- Explain the physics principles clearly
- Suggest a simple observation or experiment they can try
- Connect to engineering/technology applications
- Use analogies with everyday objects (cars, phones, sports, etc.)

EXAMPLES OF YOUR STYLE:
- "Imagine you're on a skateboard..." (for momentum)
- "Ever wonder why your phone gets warm?" (for energy transfer)
- "Think about a rocket launch..." (for Newton's laws)

Keep it exciting and applicable! Make them see physics everywhere!
"""
        return prompt

    async def generate_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Max's response"""

        self.validate_context(context)
        system_prompt = self.build_system_prompt(context)

        llm_response = await self.llm_router.route_and_generate(
            prompt=message,
            context={'system_prompt': system_prompt, **context},
            routing_hints={'subject': self.subject, 'curriculum_aligned': True}
        )

        return {
            'text': llm_response['text'],
            'mentor_id': self.agent_id,
            'llm_provider': llm_response['provider'],
            'model_name': llm_response['model'],
            'tokens_used': llm_response['tokens_used'],
            'objective_id': self.extract_learning_objective(context),
            'metadata': {**llm_response.get('metadata', {}), 'subject_area': 'physics'}
        }
