"""
Students router — Full CRUD with search, filter, pagination, and sort.

Endpoints:
    POST   /students       — Create a student
    GET    /students       — List students (with query params)
    GET    /students/{id}  — Get a single student
    PUT    /students/{id}  — Update a student
    DELETE /students/{id}  — Delete a student
"""

import math
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.database import get_db
from app.dependencies import get_current_user
from app.errors import AppException
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


def _generate_student_id(db: Session) -> str:
    """Generate next student ID like STU-001, STU-002, etc."""
    last = db.query(Student).order_by(Student.id.desc()).first()
    next_num = (last.id + 1) if last else 1
    return f"STU-{next_num:03d}"


@router.post(
    "",
    status_code=201,
    summary="Create Student",
    description="Create a new student. Email must be unique.",
    responses={
        201: {"description": "Student created"},
        401: {"description": "Unauthorized"},
        409: {"description": "Duplicate email"},
        422: {"description": "Validation error"},
    },
)
def create_student(
    body: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check duplicate email
    existing = db.query(Student).filter(Student.email == body.email).first()
    if existing:
        raise AppException(
            status_code=409,
            message="Duplicate entry",
            errors=[{"field": "email", "message": "Email already exists"}],
        )

    student = Student(
        student_id=_generate_student_id(db),
        name=body.name,
        email=body.email,
        phone=body.phone,
        course=body.course,
        semester=body.semester,
        date_of_birth=body.date_of_birth,
        address=body.address,
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "success": True,
        "message": "Student created successfully",
        "data": StudentResponse.model_validate(student).model_dump(),
    }


@router.get(
    "",
    summary="List Students",
    description="List students with optional search, filter, pagination, and sort.",
    responses={
        200: {"description": "Students list"},
        401: {"description": "Unauthorized"},
    },
)
def list_students(
    name: str | None = Query(None, description="Filter by name (partial match)"),
    course: str | None = Query(None, description="Filter by course (partial match)"),
    email: str | None = Query(None, description="Filter by email (partial match)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    sort: str = Query("id", description="Sort field (id, name, email, course, student_id)"),
    order: str = Query("asc", description="Sort order (asc, desc)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Student)

    # Filters
    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))
    if course:
        query = query.filter(Student.course.ilike(f"%{course}%"))
    if email:
        query = query.filter(Student.email.ilike(f"%{email}%"))

    # Total count before pagination
    total = query.count()

    # Sort
    sort_columns = {
        "id": Student.id,
        "name": Student.name,
        "email": Student.email,
        "course": Student.course,
        "student_id": Student.student_id,
    }
    sort_col = sort_columns.get(sort, Student.id)
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))

    # Pagination
    offset = (page - 1) * limit
    students = query.offset(offset).limit(limit).all()

    return {
        "success": True,
        "data": [StudentResponse.model_validate(s).model_dump() for s in students],
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": math.ceil(total / limit) if total > 0 else 0,
    }


@router.get(
    "/{student_id}",
    summary="Get Student",
    description="Get a single student by ID.",
    responses={
        200: {"description": "Student found"},
        401: {"description": "Unauthorized"},
        404: {"description": "Student not found"},
    },
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise AppException(status_code=404, message="Student not found")

    return {
        "success": True,
        "data": StudentResponse.model_validate(student).model_dump(),
    }


@router.put(
    "/{student_id}",
    summary="Update Student",
    description="Update an existing student. Email must remain unique.",
    responses={
        200: {"description": "Student updated"},
        401: {"description": "Unauthorized"},
        404: {"description": "Student not found"},
        409: {"description": "Duplicate email"},
        422: {"description": "Validation error"},
    },
)
def update_student(
    student_id: int,
    body: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise AppException(status_code=404, message="Student not found")

    # Check duplicate email if email is being updated
    if body.email and body.email != student.email:
        existing = db.query(Student).filter(Student.email == body.email).first()
        if existing:
            raise AppException(
                status_code=409,
                message="Duplicate entry",
                errors=[{"field": "email", "message": "Email already exists"}],
            )

    # Apply updates
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)

    student.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(student)

    return {
        "success": True,
        "message": "Student updated successfully",
        "data": StudentResponse.model_validate(student).model_dump(),
    }


@router.delete(
    "/{student_id}",
    summary="Delete Student",
    description="Delete a student by ID.",
    responses={
        200: {"description": "Student deleted"},
        401: {"description": "Unauthorized"},
        404: {"description": "Student not found"},
    },
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise AppException(status_code=404, message="Student not found")

    db.delete(student)
    db.commit()

    return {
        "success": True,
        "message": "Student deleted successfully",
    }
