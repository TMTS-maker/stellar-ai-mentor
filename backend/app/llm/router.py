"""
Multi-LLM Router

Routes requests to different LLM providers (LucidAI, OpenAI, Anthropic)
based on availability, cost, and performance requirements
"""
from typing import Dict, Any, Optional
from enum import Enum
import httpx
from app.core.config import settings


class LLMProvider(str, Enum):
    """Available LLM providers"""
    LUCIDAI = "lucidai"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class MultiLLMRouter:
    """
    Routes LLM requests to appropriate provider

    Implements fallback logic and cost optimization
    """

    def __init__(self):
        self.default_provider = settings.DEFAULT_LLM_PROVIDER
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE

    async def route_and_generate(
        self,
        prompt: str,
        context: Dict[str, Any],
        routing_hints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route request to appropriate LLM and generate response

        Args:
            prompt: User message/prompt
            context: Context including system_prompt, student info
            routing_hints: Hints for routing decision (subject, complexity, etc.)

        Returns:
            Dict containing:
                - text: Generated response
                - provider: Which LLM was used
                - model: Specific model name
                - tokens_used: Token count
                - metadata: Additional info
        """
        # Determine which provider to use
        provider = self._select_provider(routing_hints)

        # Get system prompt from context
        system_prompt = context.get('system_prompt', '')

        # Generate response based on provider
        if provider == LLMProvider.LUCIDAI:
            response = await self._generate_lucidai(prompt, system_prompt, context)
        elif provider == LLMProvider.OPENAI:
            response = await self._generate_openai(prompt, system_prompt, context)
        elif provider == LLMProvider.ANTHROPIC:
            response = await self._generate_anthropic(prompt, system_prompt, context)
        else:
            # Fallback to simulated response for development
            response = await self._generate_fallback(prompt, system_prompt, context)

        response['provider'] = provider.value
        return response

    def _select_provider(self, routing_hints: Optional[Dict[str, Any]] = None) -> LLMProvider:
        """
        Select which LLM provider to use

        Args:
            routing_hints: Hints like subject, curriculum_aligned, complexity

        Returns:
            Selected LLM provider
        """
        if not routing_hints:
            return LLMProvider(self.default_provider)

        # Priority logic:
        # 1. Curriculum-aligned queries -> Use best model (Anthropic or OpenAI)
        # 2. Simple queries -> Use LucidAI (cost-effective)
        # 3. Complex reasoning -> Use OpenAI GPT-4

        if routing_hints.get('curriculum_aligned'):
            # For curriculum-aligned content, use Anthropic (best instruction following)
            if settings.ANTHROPIC_API_KEY:
                return LLMProvider.ANTHROPIC
            elif settings.OPENAI_API_KEY:
                return LLMProvider.OPENAI

        if routing_hints.get('complexity', 'low') == 'high':
            # For complex queries, prefer OpenAI GPT-4
            if settings.OPENAI_API_KEY:
                return LLMProvider.OPENAI

        # Default to LucidAI or configured default
        if settings.LUCIDAI_API_KEY:
            return LLMProvider.LUCIDAI

        return LLMProvider(self.default_provider)

    async def _generate_lucidai(
        self,
        prompt: str,
        system_prompt: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate response using LucidAI"""
        if not settings.LUCIDAI_API_KEY:
            return await self._generate_fallback(prompt, system_prompt, context)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.LUCIDAI_ENDPOINT}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.LUCIDAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "lucidai-v1",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature
                    },
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "text": data['choices'][0]['message']['content'],
                        "model": "lucidai-v1",
                        "tokens_used": data.get('usage', {}).get('total_tokens', 0),
                        "metadata": {"finish_reason": data['choices'][0].get('finish_reason')}
                    }
        except Exception as e:
            print(f"LucidAI error: {e}")
            return await self._generate_fallback(prompt, system_prompt, context)

    async def _generate_openai(
        self,
        prompt: str,
        system_prompt: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate response using OpenAI"""
        if not settings.OPENAI_API_KEY:
            return await self._generate_fallback(prompt, system_prompt, context)

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

            response = await client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            return {
                "text": response.choices[0].message.content,
                "model": response.model,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "metadata": {"finish_reason": response.choices[0].finish_reason}
            }
        except Exception as e:
            print(f"OpenAI error: {e}")
            return await self._generate_fallback(prompt, system_prompt, context)

    async def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate response using Anthropic Claude"""
        if not settings.ANTHROPIC_API_KEY:
            return await self._generate_fallback(prompt, system_prompt, context)

        try:
            from anthropic import AsyncAnthropic

            client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

            response = await client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "text": response.content[0].text,
                "model": response.model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "metadata": {"stop_reason": response.stop_reason}
            }
        except Exception as e:
            print(f"Anthropic error: {e}")
            return await self._generate_fallback(prompt, system_prompt, context)

    async def _generate_fallback(
        self,
        prompt: str,
        system_prompt: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback response for development/testing when APIs are unavailable

        Generates a simulated educational response
        """
        student_name = context.get('student', {}).get('name', 'there')

        fallback_response = f"""Hello {student_name}! I understand you're asking about: "{prompt[:50]}..."

I'm currently running in development mode without live LLM connections. In production, I would provide a detailed, personalized response based on your curriculum and learning level.

Here's what I would typically do:
1. Analyze your question in context of your current learning objectives
2. Provide a clear, step-by-step explanation
3. Offer examples and real-world applications
4. Check your understanding with follow-up questions
5. Award XP based on your engagement

To enable live AI responses, configure your LLM API keys in the environment settings.

How else can I help you today?"""

        return {
            "text": fallback_response,
            "model": "fallback-v1",
            "tokens_used": len(fallback_response.split()),
            "metadata": {"mode": "development_fallback"}
        }
