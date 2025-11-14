"""AI conversation router"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user, require_role
from app.db import get_db
from app.models.user import User
from app.models.student import Student
from app.models.task import Task
from app.models.conversation import ConversationSession, ConversationMessage, MessageSender
from app.models.skill import SkillScore
from app.models.gamification import XPEvent
from app.services.ai.stt_service import STTService
from app.services.ai.llm_service import LLMService
from app.services.ai.tts_service import TTSService
from app.services.ai.avatar_service import AvatarService
from app.services.ai.mentor_engine import MentorEngine, MentorMode, MentorPersona
from app.schemas.conversation import (
    TextConversationRequest, TextConversationResponse,
    VoiceConversationResponse
)
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI Conversation"])


# Schema for mentor info response
class MentorInfo(BaseModel):
    """Mentor avatar information"""
    id: str
    display_name: str
    emoji: str
    short_description: str
    age_min: int
    age_max: int
    subjects: List[str]
    teaching_style: str
    tone: str

    class Config:
        from_attributes = True


@router.get("/mentors", response_model=List[MentorInfo])
async def get_mentors(current_user: User = Depends(get_current_user)):
    """
    Get list of available mentor avatars.

    Returns information about all 8 mentor personas to help students
    choose who they'd like to learn with.
    """
    mentors = MentorEngine.get_all_mentors()

    return [
        MentorInfo(
            id=m.id,
            display_name=m.display_name,
            emoji=m.emoji,
            short_description=m.short_description,
            age_min=m.age_min,
            age_max=m.age_max,
            subjects=m.subjects,
            teaching_style=m.teaching_style.value,
            tone=m.tone
        )
        for m in mentors
    ]


@router.post("/conversation/text", response_model=TextConversationResponse)
async def text_conversation(
    request: TextConversationRequest,
    mentor_id: Optional[str] = Query(None, description="Specific mentor to use (optional)"),
    mode: Optional[str] = Query(None, description="Conversation mode: explain, quiz, motivate, etc."),
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle text-based conversation with AI avatar mentor.

    Flow:
    1. Get student profile and LVO context
    2. Select appropriate mentor (or use specified mentor_id)
    3. Build enriched system prompt with student context
    4. Get/create conversation session
    5. Store student message
    6. Call LLM service with mentor persona
    7. Store avatar response
    8. Return response + optional XP bonus
    """
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    # Load LVO context for mentor
    # Get total XP
    xp_result = await db.execute(
        select(func.sum(XPEvent.xp_amount)).where(XPEvent.student_id == student.id)
    )
    total_xp = xp_result.scalar() or 0

    # Get weak skills (score < 60)
    weak_skills_result = await db.execute(
        select(SkillScore)
        .where(SkillScore.student_id == student.id)
        .where(SkillScore.score < 60)
        .order_by(SkillScore.score.asc())
        .limit(3)
    )
    weak_skills = weak_skills_result.scalars().all()

    # Get task context if task_id provided
    task_context = None
    task_subject = None
    if request.task_id:
        result = await db.execute(select(Task).where(Task.id == request.task_id))
        task = result.scalar_one_or_none()
        if task:
            task_context = f"Task: {task.title}. {task.description}"
            # Try to infer subject from task metadata or subject relationship
            if task.subject:
                task_subject = task.subject.name

    # Select mentor persona
    if mentor_id:
        # Use specified mentor
        persona = MentorEngine.get_persona_by_id(mentor_id)
        if not persona:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid mentor_id: {mentor_id}"
            )
    else:
        # Intelligent mentor suggestion based on context
        persona = MentorEngine.suggest_persona_for_student(
            student=student,
            subject=task_subject,
            weak_skills=weak_skills,
            student_age=None  # Could calculate from student.birthdate if available
        )

    # Build student context for mentor
    student_context = {
        "name": current_user.full_name,
        "grade": student.grade_level or "Unknown",
    }

    # Build LVO context
    lvo_context = {
        "xp": total_xp,
        "level": min(total_xp // 1000, 10),  # Simplified level calculation
        "weak_skills": [{"name": f"Skill ID: {ws.skill_id}", "score": ws.score} for ws in weak_skills],
    }

    # Build enriched system prompt using MentorEngine
    system_prompt = MentorEngine.build_system_prompt(
        persona=persona,
        student_context=student_context,
        lvo_context=lvo_context
    )

    # Get or create conversation session
    session = ConversationSession(
        student_id=student.id,
        task_id=request.task_id,
        avatar_type=persona.id  # Store which mentor is being used
    )
    db.add(session)
    await db.flush()

    # Store student message
    student_message = ConversationMessage(
        session_id=session.id,
        sender=MessageSender.STUDENT,
        text=request.message
    )
    db.add(student_message)

    # Build conversation history
    result = await db.execute(
        select(ConversationMessage)
        .where(ConversationMessage.session_id == session.id)
        .order_by(ConversationMessage.timestamp)
    )
    all_messages = result.scalars().all()

    conversation_history = []
    for msg in all_messages:
        role = "user" if msg.sender == MessageSender.STUDENT else "assistant"
        conversation_history.append({"role": role, "content": msg.text})

    # Generate LLM response with mentor persona
    # Add system prompt as first message
    messages_with_system = [{"role": "system", "content": system_prompt}] + conversation_history

    llm_response = await LLMService.generate_response(
        messages=messages_with_system,
        student_name=current_user.full_name,
        task_context=task_context
    )

    # Store avatar response
    avatar_message = ConversationMessage(
        session_id=session.id,
        sender=MessageSender.AVATAR,
        text=llm_response,
        message_metadata={"mentor_id": persona.id, "mode": mode}
    )
    db.add(avatar_message)

    await db.commit()

    # Optional: Award XP for engagement
    xp_bonus = 5  # Small XP for each conversation turn

    return TextConversationResponse(
        reply=llm_response,
        xp_bonus=xp_bonus,
        session_id=session.id
    )


@router.post("/conversation/voice", response_model=VoiceConversationResponse)
async def voice_conversation(
    audio: UploadFile = File(...),
    task_id: Optional[str] = Form(None),
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle voice-based conversation with AI avatar.

    Flow:
    1. Transcribe audio (STT)
    2. Process as text conversation
    3. Generate TTS audio
    4. Generate avatar video (optional)
    5. Return complete response
    """
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    # Read audio file
    audio_data = await audio.read()

    # Transcribe audio
    transcription = await STTService.transcribe_audio(audio_data, audio.filename)

    # Get or create conversation session
    task_uuid = UUID(task_id) if task_id else None
    session = ConversationSession(
        student_id=student.id,
        task_id=task_uuid,
        avatar_type="stellar"
    )
    db.add(session)
    await db.flush()

    # Store student message
    student_message = ConversationMessage(
        session_id=session.id,
        sender=MessageSender.STUDENT,
        text=transcription,
        message_metadata={"from_voice": True}
    )
    db.add(student_message)

    # Get task context
    task_context = None
    if task_uuid:
        result = await db.execute(select(Task).where(Task.id == task_uuid))
        task = result.scalar_one_or_none()
        if task:
            task_context = f"Task: {task.title}. {task.description}"

    # Build conversation history
    result = await db.execute(
        select(ConversationMessage)
        .where(ConversationMessage.session_id == session.id)
        .order_by(ConversationMessage.timestamp)
    )
    all_messages = result.scalars().all()

    conversation_history = []
    for msg in all_messages:
        role = "user" if msg.sender == MessageSender.STUDENT else "assistant"
        conversation_history.append({"role": role, "content": msg.text})

    # Generate LLM response
    llm_response = await LLMService.generate_response(
        messages=conversation_history,
        student_name=current_user.full_name,
        task_context=task_context
    )

    # Generate TTS audio
    audio_url = await TTSService.synthesize_speech(llm_response)

    # Generate avatar video (optional for MVP)
    avatar_video_url = await AvatarService.generate_avatar_video(
        script_text=llm_response,
        audio_url=audio_url
    )

    # Store avatar response
    avatar_message = ConversationMessage(
        session_id=session.id,
        sender=MessageSender.AVATAR,
        text=llm_response,
        audio_url=audio_url,
        message_metadata={"avatar_video_url": avatar_video_url}
    )
    db.add(avatar_message)

    await db.commit()

    # Award XP for voice engagement
    xp_bonus = 10  # More XP for voice interaction

    return VoiceConversationResponse(
        transcription=transcription,
        reply=llm_response,
        audio_url=audio_url,
        avatar_video_url=avatar_video_url,
        xp_bonus=xp_bonus,
        session_id=session.id
    )


@router.post("/conversation/{session_id}/end")
async def end_conversation(
    session_id: UUID,
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """End a conversation session"""
    result = await db.execute(
        select(ConversationSession).where(ConversationSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    session.ended_at = datetime.utcnow()
    await db.commit()

    return {"status": "ended", "session_id": str(session_id)}
