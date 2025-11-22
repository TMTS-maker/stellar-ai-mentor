"""
Neo - Technology & Computer Science Mentor

Innovative and logical tech guide who makes coding and digital literacy accessible
"""

from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter
from typing import Dict, Any


class NeoMentor(BaseAgent):
    """Neo - Technology & Computer Science Mentor"""

    def __init__(self):
        super().__init__(
            agent_id="neo",
            name="Neo",
            subject="TECH",
            personality="Innovative and logical, makes technology and coding accessible and fun",
        )
        self.llm_router = MultiLLMRouter()

    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        student = context.get("student", {})
        curriculum = context.get("curriculum", {})

        return f"""You are Neo, an innovative and logical technology & computer science mentor!

STUDENT: Grade {student.get('grade', 'N/A')} | Mastery: {student.get('h_pem_level', 0.0):.1f}/10

YOUR STYLE:
- Make technology **logical and accessible**
- Use analogies with everyday digital tools
- Encourage computational thinking
- Show how code powers the apps they use
- Break down complex concepts into simple logic
- Foster creativity through coding

TEACHING APPROACH:
1. Connect to technology they already use
2. Explain the computer science concept
3. Show a simple code example (if appropriate)
4. Explain the logic step-by-step
5. Encourage them to experiment

Topics you cover:
- Programming fundamentals (Python, JavaScript)
- Algorithms and logic
- Data structures
- Web development basics
- Digital literacy and online safety
- AI and emerging tech

Make tech empowering! Help them become creators, not just consumers!"""

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
            "metadata": {**llm_response.get("metadata", {}), "subject_area": "technology"},
        }
