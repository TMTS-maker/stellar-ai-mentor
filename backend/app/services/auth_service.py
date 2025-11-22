"""
Authentication Service

Business logic for user authentication, registration, and management
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
import uuid

from app.database.models.user import User, Student, Teacher, Parent
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
from app.core.config import settings
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    Token,
    LoginResponse,
    UserResponse,
    StudentResponse,
    TeacherResponse,
)


class AuthService:
    """Service for authentication operations"""

    def __init__(self, db: Session):
        self.db = db

    async def register_user(self, request: RegisterRequest) -> dict:
        """
        Register a new user

        Args:
            request: Registration request data

        Returns:
            dict: Registration result with user_id

        Raises:
            HTTPException: 400 if email already exists
        """
        # Check if email already exists
        existing_user = self.db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
            )

        # Hash password
        hashed_password = get_password_hash(request.password)

        # Create base user
        user = User(
            email=request.email,
            hashed_password=hashed_password,
            full_name=request.full_name,
            user_type=request.user_type,
            is_active=True,
            is_verified=False,
        )

        self.db.add(user)
        self.db.flush()  # Get the user ID

        # Create role-specific profile
        if request.user_type == "student":
            student = Student(
                id=user.id,
                school_id=request.school_id,
                grade_level=request.grade_level,
                age=request.age,
                curriculum_id=request.curriculum_id,
                total_xp=0,
                current_level=1,
                h_pem_level=0.0,
            )
            self.db.add(student)

        elif request.user_type == "teacher":
            teacher = Teacher(
                id=user.id,
                school_id=request.school_id,
                subjects=request.subjects or [],
                grade_levels=request.grade_levels or [],
            )
            self.db.add(teacher)

        elif request.user_type == "parent":
            parent = Parent(id=user.id)
            self.db.add(parent)

        self.db.commit()
        self.db.refresh(user)

        return {
            "message": "User registered successfully",
            "user_id": str(user.id),
            "email": user.email,
        }

    async def login(self, request: LoginRequest) -> LoginResponse:
        """
        Authenticate user and generate tokens

        Args:
            request: Login credentials

        Returns:
            LoginResponse: Access token and user info

        Raises:
            HTTPException: 401 if credentials are invalid
        """
        # Find user by email
        user = self.db.query(User).filter(User.email == request.email).first()

        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User account is inactive"
            )

        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id), "user_type": user.user_type})

        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "user_type": user.user_type}
        )

        # Prepare user response
        user_response = UserResponse.from_orm(user)

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user_response,
        )

    async def get_user_profile(self, user_id: uuid.UUID) -> dict:
        """
        Get detailed user profile based on user type

        Args:
            user_id: User UUID

        Returns:
            dict: User profile data

        Raises:
            HTTPException: 404 if user not found
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user.user_type == "student":
            student = self.db.query(Student).filter(Student.id == user_id).first()
            if student:
                # Merge user and student data
                return {
                    **UserResponse.from_orm(user).dict(),
                    **StudentResponse.from_orm(student).dict(),
                }

        elif user.user_type == "teacher":
            teacher = self.db.query(Teacher).filter(Teacher.id == user_id).first()
            if teacher:
                return {
                    **UserResponse.from_orm(user).dict(),
                    **TeacherResponse.from_orm(teacher).dict(),
                }

        return UserResponse.from_orm(user).dict()

    async def change_password(
        self, user_id: uuid.UUID, current_password: str, new_password: str
    ) -> dict:
        """
        Change user password

        Args:
            user_id: User UUID
            current_password: Current password
            new_password: New password

        Returns:
            dict: Success message

        Raises:
            HTTPException: 400 if current password is incorrect
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect"
            )

        user.hashed_password = get_password_hash(new_password)
        self.db.commit()

        return {"message": "Password changed successfully"}

    async def refresh_access_token(self, refresh_token: str) -> Token:
        """
        Generate new access token from refresh token

        Args:
            refresh_token: Valid refresh token

        Returns:
            Token: New access token

        Raises:
            HTTPException: 401 if refresh token is invalid
        """
        from app.core.security import decode_access_token, validate_token_type

        payload = decode_access_token(refresh_token)

        if payload is None or not validate_token_type(payload, "refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        user_id = payload.get("sub")
        user_type = payload.get("user_type")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Create new access token
        access_token = create_access_token(data={"sub": user_id, "user_type": user_type})

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
