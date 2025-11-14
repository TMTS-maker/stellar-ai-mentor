"""Classrooms router with bulk student import"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user, require_role, get_password_hash
from app.db import get_db
from app.models.user import User, UserRole
from app.models.classroom import Classroom, Enrollment
from app.models.student import Student
from app.schemas.student import StudentBulkCreate

router = APIRouter(prefix="/classes", tags=["Classrooms"])


@router.post("/{class_id}/students/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_import_students(
    class_id: UUID,
    bulk_data: StudentBulkCreate,
    current_user: User = Depends(require_role("teacher", "school_admin")),
    db: AsyncSession = Depends(get_db)
):
    """
    Bulk import students to a classroom.

    Accepts a list of student data (email, full_name, password, grade_level).
    Creates User accounts, Student profiles, and Enrollments.
    """
    # Verify classroom exists
    result = await db.execute(select(Classroom).where(Classroom.id == class_id))
    classroom = result.scalar_one_or_none()

    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found"
        )

    created_students = []
    errors = []

    for idx, student_data in enumerate(bulk_data.students):
        try:
            # Check if email already exists
            email = student_data.get("email")
            full_name = student_data.get("full_name")
            password = student_data.get("password", "DefaultPassword123")
            grade_level = student_data.get("grade_level")

            if not email or not full_name:
                errors.append({
                    "index": idx,
                    "email": email,
                    "error": "Email and full_name are required"
                })
                continue

            result = await db.execute(select(User).where(User.email == email))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                errors.append({
                    "index": idx,
                    "email": email,
                    "error": "Email already registered"
                })
                continue

            # Create user
            user = User(
                email=email,
                password_hash=get_password_hash(password),
                full_name=full_name,
                role=UserRole.STUDENT
            )
            db.add(user)
            await db.flush()

            # Create student profile
            student = Student(
                user_id=user.id,
                school_id=classroom.school_id,
                grade_level=grade_level
            )
            db.add(student)
            await db.flush()

            # Create enrollment
            enrollment = Enrollment(
                student_id=student.id,
                classroom_id=class_id
            )
            db.add(enrollment)

            created_students.append({
                "email": email,
                "student_id": str(student.id),
                "user_id": str(user.id)
            })

        except Exception as e:
            errors.append({
                "index": idx,
                "email": student_data.get("email"),
                "error": str(e)
            })

    await db.commit()

    return {
        "created_count": len(created_students),
        "error_count": len(errors),
        "created_students": created_students,
        "errors": errors
    }
