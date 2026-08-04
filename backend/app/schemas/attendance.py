"""Attendance schemas."""

from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional


VALID_STATUSES = ["Present", "Absent", "Late"]


class AttendanceCreate(BaseModel):
    """Schema for creating an attendance record."""
    student_id: int
    date: date
    status: str

    @field_validator("status")
    @classmethod
    def status_must_be_valid(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}")
        return v


class AttendanceUpdate(BaseModel):
    """Schema for updating an attendance record."""
    student_id: Optional[int] = None
    date: Optional[date] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def status_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}")
        return v


class AttendanceResponse(BaseModel):
    """Attendance data in API responses."""
    id: int
    student_id: int
    date: date
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
