"""
Chat API endpoints.

Provides RESTful endpoints for interacting with AI mentors.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from ..agents.schemas import ChatRequest, ChatResponse, MentorPersona
from ..agents.personas import list_mentors, get_mentor_by_id
from ..agents.mentor_engine import get_mentor_engine
from ..agents.supervisor import get_supervisor_agent

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.get("/mentors", response_model=List[dict])
async def get_all_mentors():
    """
    Get a list of all available mentors.

    Returns:
        List of mentor information (id, name, subjects, age range, etc.)
    """
    mentors = list_mentors()
    return [
        {
            "id": mentor.id,
            "display_name": mentor.display_name,
            "emoji": mentor.emoji,
            "subjects": mentor.subjects,
            "age_range": f"{mentor.age_min}-{mentor.age_max}",
            "personality_traits": mentor.personality_traits,
            "voice_tone": mentor.voice_tone,
            "teaching_style": mentor.teaching_style.value,
            "description": mentor.description,
            "gradient": mentor.gradient
        }
        for mentor in mentors.values()
    ]


@router.get("/mentors/{mentor_id}", response_model=dict)
async def get_mentor(mentor_id: str):
    """
    Get detailed information about a specific mentor.

    Args:
        mentor_id: Mentor identifier

    Returns:
        Mentor details

    Raises:
        404: If mentor not found
    """
    mentor = get_mentor_by_id(mentor_id)
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor '{mentor_id}' not found"
        )

    return {
        "id": mentor.id,
        "display_name": mentor.display_name,
        "emoji": mentor.emoji,
        "subjects": mentor.subjects,
        "age_min": mentor.age_min,
        "age_max": mentor.age_max,
        "personality_traits": mentor.personality_traits,
        "voice_tone": mentor.voice_tone,
        "teaching_style": mentor.teaching_style.value,
        "lvo_strategies": {
            "learn": mentor.lvo_learn_strategy,
            "verify": mentor.lvo_verify_strategy,
            "own": mentor.lvo_own_strategy
        },
        "description": mentor.description,
        "languages": mentor.languages
    }


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message to a mentor or the supervisor.

    If mentor_id is specified, routes directly to that mentor.
    If mentor_id is None, uses the Supervisor to determine the best mentor.

    Args:
        request: Chat request with message and context

    Returns:
        Chat response from the mentor or supervisor

    Raises:
        400: If request is invalid
        404: If specified mentor not found
        500: If LLM communication fails
    """
    try:
        if request.mentor_id:
            # Direct mentor interaction
            mentor = get_mentor_by_id(request.mentor_id)
            if not mentor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Mentor '{request.mentor_id}' not found"
                )

            engine = get_mentor_engine()
            response = await engine.chat(
                mentor_id=request.mentor_id,
                message=request.message,
                student_context=request.student_context,
                conversation_history=request.conversation_history,
                provider=request.provider,
                temperature=request.temperature
            )
        else:
            # Supervisor routing
            supervisor = get_supervisor_agent()
            response = await supervisor.route(
                message=request.message,
                student_context=request.student_context,
                conversation_history=request.conversation_history,
                provider=request.provider
            )

        return response

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )


@router.post("/message/{mentor_id}", response_model=ChatResponse)
async def send_message_to_mentor(mentor_id: str, request: ChatRequest):
    """
    Send a message directly to a specific mentor (alternative endpoint).

    Args:
        mentor_id: ID of the mentor
        request: Chat request

    Returns:
        Chat response from the mentor
    """
    # Override mentor_id in request
    request.mentor_id = mentor_id
    return await send_message(request)
