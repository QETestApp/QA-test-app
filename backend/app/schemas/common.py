"""Common response schemas used across all modules."""

from pydantic import BaseModel
from typing import Any


class ErrorDetail(BaseModel):
    """Single field-level error."""
    field: str
    message: str


class ErrorResponse(BaseModel):
    """Consistent error response format."""
    success: bool = False
    message: str
    errors: list[ErrorDetail] = []


class SuccessResponse(BaseModel):
    """Consistent success response format."""
    success: bool = True
    message: str
    data: Any = None


class PaginatedResponse(BaseModel):
    """Paginated list response."""
    success: bool = True
    data: list[Any]
    page: int
    limit: int
    total: int
    total_pages: int
