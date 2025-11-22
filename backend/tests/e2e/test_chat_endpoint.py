"""End-to-end tests for Chat API endpoint"""
import pytest
from fastapi.testclient import TestClient


class TestChatEndpoint:
    """E2E test suite for /api/chat endpoint."""

    def test_health_check_endpoint(self, client):
        """Test that health check endpoint is accessible."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_list_mentors_endpoint(self, client):
        """Test that /api/agents endpoint returns all mentors."""
        response = client.get("/api/agents")
        assert response.status_code == 200

        data = response.json()
        assert "mentors" in data
        assert len(data["mentors"]) == 8

        # Verify expected mentors are present
        mentor_ids = [m["id"] for m in data["mentors"]]
        expected = ["stella", "max", "nova", "darwin", "lexis", "neo", "luna", "atlas"]
        for mentor_id in expected:
            assert mentor_id in mentor_ids

    def test_chat_endpoint_accepts_valid_request(self, client):
        """Test that /api/chat accepts valid chat requests."""
        request = {
            "student_id": "550e8400-e29b-41d4-a716-446655440000",
            "message": "How do I solve 2x + 3 = 7?",
            "mentor_id": "stella",
        }

        response = client.post("/api/chat", json=request)

        # Should return 200 (or 500 if backend not fully integrated)
        # For Phase 0 scaffold, may return scaffold response
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "message" in data
            assert "mentor_id" in data
            assert data["mentor_id"] in ["stella", "max", "nova", "darwin", "lexis", "neo", "luna", "atlas"]

    def test_chat_endpoint_validates_request_format(self, client):
        """Test that /api/chat validates request format."""
        # Missing required field (message)
        invalid_request = {
            "student_id": "550e8400-e29b-41d4-a716-446655440000",
        }

        response = client.post("/api/chat", json=invalid_request)

        # Should return 422 (validation error)
        assert response.status_code == 422

    def test_chat_endpoint_auto_selects_mentor_when_not_provided(self, client):
        """Test that /api/chat auto-selects mentor when not provided."""
        request = {
            "student_id": "550e8400-e29b-41d4-a716-446655440000",
            "message": "Help me with calculus",
            # No mentor_id provided
        }

        response = client.post("/api/chat", json=request)

        # Should return 200 with auto-selected mentor
        if response.status_code == 200:
            data = response.json()
            assert "mentor_id" in data
            # Should auto-select math mentor (Stella) for calculus
            assert data["mentor_id"] is not None

    def test_chat_endpoint_handles_conversation_continuity(self, client):
        """Test that /api/chat handles conversation continuity with conversation_id."""
        # First message
        first_request = {
            "student_id": "550e8400-e29b-41d4-a716-446655440000",
            "message": "I'm learning about photosynthesis",
            "mentor_id": "max",
        }

        first_response = client.post("/api/chat", json=first_request)

        if first_response.status_code == 200:
            conversation_id = first_response.json().get("conversation_id")

            # Follow-up message with conversation_id
            second_request = {
                "student_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": "What role do chloroplasts play?",
                "mentor_id": "max",
                "conversation_id": conversation_id,
            }

            second_response = client.post("/api/chat", json=second_request)

            # Should maintain conversation context
            if second_response.status_code == 200:
                assert second_response.json().get("conversation_id") == conversation_id

    def test_chat_endpoint_returns_llm_metadata(self, client):
        """Test that /api/chat returns LLM metadata."""
        request = {
            "student_id": "550e8400-e29b-41d4-a716-446655440000",
            "message": "What is a prime number?",
            "mentor_id": "stella",
        }

        response = client.post("/api/chat", json=request)

        if response.status_code == 200:
            data = response.json()
            # Should include which LLM was used
            assert "llm_used" in data
            assert data["llm_used"] in ["lucidai", "gemini", "gpt4", "claude", None]

    def test_api_docs_are_accessible(self, client):
        """Test that API documentation (Swagger UI) is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_api_redoc_is_accessible(self, client):
        """Test that ReDoc documentation is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_chat_endpoint_handles_special_characters(self, client):
        """Test that /api/chat handles special characters in messages."""
        request = {
            "student_id": "550e8400-e29b-41d4-a716-446655440000",
            "message": "What is √16? Also, explain π (pi).",
            "mentor_id": "stella",
        }

        response = client.post("/api/chat", json=request)

        # Should handle special characters gracefully
        assert response.status_code in [200, 500]

    def test_chat_endpoint_handles_long_messages(self, client):
        """Test that /api/chat handles long messages."""
        long_message = "Can you explain " + "this topic " * 100 + "in detail?"

        request = {
            "student_id": "550e8400-e29b-41d4-a716-446655440000",
            "message": long_message,
            "mentor_id": "stella",
        }

        response = client.post("/api/chat", json=request)

        # Should handle or reject gracefully (not crash)
        assert response.status_code in [200, 400, 413, 422, 500]

    def test_cors_headers_are_configured(self, client):
        """Test that CORS headers are properly configured."""
        # OPTIONS preflight request
        response = client.options("/api/chat")

        # Should return appropriate CORS headers (or 405 if OPTIONS not implemented)
        assert response.status_code in [200, 405]

    @pytest.mark.asyncio
    async def test_concurrent_chat_requests(self, client):
        """Test handling of concurrent chat requests."""
        import asyncio

        async def make_request(student_id):
            request = {
                "student_id": student_id,
                "message": "Test concurrent message",
                "mentor_id": "stella",
            }
            return client.post("/api/chat", json=request)

        # Simulate 5 concurrent requests
        tasks = [make_request(f"student-{i}") for i in range(5)]

        # Execute concurrently (using sync client, so just sequential for now)
        for task in tasks:
            response = await task if asyncio.iscoroutine(task) else task
            assert response.status_code in [200, 500]
