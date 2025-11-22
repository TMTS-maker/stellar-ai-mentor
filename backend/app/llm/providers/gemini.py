"""Google Gemini provider implementation."""
from typing import List, Optional
import google.generativeai as genai
from .base import BaseLLMClient, Message, LLMResponse


class GeminiClient(BaseLLMClient):
    """Google Gemini LLM client implementation."""

    def __init__(self, api_key: str, default_model: str = "gemini-1.5-pro"):
        super().__init__(api_key, default_model)
        genai.configure(api_key=api_key)

    async def complete(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Google Gemini API."""
        model_name = model or self.default_model
        gemini_model = genai.GenerativeModel(model_name)

        # Convert messages to Gemini format
        # Gemini uses a different conversation format
        system_instruction = None
        conversation = []

        for msg in messages:
            if msg.role == "system":
                system_instruction = msg.content
            elif msg.role == "user":
                conversation.append({"role": "user", "parts": [msg.content]})
            elif msg.role == "assistant":
                conversation.append({"role": "model", "parts": [msg.content]})

        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        # For now, concatenate system with first user message
        if system_instruction and conversation:
            conversation[0]["parts"][0] = f"{system_instruction}\n\n{conversation[0]['parts'][0]}"

        # Generate response
        response = await gemini_model.generate_content_async(
            conversation,
            generation_config=generation_config
        )

        return LLMResponse(
            content=response.text,
            model=model_name,
            provider="gemini",
            metadata={"finish_reason": response.candidates[0].finish_reason.name if response.candidates else None}
        )

    async def stream_complete(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """Stream completion from Gemini."""
        model_name = model or self.default_model
        gemini_model = genai.GenerativeModel(model_name)

        # Convert messages
        system_instruction = None
        conversation = []

        for msg in messages:
            if msg.role == "system":
                system_instruction = msg.content
            elif msg.role == "user":
                conversation.append({"role": "user", "parts": [msg.content]})
            elif msg.role == "assistant":
                conversation.append({"role": "model", "parts": [msg.content]})

        if system_instruction and conversation:
            conversation[0]["parts"][0] = f"{system_instruction}\n\n{conversation[0]['parts'][0]}"

        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        response = await gemini_model.generate_content_async(
            conversation,
            generation_config=generation_config,
            stream=True
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text
