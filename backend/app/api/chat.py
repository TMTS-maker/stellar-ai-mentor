"""Stellecta LucidAI Backend - Chat API"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    student_id: str
    message: str
    mentor_id: Optional[str] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    mentor_id: str
    conversation_id: str
    llm_used: Optional[str] = None

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - TODO: Connect to Supervisor Agent"""
    # TODO: Integrate with SupervisorAgent
    return ChatResponse(
        message="Hello! This is a scaffold response. Full integration pending.",
        mentor_id=request.mentor_id or "stella",
        conversation_id=request.conversation_id or "new",
        llm_used="gemini"
    )
