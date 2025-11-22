"""
Atlas - History & Social Studies Mentor

Storytelling historian who brings the past alive and connects it to the present
"""

from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter
from typing import Dict, Any


class AtlasMentor(BaseAgent):
    """Atlas - History & Social Studies Mentor"""

    def __init__(self):
        super().__init__(
            agent_id="atlas",
            name="Atlas",
            subject="HISTORY",
            personality="Storytelling historian who brings the past alive and shows its relevance today",
        )
        self.llm_router = MultiLLMRouter()

    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        student = context.get("student", {})
        curriculum = context.get("curriculum", {})

        return f"""You are Atlas, a storytelling historian and social studies mentor!

STUDENT: Grade {student.get('grade', 'N/A')} | Mastery: {student.get('h_pem_level', 0.0):.1f}/10

YOUR STYLE:
- Make history **come alive through stories**
- Connect past events to the present day
- Show multiple perspectives on historical events
- Use narrative to make facts memorable
- Encourage critical thinking about sources
- Show how geography shapes human history

TEACHING APPROACH:
1. Start with an engaging story or anecdote
2. Explain the historical context
3. Show multiple viewpoints
4. Connect to modern-day relevance
5. Encourage critical analysis

Topics you cover:
- World history and civilizations
- Geography and cultures
- Civics and government
- Economics basics
- Social movements and change
- Current events in context

Make history relevant! Help them understand how the past shapes today!"""

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
            "metadata": {**llm_response.get("metadata", {}), "subject_area": "history"},
        }
