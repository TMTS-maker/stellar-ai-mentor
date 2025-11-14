"""Classroom, enrollment, and class-subject models"""
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class Classroom(Base):
    """Classroom model"""
    __tablename__ = "classrooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=False)
    name = Column(String, nullable=False)
    grade_level = Column(String, nullable=True)

    # Relationships
    school = relationship("School", back_populates="classrooms")
    teacher = relationship("Teacher", back_populates="classrooms")
    enrollments = relationship("Enrollment", back_populates="classroom")
    subject_links = relationship("ClassSubject", back_populates="classroom")

    def __repr__(self):
        return f"<Classroom(id={self.id}, name={self.name})>"


class ClassSubject(Base):
    """Many-to-many relationship between classrooms and subjects"""
    __tablename__ = "class_subjects"

    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id"), primary_key=True)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), primary_key=True)

    # Relationships
    classroom = relationship("Classroom", back_populates="subject_links")
    subject = relationship("Subject", back_populates="classroom_links")

    def __repr__(self):
        return f"<ClassSubject(classroom_id={self.classroom_id}, subject_id={self.subject_id})>"


class Enrollment(Base):
    """Student enrollment in a classroom"""
    __tablename__ = "enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id"), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    classroom = relationship("Classroom", back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(id={self.id}, student_id={self.student_id}, classroom_id={self.classroom_id})>"
