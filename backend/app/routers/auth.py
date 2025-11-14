"""Authentication router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import verify_password, get_password_hash, create_access_token, create_refresh_token, get_current_user
from app.db import get_db
from app.models.user import User, UserRole
from app.models.school import School
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.parent import Parent
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    Creates User and associated role profile (School, Teacher, Student, or Parent).
    """
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(user)
    await db.flush()

    # Create role-specific profile
    if user_data.role == UserRole.SCHOOL_ADMIN:
        # For school admin, we need to create a school
        # This is simplified - in production, you might want a separate endpoint
        school = School(
            name=f"{user_data.full_name}'s School",
            admin_user_id=user.id
        )
        db.add(school)

    elif user_data.role == UserRole.TEACHER:
        if not user_data.school_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="school_id required for teachers"
            )
        teacher = Teacher(
            user_id=user.id,
            school_id=user_data.school_id
        )
        db.add(teacher)

    elif user_data.role == UserRole.STUDENT:
        if not user_data.school_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="school_id required for students"
            )
        student = Student(
            user_id=user.id,
            school_id=user_data.school_id,
            grade_level=user_data.grade_level
        )
        db.add(student)

    elif user_data.role == UserRole.PARENT:
        parent = Parent(
            user_id=user.id
        )
        db.add(parent)

    await db.commit()
    await db.refresh(user)

    return user


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login with email and password, returns JWT tokens"""
    # Find user by email
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """Refresh access token using refresh token"""
    access_token = create_access_token(current_user.id)
    refresh_token = create_refresh_token(current_user.id)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information"""
    return current_user
