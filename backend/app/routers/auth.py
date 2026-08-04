"""
Authentication router.

Endpoints:
    POST /auth/login   — Authenticate and receive JWT
    POST /auth/logout  — Invalidate JWT
    GET  /auth/profile — Get current user profile
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
import hashlib
import jwt

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_db
from app.dependencies import get_current_user, blacklist_token
from app.errors import AppException
from app.models.user import User
from app.schemas.auth import LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _hash_password(password: str) -> str:
    """Simple SHA-256 hash for the test playground."""
    return hashlib.sha256(password.encode()).hexdigest()


def _create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post(
    "/login",
    summary="Login",
    description="Authenticate with email and password to receive a JWT token.",
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
        422: {"description": "Validation error"},
    },
)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(User).filter(User.email == body.email).first()

    if not user or user.hashed_password != _hash_password(body.password):
        raise AppException(
            status_code=401,
            message="Invalid email or password",
        )

    token = _create_access_token({"sub": str(user.id)})

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
            },
        },
    }


@router.post(
    "/logout",
    summary="Logout",
    description="Invalidate the current JWT token.",
    responses={
        200: {"description": "Logout successful"},
        401: {"description": "Unauthorized"},
    },
)
def logout(
    current_user: User = Depends(get_current_user),
    authorization: str = Header(...),
):
    """Blacklist the current token."""
    token = authorization.split("Bearer ")[1]
    blacklist_token(token)

    return {
        "success": True,
        "message": "Logout successful",
    }


@router.get(
    "/profile",
    summary="Get Profile",
    description="Get the authenticated user's profile.",
    responses={
        200: {"description": "Profile retrieved"},
        401: {"description": "Unauthorized"},
    },
)
def get_profile(current_user: User = Depends(get_current_user)):
    """Return the current user's profile."""
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "created_at": str(current_user.created_at) if current_user.created_at else None,
        },
    }
