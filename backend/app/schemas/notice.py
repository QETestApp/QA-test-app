"""Notice schemas."""

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class NoticeCreate(BaseModel):
    """Schema for creating a notice."""
    title: str
    description: Optional[str] = None
    created_by: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title is required and cannot be empty")
        return v.strip()


class NoticeUpdate(BaseModel):
    """Schema for updating a notice."""
    title: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v


class NoticeResponse(BaseModel):
    """Notice data in API responses."""
    id: int
    title: str
    description: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
