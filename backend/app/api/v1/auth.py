"""
Authentication API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.database.models.user import User
from app.services.auth_service import AuthService
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    PasswordChangeRequest,
    RegisterResponse,
    LoginResponse,
    Token,
    UserResponse,
    MessageResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user account

    - **email**: Valid email address
    - **password**: Minimum 8 characters
    - **user_type**: student, teacher, or parent
    - **Additional fields** required based on user type
    """
    auth_service = AuthService(db)
    result = await auth_service.register_user(request)
    return result


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and receive JWT access token

    Returns access token, refresh token, and user information
    """
    auth_service = AuthService(db)
    result = await auth_service.login(request)
    return result


@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Get new access token using refresh token

    Refresh tokens are long-lived and can be used to get new access tokens
    without requiring the user to log in again
    """
    auth_service = AuthService(db)
    result = await auth_service.refresh_access_token(request.refresh_token)
    return result


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get current authenticated user's profile information
    """
    auth_service = AuthService(db)
    profile = await auth_service.get_user_profile(current_user.id)
    return profile


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    request: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Change password for authenticated user
    """
    auth_service = AuthService(db)
    result = await auth_service.change_password(
        user_id=current_user.id,
        current_password=request.current_password,
        new_password=request.new_password,
    )
    return result


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user

    Note: Since we're using stateless JWT tokens, logout is handled client-side
    by removing the token. This endpoint is provided for API consistency.
    """
    return MessageResponse(
        message="Logged out successfully", detail="Please remove the token from client storage"
    )


@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    """
    Verify if the provided token is valid

    Returns 200 if valid, 401 if invalid
    """
    return {"valid": True, "user_id": str(current_user.id), "user_type": current_user.user_type}
