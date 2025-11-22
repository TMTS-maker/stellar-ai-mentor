"""
API v1 Router

Combines all API v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1 import auth

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(auth.router)

# Future routers will be added here:
# api_router.include_router(chat.router)
# api_router.include_router(curriculum.router)
# api_router.include_router(gamification.router)
# api_router.include_router(teacher.router)
# api_router.include_router(admin.router)
