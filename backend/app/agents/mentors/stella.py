"""
Stella - Mathematics Mentor

Patient and encouraging math tutor who makes complex concepts accessible
"""

from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter
from typing import Dict, Any


class StellaMentor(BaseAgent):
    """
    Stella - Mathematics Mentor

    Personality: Patient, encouraging, uses visual analogies
    Approach: Step-by-step breakdowns, real-world examples
    Specialty: Algebra, Geometry, Calculus, Statistics
    """

    def __init__(self):
        super().__init__(
            agent_id="stella",
            name="Stella",
            subject="MATH",
            personality="Patient and encouraging, uses step-by-step explanations with real-world analogies",
        )
        self.llm_router = MultiLLMRouter()

    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build Stella's system prompt with student context"""

        student = context.get("student", {})
        curriculum = context.get("curriculum", {})

        prompt = f"""You are Stella, a patient and encouraging mathematics tutor.

STUDENT PROFILE:
- Grade Level: {student.get('grade', 'Unknown')}
- Curriculum: {curriculum.get('curriculum_name', 'General Math')}
- H-PEM Mastery Level: {student.get('h_pem_level', 0.0):.1f}/10.0
- Current Level: {student.get('current_level', 1)}

CURRENT LEARNING OBJECTIVES:
"""

        objectives = curriculum.get("current_objectives", [])
        if objectives:
            for obj in objectives[:3]:  # Show top 3 objectives
                prompt += (
                    f"- [{obj.get('objective_code', 'N/A')}] {obj.get('objective_text', 'N/A')}\n"
                )
        else:
            prompt += "- General mathematics exploration\n"

        prompt += """
YOUR TEACHING STYLE:
1. **Patient & Encouraging**: Always maintain a supportive tone
2. **Step-by-Step**: Break down complex problems into manageable steps
3. **Real-World Examples**: Use everyday analogies (e.g., "Think of fractions like pizza slices")
4. **Visual Thinking**: Describe concepts visually when possible
5. **Check Understanding**: Ask follow-up questions to ensure comprehension
6. **Curriculum-Aligned**: Reference the learning objectives when relevant

RESPONSE STRUCTURE:
1. Acknowledge the student's question positively
2. Explain the concept clearly at an appropriate grade level
3. Provide a concrete example
4. Check understanding with a gentle question
5. Encourage further questions

IMPORTANT GUIDELINES:
- Use age-appropriate language for grade level
- Never give direct answers to homework - guide them to discover
- Celebrate small wins and progress
- If stuck, offer hints rather than solutions
- Reference curriculum objectives when teaching concepts
- Keep responses concise (2-3 paragraphs max)

Remember: Your goal is to build confidence and genuine understanding, not just provide answers!
"""
        return prompt

    async def generate_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Stella's response to student message"""

        # Validate context
        self.validate_context(context)

        # Build system prompt
        system_prompt = self.build_system_prompt(context)

        # Prepare context for LLM
        llm_context = {"system_prompt": system_prompt, **context}

        # Route to LLM with hints
        llm_response = await self.llm_router.route_and_generate(
            prompt=message,
            context=llm_context,
            routing_hints={
                "subject": self.subject,
                "curriculum_aligned": True,
                "complexity": "medium",
            },
        )

        # Extract objective ID if relevant
        objective_id = self.extract_learning_objective(context)

        # Return formatted response
        return {
            "text": llm_response["text"],
            "mentor_id": self.agent_id,
            "llm_provider": llm_response["provider"],
            "model_name": llm_response["model"],
            "tokens_used": llm_response["tokens_used"],
            "objective_id": objective_id,
            "metadata": {
                **llm_response.get("metadata", {}),
                "teaching_style": "step_by_step",
                "subject_area": "mathematics",
            },
        }
