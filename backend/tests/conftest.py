"""Pytest configuration and fixtures for Stellecta LucidAI Backend tests"""
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.main import app
from app.database.models.base import Base
from app.config import Settings, get_settings


# Test database URL (use in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Override settings for testing."""
    settings = Settings(
        app_name="Stellecta LucidAI Backend - Test",
        app_debug=True,
        database_url=TEST_DATABASE_URL,
        gemini_api_key="test-gemini-key",
        openai_api_key="test-openai-key",
        anthropic_api_key="test-anthropic-key",
        lucidai_api_url="http://test-lucidai",
        lucidai_api_key="test-lucidai-key",
        routing_mode="single",
        default_llm="gemini",
        enable_lucidai=False,
    )
    return settings


@pytest.fixture(scope="function")
def db_engine():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_settings) -> TestClient:
    """Create test client for FastAPI app."""
    # Override settings dependency
    app.dependency_overrides[get_settings] = lambda: test_settings
    return TestClient(app)


@pytest.fixture
def sample_llm_request():
    """Sample LLM request for testing."""
    from app.llm.schemas import LLMRequest
    return LLMRequest(
        system_prompt="You are a helpful math tutor.",
        user_message="What is 2 + 2?",
        temperature=0.7,
        max_tokens=500,
    )


@pytest.fixture
def sample_llm_response():
    """Sample LLM response for testing."""
    from app.llm.schemas import LLMResponse
    return LLMResponse(
        content="2 + 2 equals 4. This is a basic arithmetic operation.",
        llm_provider="gemini",
        model_version="gemini-1.5-pro",
        confidence_score=0.95,
        tokens_input=25,
        tokens_output=15,
        inference_time_ms=342,
        cost_usd=0.0001,
        metadata={}
    )


@pytest.fixture
def sample_student_context():
    """Sample student context for testing."""
    return {
        "student_id": "test-student-123",
        "age": 13,
        "grade_level": 7,
        "h_pem_proficiency": 0.65,
        "h_pem_resilience": 0.72,
        "weak_skills": ["fractions", "word_problems"],
        "achievements": ["completed_algebra_1"],
        "learning_style": "visual",
    }


@pytest.fixture
def sample_conversation_context():
    """Sample conversation context for testing."""
    return [
        {"role": "user", "content": "Hi, I need help with algebra."},
        {"role": "assistant", "content": "Hello! I'd be happy to help you with algebra. What specific topic are you working on?"},
        {"role": "user", "content": "Solving equations with variables on both sides."},
    ]


@pytest.fixture
def sample_routing_hints():
    """Sample routing hints for testing."""
    from app.llm.schemas import RoutingHints
    return RoutingHints(
        task_type="tutoring",
        risk_level="low",
        subject="mathematics",
        prefer_llm=None,
    )
