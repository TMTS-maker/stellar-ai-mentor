"""AI conversation router"""
from typing import Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user, require_role
from app.db import get_db
from app.models.user import User
from app.models.student import Student
from app.models.task import Task
from app.models.conversation import ConversationSession, ConversationMessage, MessageSender
from app.services.ai.stt_service import STTService
from app.services.ai.llm_service import LLMService
from app.services.ai.tts_service import TTSService
from app.services.ai.avatar_service import AvatarService
from app.schemas.conversation import (
    TextConversationRequest, TextConversationResponse,
    VoiceConversationResponse
)

router = APIRouter(prefix="/ai", tags=["AI Conversation"])


@router.post("/conversation/text", response_model=TextConversationResponse)
async def text_conversation(
    request: TextConversationRequest,
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle text-based conversation with AI avatar.

    Flow:
    1. Get/create conversation session
    2. Store student message
    3. Call LLM service for response
    4. Store avatar response
    5. Return response + optional XP bonus
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

    # Get or create conversation session
    session = ConversationSession(
        student_id=student.id,
        task_id=request.task_id,
        avatar_type="stellar"
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

    # Get task context if task_id provided
    task_context = None
    if request.task_id:
        result = await db.execute(select(Task).where(Task.id == request.task_id))
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

    # Store avatar response
    avatar_message = ConversationMessage(
        session_id=session.id,
        sender=MessageSender.AVATAR,
        text=llm_response
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
        metadata={"from_voice": True}
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
        metadata={"avatar_video_url": avatar_video_url}
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
