"""
Stellecta API - Main Application Entry Point

AI-Powered Educational Platform with Multi-LLM Router and Curriculum Integration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Import routers
from app.api.v1.router import api_router

app = FastAPI(
    title="Stellecta API",
    description="AI-Powered Educational Platform with 8 Mentor Agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Stellecta API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print(f"Starting Stellecta API in {settings.ENVIRONMENT} mode...")
    # Database initialization will be added in Phase 2
    # Redis connection will be added in Phase 4

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down Stellecta API...")
    # Cleanup tasks will be added as needed
