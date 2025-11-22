"""
Phase 4 Agent Logic Validation Tests

Tests agent functionality without requiring full database schema
Focus on core agent logic, routing, and response generation
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import pytest

# Import application components
from app.agents.mentors import (
    StellaMentor,
    MaxMentor,
    NovaMentor,
    DarwinMentor,
    LexisMentor,
    NeoMentor,
    LunaMentor,
    AtlasMentor,
    get_mentor,
    list_mentors,
    MENTOR_REGISTRY,
)
from app.agents.base_agent import BaseAgent
from app.llm.router import MultiLLMRouter, LLMProvider


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
        print("\n" + "=" * 70)
        if self.failed == 0:
            print(f"✅ ALL {self.total} TESTS PASSED!")
            print("=" * 70)
            print("\n🎉 Phase 4 Agent System Validated Successfully!")
            print("   All core functionality working correctly.")
        else:
            print(f"⚠️  {self.passed}/{self.total} TESTS PASSED, {self.failed} FAILED")
            print("=" * 70)
            if self.errors:
                print("\nFailures:")
                for test_name, error in self.errors:
                    print(f"   • {test_name}: {error}")
        return self.failed == 0


results = TestResults()


# ============================================================================
# Test 1: Mentor Registry & Infrastructure
# ============================================================================


def test_mentor_registry():
    """Test mentor registry and infrastructure"""
    print("\n🔍 Test 1: Mentor Registry & Infrastructure")

    try:
        # Test: Registry has all 8 mentors
        if len(MENTOR_REGISTRY) == 8:
            results.record_pass(f"Mentor registry complete (8 mentors)")
        else:
            results.record_fail("Registry size", f"Expected 8, got {len(MENTOR_REGISTRY)}")

        # Test: All expected mentors present
        expected_mentors = ["stella", "max", "nova", "darwin", "lexis", "neo", "luna", "atlas"]
        for mentor_id in expected_mentors:
            if mentor_id in MENTOR_REGISTRY:
                results.record_pass(f"Mentor '{mentor_id}' registered")
            else:
                results.record_fail(f"Mentor registration", f"'{mentor_id}' missing")

        # Test: list_mentors function
        mentor_list = list_mentors()
        if len(mentor_list) == 8:
            results.record_pass("list_mentors() returns all 8")
        else:
            results.record_fail("list_mentors()", f"Expected 8, got {len(mentor_list)}")

        # Test: get_mentor function
        stella = get_mentor("stella")
        if isinstance(stella, StellaMentor) and stella.agent_id == "stella":
            results.record_pass("get_mentor() instantiation")
        else:
            results.record_fail("get_mentor()", "Failed to instantiate")

        # Test: Invalid mentor raises error
        try:
            get_mentor("invalid_mentor")
            results.record_fail("Invalid mentor", "Should raise KeyError")
        except KeyError:
            results.record_pass("Invalid mentor handling (KeyError)")

    except Exception as e:
        results.record_fail("Mentor registry", str(e))


# ============================================================================
# Test 2: Individual Mentor Validation
# ============================================================================


@pytest.mark.asyncio
async def test_individual_mentors():
    """Test each of the 8 mentors"""
    print("\n🤖 Test 2: Individual Mentor Validation")

    test_context = {
        "student": {
            "id": "test-student",
            "grade": 10,
            "age": 15,
            "h_pem_level": 5.0,
            "total_xp": 200,
            "current_level": 3,
            "name": "Test Student",
        },
        "curriculum": {
            "curriculum_id": "test-curr-id",
            "curriculum_name": "Test Curriculum Grade 10",
            "current_objectives": [
                {
                    "id": "obj-123",
                    "objective_code": "MATH-10-ALG-001",
                    "objective_text": "Solve quadratic equations",
                }
            ],
        },
        "subject": "MATH",
    }

    mentor_tests = [
        ("stella", StellaMentor, "MATH", "How do I solve x^2 + 5x + 6 = 0?"),
        ("max", MaxMentor, "PHYSICS", "Explain Newton's first law"),
        ("nova", NovaMentor, "CHEMISTRY", "What happens when you mix an acid and a base?"),
        ("darwin", DarwinMentor, "BIOLOGY", "How does the heart pump blood?"),
        ("lexis", LexisMentor, "LANGUAGE", "How do I write a good thesis statement?"),
        ("neo", NeoMentor, "TECH", "What is a variable in programming?"),
        ("luna", LunaMentor, "ARTS", "How do I use perspective in drawing?"),
        ("atlas", AtlasMentor, "HISTORY", "What led to the fall of the Roman Empire?"),
    ]

    for mentor_id, MentorClass, subject, test_question in mentor_tests:
        try:
            # Instantiate mentor
            mentor = MentorClass()

            # Test: Correct initialization
            if mentor.agent_id == mentor_id and mentor.subject == subject:
                results.record_pass(f"{mentor.name}: Initialization")
            else:
                results.record_fail(f"{mentor.name}", "Initialization mismatch")

            # Test: System prompt generation
            system_prompt = mentor.build_system_prompt(test_context)
            if len(system_prompt) > 200:  # Reasonable prompt length
                results.record_pass(f"{mentor.name}: System prompt generation")
            else:
                results.record_fail(
                    f"{mentor.name}", f"System prompt too short ({len(system_prompt)} chars)"
                )

            # Test: Prompt contains key elements
            if mentor.name in system_prompt and "Grade" in system_prompt:
                results.record_pass(f"{mentor.name}: Prompt context integration")
            else:
                results.record_fail(f"{mentor.name}", "Prompt missing context")

            # Test: Response generation
            response = await mentor.generate_response(test_question, test_context)

            # Validate response structure
            required_fields = ["text", "mentor_id", "llm_provider", "model_name"]
            if all(field in response for field in required_fields):
                results.record_pass(f"{mentor.name}: Response structure")
            else:
                missing = [f for f in required_fields if f not in response]
                results.record_fail(f"{mentor.name}", f"Response missing: {missing}")

            # Validate response content
            if response["text"] and len(response["text"]) > 50:
                results.record_pass(f"{mentor.name}: Response content")
            else:
                results.record_fail(f"{mentor.name}", "Response content too short")

            # Validate mentor_id matches
            if response["mentor_id"] == mentor_id:
                results.record_pass(f"{mentor.name}: Mentor ID consistency")
            else:
                results.record_fail(f"{mentor.name}", "Mentor ID mismatch")

        except Exception as e:
            results.record_fail(f"{mentor.name} validation", str(e))


# ============================================================================
# Test 3: LLM Router
# ============================================================================


@pytest.mark.asyncio
async def test_llm_router():
    """Test Multi-LLM Router"""
    print("\n🔀 Test 3: Multi-LLM Router")

    try:
        router = MultiLLMRouter()

        # Test: Router initialization
        if router.default_provider and router.max_tokens > 0:
            results.record_pass("LLM Router initialization")
        else:
            results.record_fail("Router init", "Invalid configuration")

        # Test: Provider selection logic
        test_cases = [
            ({"curriculum_aligned": True}, "Curriculum-aligned routing"),
            ({"complexity": "high"}, "High complexity routing"),
            ({}, "Default routing"),
        ]

        for hints, description in test_cases:
            provider = router._select_provider(hints)
            if provider in LLMProvider.__members__.values():
                results.record_pass(f"Provider selection: {description}")
            else:
                results.record_fail(description, f"Invalid provider: {provider}")

        # Test: Fallback response generation
        test_context = {
            "student": {"name": "Test Student"},
            "system_prompt": "You are a helpful tutor.",
        }

        fallback_response = await router._generate_fallback(
            "What is 2+2?", "You are a math tutor.", test_context
        )

        if "text" in fallback_response and "model" in fallback_response:
            results.record_pass("Fallback response generation")
        else:
            results.record_fail("Fallback", "Missing response fields")

        if len(fallback_response["text"]) > 20:
            results.record_pass("Fallback content quality")
        else:
            results.record_fail("Fallback content", "Too short")

    except Exception as e:
        results.record_fail("LLM Router", str(e))


# ============================================================================
# Test 4: Subject Detection (from SupervisorService)
# ============================================================================


def test_subject_detection():
    """Test subject detection logic"""
    print("\n🎯 Test 4: Subject Detection Logic")

    from app.services.supervisor_service import SupervisorService

    # Create a mock DB (we won't use it for this test)
    class MockDB:
        pass

    supervisor = SupervisorService(MockDB())

    test_cases = [
        ("What is 2+2?", "MATH"),
        ("Solve this equation", "MATH"),
        ("Explain gravity", "PHYSICS"),
        ("What is momentum?", "PHYSICS"),
        ("What is H2O?", "CHEMISTRY"),
        ("Chemical reaction", "CHEMISTRY"),
        ("How does DNA work?", "BIOLOGY"),
        ("Photosynthesis process", "BIOLOGY"),
        ("Write an essay about", "LANGUAGE"),
        ("Grammar rules", "LANGUAGE"),
        ("How do I code in Python?", "TECH"),
        ("What is an algorithm?", "TECH"),
        ("How to draw perspective?", "ARTS"),
        ("Color theory", "ARTS"),
        ("Ancient civilizations", "HISTORY"),
        ("World War 2 causes", "HISTORY"),
    ]

    correct = 0
    for message, expected in test_cases:
        detected = supervisor.detect_subject(message)
        if detected == expected:
            correct += 1

    accuracy = (correct / len(test_cases)) * 100

    if accuracy == 100:
        results.record_pass(f"Subject detection (100% accuracy)")
    elif accuracy >= 80:
        results.record_pass(f"Subject detection ({accuracy:.1f}% accuracy - good)")
    else:
        results.record_fail("Subject detection", f"Only {accuracy:.1f}% accurate")


# ============================================================================
# Test 5: Agent Base Class Functionality
# ============================================================================


def test_base_agent():
    """Test BaseAgent functionality"""
    print("\n🏗️  Test 5: BaseAgent Functionality")

    try:
        # Get a mentor instance
        stella = StellaMentor()

        # Test: Context validation
        valid_context = {"student": {"grade": 10}, "curriculum": {"curriculum_name": "Test"}}

        if stella.validate_context(valid_context):
            results.record_pass("Context validation (valid)")
        else:
            results.record_fail("Context validation", "Valid context rejected")

        # Test: Invalid context detection
        try:
            stella.validate_context({})  # Missing required fields
            results.record_fail("Invalid context", "Should raise ValueError")
        except ValueError:
            results.record_pass("Context validation (invalid)")

        # Test: Get agent info
        info = stella.get_agent_info()
        if "agent_id" in info and "name" in info and "subject" in info:
            results.record_pass("Agent info retrieval")
        else:
            results.record_fail("Agent info", "Missing fields")

        # Test: Persona description
        persona = stella.get_persona_description()
        if len(persona) > 10 and stella.name in persona:
            results.record_pass("Persona description")
        else:
            results.record_fail("Persona", "Invalid description")

        # Test: Extract learning objective
        context_with_obj = {
            "student": {},
            "curriculum": {
                "current_objectives": [{"id": "obj-123", "objective_text": "Test objective"}]
            },
        }

        obj_id = stella.extract_learning_objective(context_with_obj)
        if obj_id == "obj-123":
            results.record_pass("Learning objective extraction")
        else:
            results.record_fail("Objective extraction", f"Expected 'obj-123', got {obj_id}")

    except Exception as e:
        results.record_fail("BaseAgent functionality", str(e))


# ============================================================================
# Main Test Runner
# ============================================================================


async def run_all_tests():
    """Run all validation tests"""
    print("=" * 70)
    print("🧪 PHASE 4 AGENT LOGIC VALIDATION")
    print("   Testing Agent System Core Functionality")
    print("=" * 70)

    # Run all test suites
    test_mentor_registry()
    await test_individual_mentors()
    await test_llm_router()
    test_subject_detection()
    test_base_agent()

    # Print summary
    success = results.summary()

    if success:
        print("\n📊 Validation Summary:")
        print("   • All 8 mentors functional")
        print("   • LLM routing working")
        print("   • Subject detection accurate")
        print("   • Base infrastructure solid")
        print("\n✨ Ready to proceed with:")
        print("   → Frontend chat interface")
        print("   → Curriculum integration")
        print("   → Full gamification system")
        return 0
    else:
        print("\n⚠️  Review and fix errors before proceeding")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
