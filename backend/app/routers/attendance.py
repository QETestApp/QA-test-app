"""
Attendance router — Full CRUD.

Endpoints:
    POST   /attendance       — Record attendance
    GET    /attendance       — List attendance records
    GET    /attendance/{id}  — Get a single record
    PUT    /attendance/{id}  — Update a record
    DELETE /attendance/{id}  — Delete a record
"""

import math
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.database import get_db
from app.dependencies import get_current_user
from app.errors import AppException
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post(
    "",
    status_code=201,
    summary="Record Attendance",
    description="Create a new attendance record. Student must exist.",
    responses={
        201: {"description": "Attendance recorded"},
        401: {"description": "Unauthorized"},
        404: {"description": "Student not found"},
        422: {"description": "Validation error"},
    },
)
def create_attendance(
    body: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify student exists
    student = db.query(Student).filter(Student.id == body.student_id).first()
    if not student:
        raise AppException(
            status_code=404,
            message="Student not found",
            errors=[{"field": "student_id", "message": f"Student with ID {body.student_id} does not exist"}],
        )

    record = Attendance(
        student_id=body.student_id,
        date=body.date,
        status=body.status,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "success": True,
        "message": "Attendance recorded successfully",
        "data": AttendanceResponse.model_validate(record).model_dump(),
    }


@router.get(
    "",
    summary="List Attendance",
    description="List attendance records with optional filters.",
    responses={
        200: {"description": "Attendance list"},
        401: {"description": "Unauthorized"},
    },
)
def list_attendance(
    student_id: int | None = Query(None, description="Filter by student ID"),
    status: str | None = Query(None, description="Filter by status (Present, Absent, Late)"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("id", description="Sort field"),
    order: str = Query("asc", description="Sort order (asc, desc)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Attendance)

    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    if status:
        query = query.filter(Attendance.status == status)

    total = query.count()

    sort_columns = {
        "id": Attendance.id,
        "student_id": Attendance.student_id,
        "date": Attendance.date,
        "status": Attendance.status,
    }
    sort_col = sort_columns.get(sort, Attendance.id)
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))

    offset = (page - 1) * limit
    records = query.offset(offset).limit(limit).all()

    return {
        "success": True,
        "data": [AttendanceResponse.model_validate(r).model_dump() for r in records],
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": math.ceil(total / limit) if total > 0 else 0,
    }


@router.get(
    "/{record_id}",
    summary="Get Attendance Record",
    description="Get a single attendance record by ID.",
    responses={
        200: {"description": "Record found"},
        401: {"description": "Unauthorized"},
        404: {"description": "Record not found"},
    },
)
def get_attendance(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Attendance).filter(Attendance.id == record_id).first()
    if not record:
        raise AppException(status_code=404, message="Attendance record not found")

    return {
        "success": True,
        "data": AttendanceResponse.model_validate(record).model_dump(),
    }


@router.put(
    "/{record_id}",
    summary="Update Attendance Record",
    description="Update an existing attendance record.",
    responses={
        200: {"description": "Record updated"},
        401: {"description": "Unauthorized"},
        404: {"description": "Record not found"},
        422: {"description": "Validation error"},
    },
)
def update_attendance(
    record_id: int,
    body: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Attendance).filter(Attendance.id == record_id).first()
    if not record:
        raise AppException(status_code=404, message="Attendance record not found")

    if body.student_id is not None:
        student = db.query(Student).filter(Student.id == body.student_id).first()
        if not student:
            raise AppException(
                status_code=404,
                message="Student not found",
                errors=[{"field": "student_id", "message": f"Student with ID {body.student_id} does not exist"}],
            )

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    record.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(record)

    return {
        "success": True,
        "message": "Attendance record updated successfully",
        "data": AttendanceResponse.model_validate(record).model_dump(),
    }


@router.delete(
    "/{record_id}",
    summary="Delete Attendance Record",
    description="Delete an attendance record by ID.",
    responses={
        200: {"description": "Record deleted"},
        401: {"description": "Unauthorized"},
        404: {"description": "Record not found"},
    },
)
def delete_attendance(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Attendance).filter(Attendance.id == record_id).first()
    if not record:
        raise AppException(status_code=404, message="Attendance record not found")

    db.delete(record)
    db.commit()

    return {
        "success": True,
        "message": "Attendance record deleted successfully",
    }
