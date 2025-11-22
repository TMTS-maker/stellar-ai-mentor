"""Stellecta LucidAI Backend - Agents API"""
from fastapi import APIRouter
from app.agents.personas import get_all_mentors

router = APIRouter()

@router.get("/")
async def list_agents():
    """List all mentor agents"""
    mentors = get_all_mentors()
    return {"mentors": [{"id": m.id, "name": m.name, "subject": m.subject} for m in mentors]}
