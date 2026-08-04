"""Authentication schemas."""

from pydantic import BaseModel, EmailStr
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request body."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login success response."""
    success: bool = True
    message: str = "Login successful"
    data: dict


class ProfileResponse(BaseModel):
    """User profile response."""
    success: bool = True
    data: dict
