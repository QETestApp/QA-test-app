"""Course schemas."""

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class CourseCreate(BaseModel):
    """Schema for creating a course."""
    course_name: str
    course_code: str
    duration: Optional[str] = None
    faculty: Optional[str] = None

    @field_validator("course_name")
    @classmethod
    def course_name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Course name is required and cannot be empty")
        return v.strip()

    @field_validator("course_code")
    @classmethod
    def course_code_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Course code is required and cannot be empty")
        return v.strip().upper()


class CourseUpdate(BaseModel):
    """Schema for updating a course. All fields optional."""
    course_name: Optional[str] = None
    course_code: Optional[str] = None
    duration: Optional[str] = None
    faculty: Optional[str] = None

    @field_validator("course_name")
    @classmethod
    def course_name_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Course name cannot be empty")
        return v.strip() if v else v

    @field_validator("course_code")
    @classmethod
    def course_code_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Course code cannot be empty")
        return v.strip().upper() if v else v


class CourseResponse(BaseModel):
    """Course data in API responses."""
    id: int
    course_name: str
    course_code: str
    duration: Optional[str] = None
    faculty: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
