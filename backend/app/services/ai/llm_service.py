"""LLM service for conversation and tutoring"""
from typing import List, Dict, Optional
from app.config import settings


# System prompt template for Stellar AI tutor
SYSTEM_PROMPT = """
You are Stellar AI, an educational tutor designed for children aged 6–14.

You speak warmly, simply, clearly, and encouragingly.
You adapt to the child's age and skill level.
You help them learn through conversation, feedback, and gamified tasks.

Rules:
- Always encourage the student.
- Break concepts into small steps.
- Use simple grammar for younger children.
- Celebrate progress and effort.
- Correct mistakes gently.
- Do not use adult or complex terminology.
"""


class LLMService:
    """
    Large Language Model service abstraction.
    Supports OpenAI and Anthropic providers.
    """

    @staticmethod
    async def generate_response(
        messages: List[Dict[str, str]],
        student_name: Optional[str] = None,
        student_age: Optional[int] = None,
        task_context: Optional[str] = None,
        max_tokens: int = 500
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            student_name: Student's name for personalization
            student_age: Student's age for adaptation
            task_context: Context about the current task
            max_tokens: Maximum tokens in response

        Returns:
            Generated response text

        Note:
            Set LLM_PROVIDER and corresponding API key in .env
        """
        # Build system message with context
        system_message = SYSTEM_PROMPT

        if student_name:
            system_message += f"\n\nYou are currently speaking with {student_name}."

        if student_age:
            system_message += f"\nThe student is {student_age} years old."

        if task_context:
            system_message += f"\n\nCurrent task context: {task_context}"

        # Prepare conversation with system prompt
        conversation = [{"role": "system", "content": system_message}] + messages

        # Truncate if too long (keep last 10 messages + system)
        if len(conversation) > 11:
            conversation = [conversation[0]] + conversation[-10:]

        # Route to appropriate provider
        if settings.LLM_PROVIDER == "openai":
            return await LLMService._call_openai(conversation, max_tokens)
        elif settings.LLM_PROVIDER == "anthropic":
            return await LLMService._call_anthropic(conversation, max_tokens)
        else:
            # Stub if no provider configured
            return "[LLM stub response - Please configure LLM_PROVIDER and API key in .env]"

    @staticmethod
    async def _call_openai(messages: List[Dict], max_tokens: int) -> str:
        """Call OpenAI API"""
        if not settings.OPENAI_API_KEY:
            return "[OpenAI API key not configured]"

        try:
            import httpx

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o",
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": 0.7
                    }
                )
                response.raise_for_status()

                result = response.json()
                return result["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"OpenAI LLM Error: {e}")
            return f"[LLM error: {str(e)}]"

    @staticmethod
    async def _call_anthropic(messages: List[Dict], max_tokens: int) -> str:
        """Call Anthropic Claude API"""
        if not settings.ANTHROPIC_API_KEY:
            return "[Anthropic API key not configured]"

        try:
            import httpx

            # Convert messages format (Anthropic requires system separate)
            system_message = ""
            claude_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    claude_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": settings.ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "claude-3-5-sonnet-20241022",
                        "system": system_message,
                        "messages": claude_messages,
                        "max_tokens": max_tokens
                    }
                )
                response.raise_for_status()

                result = response.json()
                return result["content"][0]["text"]

        except Exception as e:
            print(f"Anthropic LLM Error: {e}")
            return f"[LLM error: {str(e)}]"
