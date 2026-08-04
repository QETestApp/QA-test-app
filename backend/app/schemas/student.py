"""Student schemas with validation."""

from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
from typing import Optional
import re


class StudentCreate(BaseModel):
    """Schema for creating a student."""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    course: Optional[str] = None
    semester: Optional[int] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name is required and cannot be empty")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def phone_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip():
            # Accept common phone formats: digits, spaces, dashes, parentheses, plus
            pattern = r"^[\d\s\-\+\(\)]{7,20}$"
            if not re.match(pattern, v.strip()):
                raise ValueError(
                    "Invalid phone number format. Must be 7-20 characters with digits, spaces, dashes, or parentheses"
                )
            return v.strip()
        return v

    @field_validator("semester")
    @classmethod
    def semester_must_be_valid(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 1 or v > 12):
            raise ValueError("Semester must be between 1 and 12")
        return v


class StudentUpdate(BaseModel):
    """Schema for updating a student. All fields optional."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    semester: Optional[int] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip() if v else v

    @field_validator("phone")
    @classmethod
    def phone_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip():
            pattern = r"^[\d\s\-\+\(\)]{7,20}$"
            if not re.match(pattern, v.strip()):
                raise ValueError(
                    "Invalid phone number format. Must be 7-20 characters with digits, spaces, dashes, or parentheses"
                )
            return v.strip()
        return v

    @field_validator("semester")
    @classmethod
    def semester_must_be_valid(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 1 or v > 12):
            raise ValueError("Semester must be between 1 and 12")
        return v


class StudentResponse(BaseModel):
    """Student data in API responses."""
    id: int
    student_id: str
    name: str
    email: str
    phone: Optional[str] = None
    course: Optional[str] = None
    semester: Optional[int] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
