"""
Phase 4 Validation Tests - Agent System & Chat

Comprehensive tests for:
- Agent routing and subject detection
- All 8 mentor agents
- Database persistence
- XP awarding
- Session management
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Import application components
from app.database.base import Base
from app.database.models.user import User, Student
from app.database.models.conversation import ConversationSession, Message
from app.database.models.gamification import StudentXPLog
from app.agents.mentors import (
    StellaMentor, MaxMentor, NovaMentor, DarwinMentor,
    LexisMentor, NeoMentor, LunaMentor, AtlasMentor,
    get_mentor, list_mentors, MENTOR_REGISTRY
)
from app.services.supervisor_service import SupervisorService


# Test configuration
TEST_DB_URL = "sqlite:///:memory:"  # In-memory database for testing

# Create test database engine
engine = create_engine(TEST_DB_URL, echo=False)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


class TestResults:
    """Track test results"""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []

    def record_pass(self, test_name):
        self.total += 1
        self.passed += 1
        print(f"  ✅ {test_name}")

    def record_fail(self, test_name, error):
        self.total += 1
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"  ❌ {test_name}: {error}")

    def summary(self):
        print("\n" + "="*70)
        if self.failed == 0:
            print(f"✅ ALL {self.total} TESTS PASSED!")
        else:
            print(f"⚠️  {self.passed}/{self.total} TESTS PASSED")
            print(f"   {self.failed} FAILED")
        print("="*70)
        return self.failed == 0


results = TestResults()


# ============================================================================
# Test 1: Agent Infrastructure
# ============================================================================

def test_agent_infrastructure():
    """Test base agent infrastructure"""
    print("\n🔍 Test 1: Agent Infrastructure")

    try:
        # Test mentor registry
        if len(MENTOR_REGISTRY) == 8:
            results.record_pass("Mentor registry has all 8 mentors")
        else:
            results.record_fail("Mentor registry", f"Expected 8 mentors, got {len(MENTOR_REGISTRY)}")

        # Test list_mentors function
        mentors = list_mentors()
        if len(mentors) == 8:
            results.record_pass("list_mentors() returns all 8 mentors")
        else:
            results.record_fail("list_mentors()", f"Expected 8, got {len(mentors)}")

        # Test get_mentor function
        stella = get_mentor('stella')
        if stella.agent_id == 'stella' and stella.name == 'Stella':
            results.record_pass("get_mentor() works correctly")
        else:
            results.record_fail("get_mentor()", "Stella not loaded correctly")

        # Test invalid mentor
        try:
            get_mentor('invalid')
            results.record_fail("Invalid mentor handling", "Should raise KeyError")
        except KeyError:
            results.record_pass("Invalid mentor raises KeyError")

    except Exception as e:
        results.record_fail("Agent infrastructure", str(e))


# ============================================================================
# Test 2: Individual Mentor Agents
# ============================================================================

async def test_all_mentors():
    """Test all 8 mentor agents"""
    print("\n🤖 Test 2: Individual Mentor Agents")

    test_context = {
        'student': {
            'id': 'test-student-id',
            'grade': 10,
            'age': 15,
            'h_pem_level': 5.0,
            'total_xp': 150,
            'current_level': 2
        },
        'curriculum': {
            'curriculum_id': 'test-curriculum',
            'curriculum_name': 'Test Curriculum',
            'current_objectives': [
                {
                    'id': 'obj-1',
                    'objective_code': 'TEST-001',
                    'objective_text': 'Test objective'
                }
            ]
        },
        'subject': 'MATH'
    }

    mentor_tests = [
        ('stella', 'What is 2+2?', 'MATH'),
        ('max', 'Explain gravity', 'PHYSICS'),
        ('nova', 'What is H2O?', 'CHEMISTRY'),
        ('darwin', 'How does photosynthesis work?', 'BIOLOGY'),
        ('lexis', 'Help me write an essay', 'LANGUAGE'),
        ('neo', 'What is Python?', 'TECH'),
        ('luna', 'How do I draw?', 'ARTS'),
        ('atlas', 'Tell me about ancient Rome', 'HISTORY')
    ]

    for mentor_id, test_message, subject in mentor_tests:
        try:
            mentor = get_mentor(mentor_id)

            # Test system prompt building
            system_prompt = mentor.build_system_prompt(test_context)
            if len(system_prompt) > 100:
                results.record_pass(f"{mentor.name}: System prompt generation")
            else:
                results.record_fail(f"{mentor.name}: System prompt", "Too short")

            # Test response generation
            response = await mentor.generate_response(test_message, test_context)

            # Validate response structure
            if 'text' in response and 'mentor_id' in response:
                results.record_pass(f"{mentor.name}: Response structure")
            else:
                results.record_fail(f"{mentor.name}: Response structure", "Missing fields")

            # Validate response content
            if len(response['text']) > 10:
                results.record_pass(f"{mentor.name}: Response content")
            else:
                results.record_fail(f"{mentor.name}: Response content", "Too short")

        except Exception as e:
            results.record_fail(f"{mentor.name} agent", str(e))


# ============================================================================
# Test 3: Subject Detection
# ============================================================================

def test_subject_detection():
    """Test SupervisorService subject detection"""
    print("\n🎯 Test 3: Subject Detection")

    db = SessionLocal()
    supervisor = SupervisorService(db)

    test_cases = [
        ("What is 2+2?", "MATH"),
        ("Calculate the area", "MATH"),
        ("Explain gravity", "PHYSICS"),
        ("What is momentum?", "PHYSICS"),
        ("What is H2O?", "CHEMISTRY"),
        ("Explain atoms", "CHEMISTRY"),
        ("How does DNA work?", "BIOLOGY"),
        ("What is photosynthesis?", "BIOLOGY"),
        ("Help me write an essay", "LANGUAGE"),
        ("What is a metaphor?", "LANGUAGE"),
        ("How do I code?", "TECH"),
        ("What is Python programming?", "TECH"),
        ("How do I draw?", "ARTS"),
        ("What is perspective in art?", "ARTS"),
        ("Tell me about ancient Rome", "HISTORY"),
        ("What caused World War 2?", "HISTORY"),
    ]

    correct = 0
    for message, expected_subject in test_cases:
        detected = supervisor.detect_subject(message)
        if detected == expected_subject:
            correct += 1

    if correct == len(test_cases):
        results.record_pass(f"Subject detection ({correct}/{len(test_cases)} correct)")
    elif correct >= len(test_cases) * 0.8:  # 80% accuracy threshold
        results.record_pass(f"Subject detection ({correct}/{len(test_cases)} correct - good)")
    else:
        results.record_fail("Subject detection", f"Only {correct}/{len(test_cases)} correct")

    db.close()


# ============================================================================
# Test 4: Database Persistence
# ============================================================================

async def test_database_persistence():
    """Test conversation and state persistence"""
    print("\n💾 Test 4: Database Persistence")

    db = SessionLocal()

    try:
        # Create test user and student
        user = User(
            email="test@example.com",
            hashed_password="test",
            full_name="Test Student",
            user_type="student"
        )
        db.add(user)
        db.flush()

        student = Student(
            id=user.id,
            grade_level=10,
            age=15,
            total_xp=0,
            current_level=1,
            h_pem_level=0.0
        )
        db.add(student)
        db.commit()
        results.record_pass("User and Student creation")

        # Test supervisor service
        supervisor = SupervisorService(db)

        # Send first message
        response1 = await supervisor.route_student_message(
            student_id=str(student.id),
            message="What is 2+2?",
            preferred_mentor="stella"
        )
        results.record_pass("First message processed")

        # Verify session created
        sessions = db.query(ConversationSession).filter(
            ConversationSession.student_id == student.id
        ).all()
        if len(sessions) == 1:
            results.record_pass("Conversation session created")
        else:
            results.record_fail("Session creation", f"Expected 1 session, got {len(sessions)}")

        session = sessions[0]

        # Verify messages saved
        messages = db.query(Message).filter(
            Message.session_id == session.id
        ).all()
        if len(messages) == 2:  # User + Assistant
            results.record_pass("Messages persisted (user + assistant)")
        else:
            results.record_fail("Message persistence", f"Expected 2 messages, got {len(messages)}")

        # Send second message in same session
        response2 = await supervisor.route_student_message(
            student_id=str(student.id),
            message="What about 3+3?",
            session_id=response1['session_id']
        )

        # Verify session reused
        sessions = db.query(ConversationSession).filter(
            ConversationSession.student_id == student.id
        ).all()
        if len(sessions) == 1:
            results.record_pass("Session reused (not duplicated)")
        else:
            results.record_fail("Session reuse", f"Expected 1 session, got {len(sessions)}")

        # Verify message count updated
        db.refresh(session)
        if session.message_count == 4:  # 2 user + 2 assistant
            results.record_pass("Session message count updated")
        else:
            results.record_fail("Message count", f"Expected 4, got {session.message_count}")

    except Exception as e:
        results.record_fail("Database persistence", str(e))
    finally:
        db.close()


# ============================================================================
# Test 5: XP Awarding
# ============================================================================

async def test_xp_awarding():
    """Test XP and level awarding mechanisms"""
    print("\n⭐ Test 5: XP Awarding & Leveling")

    db = SessionLocal()

    try:
        # Create test student
        user = User(
            email="xp_test@example.com",
            hashed_password="test",
            full_name="XP Test Student",
            user_type="student"
        )
        db.add(user)
        db.flush()

        student = Student(
            id=user.id,
            grade_level=10,
            total_xp=0,
            current_level=1,
            h_pem_level=0.0
        )
        db.add(student)
        db.commit()

        supervisor = SupervisorService(db)

        # Send message to earn XP
        initial_xp = student.total_xp
        initial_level = student.current_level

        response = await supervisor.route_student_message(
            student_id=str(student.id),
            message="Test message",
            preferred_mentor="stella"
        )

        # Refresh student to get updated values
        db.refresh(student)

        # Verify XP awarded
        xp_gained = student.total_xp - initial_xp
        if xp_gained == 10:  # settings.XP_PER_MESSAGE
            results.record_pass(f"XP awarded correctly (10 XP)")
        else:
            results.record_fail("XP awarding", f"Expected 10 XP, got {xp_gained}")

        # Verify XP log created
        xp_logs = db.query(StudentXPLog).filter(
            StudentXPLog.student_id == student.id
        ).all()
        if len(xp_logs) == 1:
            results.record_pass("XP transaction logged")
        else:
            results.record_fail("XP logging", f"Expected 1 log, got {len(xp_logs)}")

        # Test level-up (send 10 messages to level up)
        for i in range(10):
            await supervisor.route_student_message(
                student_id=str(student.id),
                message=f"Message {i}",
                preferred_mentor="stella"
            )

        db.refresh(student)

        # After 11 total messages (110 XP), should be level 2
        expected_level = (student.total_xp // 100) + 1
        if student.current_level == expected_level:
            results.record_pass(f"Level calculation correct (Level {student.current_level})")
        else:
            results.record_fail("Level calculation", f"Expected {expected_level}, got {student.current_level}")

    except Exception as e:
        results.record_fail("XP awarding", str(e))
    finally:
        db.close()


# ============================================================================
# Test 6: Session Management
# ============================================================================

async def test_session_management():
    """Test session retrieval and management"""
    print("\n📝 Test 6: Session Management")

    db = SessionLocal()

    try:
        # Create test student
        user = User(
            email="session_test@example.com",
            hashed_password="test",
            full_name="Session Test",
            user_type="student"
        )
        db.add(user)
        db.flush()

        student = Student(
            id=user.id,
            grade_level=10,
            total_xp=0,
            current_level=1
        )
        db.add(student)
        db.commit()

        supervisor = SupervisorService(db)

        # Create multiple sessions
        session1 = await supervisor.route_student_message(
            student_id=str(student.id),
            message="Math question",
            preferred_mentor="stella"
        )

        session2 = await supervisor.route_student_message(
            student_id=str(student.id),
            message="Physics question",
            preferred_mentor="max"
        )

        # Test get_student_sessions
        sessions = await supervisor.get_student_sessions(str(student.id))
        if len(sessions) == 2:
            results.record_pass("Session history retrieval")
        else:
            results.record_fail("Session history", f"Expected 2 sessions, got {len(sessions)}")

        # Test get_session_messages
        messages = await supervisor.get_session_messages(
            session_id=session1['session_id'],
            student_id=str(student.id)
        )
        if len(messages) >= 2:  # At least user + assistant
            results.record_pass("Session messages retrieval")
        else:
            results.record_fail("Session messages", f"Expected >=2 messages, got {len(messages)}")

    except Exception as e:
        results.record_fail("Session management", str(e))
    finally:
        db.close()


# ============================================================================
# Main Test Runner
# ============================================================================

async def run_all_tests():
    """Run all validation tests"""
    print("="*70)
    print("🧪 PHASE 4 VALIDATION TEST SUITE")
    print("   Agent System & Chat Implementation")
    print("="*70)

    # Run all tests
    test_agent_infrastructure()
    await test_all_mentors()
    test_subject_detection()
    await test_database_persistence()
    await test_xp_awarding()
    await test_session_management()

    # Print summary
    success = results.summary()

    if success:
        print("\n✨ Phase 4 validation complete - Ready for production!")
        print("   All agent systems functioning correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed - Review errors above")
        for test_name, error in results.errors:
            print(f"   • {test_name}: {error}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
