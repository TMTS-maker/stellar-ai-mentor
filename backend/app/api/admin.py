"""Stellecta LucidAI Backend - Admin API"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/llm-metrics")
async def get_llm_metrics():
    """Get LLM performance metrics - TODO: Connect to router"""
    return {"metrics": {}, "message": "Metrics pending integration"}
