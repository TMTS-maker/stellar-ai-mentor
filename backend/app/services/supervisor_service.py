"""
Supervisor Service

Orchestrates student-mentor interactions:
- Detects subject from student message
- Selects appropriate mentor
- Fetches curriculum context
- Routes to mentor agent
- Saves conversation to database
- Awards XP and updates gamification
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from app.database.models.user import Student
from app.database.models.conversation import ConversationSession, Message
from app.database.models.gamification import StudentXPLog
from app.agents.mentors import MENTOR_REGISTRY, get_mentor
from app.core.config import settings
from app.services.curriculum_service import CurriculumService


class SupervisorService:
    """
    Supervisor Service - Routes student messages to appropriate mentors
    """

    # Subject keywords for detection
    SUBJECT_KEYWORDS = {
        'MATH': ['math', 'calculate', 'equation', 'algebra', 'geometry', 'calculus', 'trigonometry', 'number', 'fraction', 'decimal'],
        'PHYSICS': ['physics', 'force', 'motion', 'energy', 'velocity', 'acceleration', 'momentum', 'gravity', 'wave'],
        'CHEMISTRY': ['chemistry', 'atom', 'molecule', 'reaction', 'element', 'compound', 'acid', 'base', 'chemical'],
        'BIOLOGY': ['biology', 'cell', 'organism', 'DNA', 'evolution', 'ecosystem', 'photosynthesis', 'genetics'],
        'LANGUAGE': ['write', 'essay', 'grammar', 'literature', 'poem', 'story', 'sentence', 'paragraph', 'writing'],
        'TECH': ['code', 'program', 'computer', 'algorithm', 'software', 'python', 'javascript', 'app', 'technology'],
        'ARTS': ['art', 'draw', 'paint', 'music', 'create', 'design', 'color', 'sketch', 'creative'],
        'HISTORY': ['history', 'historical', 'ancient', 'civilization', 'war', 'revolution', 'empire', 'culture', 'geography']
    }

    # Subject to mentor mapping
    SUBJECT_TO_MENTOR = {
        'MATH': 'stella',
        'PHYSICS': 'max',
        'CHEMISTRY': 'nova',
        'BIOLOGY': 'darwin',
        'LANGUAGE': 'lexis',
        'TECH': 'neo',
        'ARTS': 'luna',
        'HISTORY': 'atlas'
    }

    def __init__(self, db: Session):
        self.db = db

    async def route_student_message(
        self,
        student_id: str,
        message: str,
        session_id: Optional[str] = None,
        preferred_mentor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Route student message to appropriate mentor

        Args:
            student_id: Student UUID
            message: Student's message text
            session_id: Optional existing session ID
            preferred_mentor: Optional mentor override

        Returns:
            Dict containing mentor response and metadata
        """
        # 1. Load student
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Student not found: {student_id}")

        # 2. Detect subject (or use preferred mentor)
        if preferred_mentor:
            mentor_id = preferred_mentor
            subject = self._get_subject_for_mentor(mentor_id)
        else:
            subject = self.detect_subject(message)
            mentor_id = self.SUBJECT_TO_MENTOR.get(subject, 'stella')  # Default to Stella

        # 3. Get or create conversation session
        session = self._get_or_create_session(student_id, session_id, mentor_id, subject)

        # 4. Build context for mentor
        context = await self._build_context(student, subject)

        # 5. Get mentor and generate response
        mentor = get_mentor(mentor_id)
        response = await mentor.generate_response(message, context)

        # 6. Save user message to database
        user_message = Message(
            session_id=session.id,
            role='user',
            content=message,
            timestamp=datetime.utcnow()
        )
        self.db.add(user_message)

        # 7. Save assistant response to database
        assistant_message = Message(
            session_id=session.id,
            role='assistant',
            content=response['text'],
            mentor_id=response['mentor_id'],
            llm_provider=response.get('llm_provider'),
            tokens_used=response.get('tokens_used'),
            model_name=response.get('model_name'),
            objective_id=response.get('objective_id'),
            xp_earned=settings.XP_PER_MESSAGE,
            extra_metadata=response.get('metadata')
        )
        self.db.add(assistant_message)

        # 8. Update session
        session.message_count += 2  # User + Assistant
        session.total_xp_earned += settings.XP_PER_MESSAGE

        # 9. Award XP to student
        xp_earned = await self._award_xp(student, settings.XP_PER_MESSAGE, session.id)

        # 10. Commit all changes
        self.db.commit()

        # 11. Return response
        return {
            'text': response['text'],
            'mentor_id': mentor_id,
            'mentor_name': mentor.name,
            'session_id': str(session.id),
            'message_id': str(assistant_message.id),
            'xp_earned': xp_earned,
            'total_xp': student.total_xp,
            'current_level': student.current_level,
            'llm_provider': response.get('llm_provider'),
            'tokens_used': response.get('tokens_used')
        }

    def detect_subject(self, message: str) -> str:
        """
        Detect subject from message content

        Args:
            message: Student's message

        Returns:
            Subject code (MATH, PHYSICS, etc.)
        """
        message_lower = message.lower()
        scores = {subject: 0 for subject in self.SUBJECT_KEYWORDS.keys()}

        # Count keyword matches for each subject
        for subject, keywords in self.SUBJECT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    scores[subject] += 1

        # Return subject with highest score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)

        # Default to MATH if no matches
        return 'MATH'

    def _get_subject_for_mentor(self, mentor_id: str) -> str:
        """Get subject for a mentor ID"""
        reverse_map = {v: k for k, v in self.SUBJECT_TO_MENTOR.items()}
        return reverse_map.get(mentor_id, 'MATH')

    def _get_or_create_session(
        self,
        student_id: str,
        session_id: Optional[str],
        mentor_id: str,
        subject: str
    ) -> ConversationSession:
        """Get existing session or create new one"""

        if session_id:
            # Try to find existing session
            session = self.db.query(ConversationSession).filter(
                ConversationSession.id == session_id,
                ConversationSession.student_id == student_id,
                ConversationSession.is_active == True
            ).first()

            if session:
                return session

        # Create new session
        session = ConversationSession(
            student_id=student_id,
            mentor_id=mentor_id,
            subject=subject,
            is_active=True,
            message_count=0,
            total_xp_earned=0
        )
        self.db.add(session)
        self.db.flush()  # Get the ID
        return session

    async def _build_context(self, student: Student, subject: str) -> Dict[str, Any]:
        """
        Build context dictionary for mentor

        Args:
            student: Student model
            subject: Subject code

        Returns:
            Context dictionary
        """
        # Basic student context
        student_context = {
            'id': str(student.id),
            'grade': student.grade_level,
            'age': student.age,
            'h_pem_level': student.h_pem_level,
            'total_xp': student.total_xp,
            'current_level': student.current_level
        }

        # Enhanced curriculum context using CurriculumService
        curriculum_service = CurriculumService(self.db)
        curriculum_context = await curriculum_service.get_student_curriculum_context(
            student_id=str(student.id),
            subject=subject
        )

        return {
            'student': student_context,
            'curriculum': curriculum_context,
            'subject': subject
        }

    async def _award_xp(
        self,
        student: Student,
        xp_amount: int,
        session_id: uuid.UUID
    ) -> int:
        """
        Award XP to student and update level

        Args:
            student: Student model
            xp_amount: XP to award
            session_id: Session ID

        Returns:
            XP awarded
        """
        # Update student XP
        student.total_xp += xp_amount

        # Check for level up (100 XP per level)
        new_level = (student.total_xp // 100) + 1
        if new_level > student.current_level:
            student.current_level = new_level

        # Log XP transaction
        xp_log = StudentXPLog(
            student_id=student.id,
            xp_amount=xp_amount,
            source='message',
            description='Engaged with AI mentor',
            session_id=session_id
        )
        self.db.add(xp_log)

        return xp_amount

    async def get_student_sessions(
        self,
        student_id: str,
        limit: int = 10
    ) -> list:
        """
        Get recent conversation sessions for student

        Args:
            student_id: Student UUID
            limit: Number of sessions to return

        Returns:
            List of session dictionaries
        """
        sessions = self.db.query(ConversationSession).filter(
            ConversationSession.student_id == student_id
        ).order_by(
            ConversationSession.start_time.desc()
        ).limit(limit).all()

        return [
            {
                'id': str(session.id),
                'mentor_id': session.mentor_id,
                'subject': session.subject,
                'start_time': session.start_time.isoformat(),
                'message_count': session.message_count,
                'total_xp_earned': session.total_xp_earned,
                'is_active': session.is_active
            }
            for session in sessions
        ]

    async def get_session_messages(
        self,
        session_id: str,
        student_id: str
    ) -> list:
        """
        Get all messages in a conversation session

        Args:
            session_id: Session UUID
            student_id: Student UUID (for security)

        Returns:
            List of message dictionaries
        """
        session = self.db.query(ConversationSession).filter(
            ConversationSession.id == session_id,
            ConversationSession.student_id == student_id
        ).first()

        if not session:
            raise ValueError("Session not found or access denied")

        messages = self.db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(
            Message.timestamp.asc()
        ).all()

        return [
            {
                'id': str(msg.id),
                'role': msg.role,
                'content': msg.content,
                'mentor_id': msg.mentor_id,
                'timestamp': msg.timestamp.isoformat(),
                'xp_earned': msg.xp_earned
            }
            for msg in messages
        ]
