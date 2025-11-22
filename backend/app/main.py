"""
Stellecta LucidAI Backend - FastAPI Application

Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.config import settings
from app.api import chat, agents, admin

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer() if settings.log_format == "json" else structlog.dev.ConsoleRenderer()
    ]
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Stellecta LucidAI Multi-LLM Backend API",
    debug=settings.app_debug,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.on_event("startup")
async def startup():
    logger.info("Stellecta LucidAI Backend starting", env=settings.app_env)

@app.on_event("shutdown")
async def shutdown():
    logger.info("Stellecta LucidAI Backend shutting down")

@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": "0.1.0",
        "status": "running",
        "environment": settings.app_env,
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
