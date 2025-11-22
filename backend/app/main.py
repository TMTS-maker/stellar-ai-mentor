"""
Stellar AI Mentor - FastAPI Application

Gold-standard pedagogical AI mentoring platform with:
- 8 specialized AI mentors (Stella, Max, Nova, Darwin, Lexis, Neo, Luna, Atlas)
- Supervisor agent for intelligent routing
- Multi-LLM support (OpenAI, Anthropic, Gemini, LucidAI)
- LVO (Learn-Verify-Own) pedagogical framework
- H-PEM (History-Practice-Evaluation-Metacognition) integration
- Gamification (XP, achievements, levels)

See docs/agent-instruction-design.md for the pedagogical framework.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.chat import router as chat_router

# Create FastAPI app
app = FastAPI(
    title="Stellar AI Mentor API",
    description=(
        "Gold-standard pedagogical AI mentoring platform with research-backed teaching principles, "
        "Socratic communication patterns, and multi-LLM support."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Stellar AI Mentor API",
        "version": "0.1.0",
        "docs": "/docs",
        "features": {
            "mentors": 8,
            "pedagogical_framework": "LVO (Learn-Verify-Own)",
            "teaching_style": "Socratic (question-first, guided discovery)",
            "llm_providers": ["OpenAI", "Anthropic", "Gemini", "LucidAI"],
            "gamification": True,
            "multi_language": "Prepared (English default)"
        },
        "endpoints": {
            "get_mentors": "/api/chat/mentors",
            "get_mentor_details": "/api/chat/mentors/{mentor_id}",
            "send_message": "/api/chat/message",
            "send_to_mentor": "/api/chat/message/{mentor_id}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "features": {
            "lvo": settings.enable_lvo,
            "hpem": settings.enable_hpem,
            "gamification": settings.enable_gamification
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload
    )
