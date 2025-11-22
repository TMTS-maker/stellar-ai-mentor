"""
Chat API Endpoints

Handles student-mentor conversations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import get_db, get_current_student
from app.database.models.user import Student
from app.services.supervisor_service import SupervisorService
from app.agents.mentors import list_mentors
from app.schemas.chat import (
    SendMessageRequest,
    SendMessageResponse,
    SessionResponse,
    SessionHistoryResponse,
    SessionMessagesResponse,
    MentorListResponse,
    MentorInfo,
)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/send", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student),
):
    """
    Send message to AI mentor

    The supervisor will:
    1. Detect subject from message (or use preferred mentor)
    2. Route to appropriate mentor agent
    3. Generate curriculum-aligned response
    4. Save conversation to database
    5. Award XP

    Returns the mentor's response along with gamification data
    """
    try:
        supervisor = SupervisorService(db)

        response = await supervisor.route_student_message(
            student_id=str(current_student.id),
            message=request.message,
            session_id=str(request.session_id) if request.session_id else None,
            preferred_mentor=request.mentor_id,
        )

        return SendMessageResponse(**response)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process message"
        )


@router.get("/sessions", response_model=SessionHistoryResponse)
async def get_sessions(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student),
):
    """
    Get student's recent conversation sessions

    Returns list of sessions ordered by most recent first
    """
    try:
        supervisor = SupervisorService(db)

        sessions = await supervisor.get_student_sessions(
            student_id=str(current_student.id), limit=limit
        )

        return SessionHistoryResponse(sessions=sessions, total_sessions=len(sessions))

    except Exception as e:
        print(f"Session fetch error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch sessions"
        )


@router.get("/sessions/{session_id}/messages", response_model=SessionMessagesResponse)
async def get_session_messages(
    session_id: str,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student),
):
    """
    Get all messages in a conversation session

    Returns complete message history for a session
    """
    try:
        supervisor = SupervisorService(db)

        messages = await supervisor.get_session_messages(
            session_id=session_id, student_id=str(current_student.id)
        )

        return SessionMessagesResponse(
            session_id=session_id, messages=messages, total_messages=len(messages)
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Message fetch error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch messages"
        )


@router.get("/mentors", response_model=MentorListResponse)
async def get_mentors():
    """
    Get list of all available AI mentors

    Returns information about all 8 mentor agents:
    - Stella (Math)
    - Max (Physics)
    - Nova (Chemistry)
    - Darwin (Biology)
    - Lexis (Language)
    - Neo (Technology)
    - Luna (Arts)
    - Atlas (History)
    """
    try:
        mentors = list_mentors()

        return MentorListResponse(
            mentors=[MentorInfo(**m) for m in mentors], total_mentors=len(mentors)
        )

    except Exception as e:
        print(f"Mentor list error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch mentors"
        )
