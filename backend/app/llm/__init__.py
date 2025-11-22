"""
Multi-LLM Router - Vendor-agnostic LLM abstraction layer.
Supports OpenAI, Anthropic, Google Gemini, and LucidAI (stub).
"""
from .router import LLMRouter, get_llm_router

__all__ = ["LLMRouter", "get_llm_router"]
