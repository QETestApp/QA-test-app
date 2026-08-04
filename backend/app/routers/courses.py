"""
Courses router — Full CRUD.

Endpoints:
    POST   /courses       — Create a course
    GET    /courses       — List courses
    GET    /courses/{id}  — Get a single course
    PUT    /courses/{id}  — Update a course
    DELETE /courses/{id}  — Delete a course
"""

import math
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.database import get_db
from app.dependencies import get_current_user
from app.errors import AppException
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post(
    "",
    status_code=201,
    summary="Create Course",
    description="Create a new course. Course code must be unique.",
    responses={
        201: {"description": "Course created"},
        401: {"description": "Unauthorized"},
        409: {"description": "Duplicate course code"},
        422: {"description": "Validation error"},
    },
)
def create_course(
    body: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(Course).filter(Course.course_code == body.course_code).first()
    if existing:
        raise AppException(
            status_code=409,
            message="Duplicate entry",
            errors=[{"field": "course_code", "message": "Course code already exists"}],
        )

    course = Course(
        course_name=body.course_name,
        course_code=body.course_code,
        duration=body.duration,
        faculty=body.faculty,
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    return {
        "success": True,
        "message": "Course created successfully",
        "data": CourseResponse.model_validate(course).model_dump(),
    }


@router.get(
    "",
    summary="List Courses",
    description="List all courses with optional search and pagination.",
    responses={
        200: {"description": "Courses list"},
        401: {"description": "Unauthorized"},
    },
)
def list_courses(
    course_name: str | None = Query(None, description="Filter by course name"),
    course_code: str | None = Query(None, description="Filter by course code"),
    faculty: str | None = Query(None, description="Filter by faculty"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("id", description="Sort field"),
    order: str = Query("asc", description="Sort order (asc, desc)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Course)

    if course_name:
        query = query.filter(Course.course_name.ilike(f"%{course_name}%"))
    if course_code:
        query = query.filter(Course.course_code.ilike(f"%{course_code}%"))
    if faculty:
        query = query.filter(Course.faculty.ilike(f"%{faculty}%"))

    total = query.count()

    sort_columns = {
        "id": Course.id,
        "course_name": Course.course_name,
        "course_code": Course.course_code,
        "faculty": Course.faculty,
    }
    sort_col = sort_columns.get(sort, Course.id)
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))

    offset = (page - 1) * limit
    courses = query.offset(offset).limit(limit).all()

    return {
        "success": True,
        "data": [CourseResponse.model_validate(c).model_dump() for c in courses],
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": math.ceil(total / limit) if total > 0 else 0,
    }


@router.get(
    "/{course_id}",
    summary="Get Course",
    description="Get a single course by ID.",
    responses={
        200: {"description": "Course found"},
        401: {"description": "Unauthorized"},
        404: {"description": "Course not found"},
    },
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise AppException(status_code=404, message="Course not found")

    return {
        "success": True,
        "data": CourseResponse.model_validate(course).model_dump(),
    }


@router.put(
    "/{course_id}",
    summary="Update Course",
    description="Update an existing course.",
    responses={
        200: {"description": "Course updated"},
        401: {"description": "Unauthorized"},
        404: {"description": "Course not found"},
        409: {"description": "Duplicate course code"},
        422: {"description": "Validation error"},
    },
)
def update_course(
    course_id: int,
    body: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise AppException(status_code=404, message="Course not found")

    if body.course_code and body.course_code != course.course_code:
        existing = db.query(Course).filter(Course.course_code == body.course_code).first()
        if existing:
            raise AppException(
                status_code=409,
                message="Duplicate entry",
                errors=[{"field": "course_code", "message": "Course code already exists"}],
            )

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)

    course.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(course)

    return {
        "success": True,
        "message": "Course updated successfully",
        "data": CourseResponse.model_validate(course).model_dump(),
    }


@router.delete(
    "/{course_id}",
    summary="Delete Course",
    description="Delete a course by ID.",
    responses={
        200: {"description": "Course deleted"},
        401: {"description": "Unauthorized"},
        404: {"description": "Course not found"},
    },
)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise AppException(status_code=404, message="Course not found")

    db.delete(course)
    db.commit()

    return {
        "success": True,
        "message": "Course deleted successfully",
    }
