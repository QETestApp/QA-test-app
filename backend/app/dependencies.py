"""
Shared dependencies for route handlers.
"""

from datetime import datetime, timezone

from fastapi import Depends, Header
from sqlalchemy.orm import Session
import jwt

from app.config import settings
from app.database import get_db
from app.errors import AppException
from app.models.user import User

# In-memory token blacklist (resets on server restart — intentional for test playground)
_blacklisted_tokens: set[str] = set()


def blacklist_token(token: str) -> None:
    """Add a token to the blacklist."""
    _blacklisted_tokens.add(token)


def is_token_blacklisted(token: str) -> bool:
    """Check if a token has been blacklisted."""
    return token in _blacklisted_tokens


def get_current_user(
    authorization: str = Header(..., description="Bearer <JWT token>"),
    db: Session = Depends(get_db),
) -> User:
    """
    Extract and validate JWT from the Authorization header.
    Returns the authenticated User or raises 401.
    """
    if not authorization.startswith("Bearer "):
        raise AppException(
            status_code=401,
            message="Invalid authorization header format. Expected: Bearer <token>",
        )

    token = authorization.split("Bearer ")[1]

    if is_token_blacklisted(token):
        raise AppException(
            status_code=401,
            message="Token has been revoked",
        )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise AppException(
            status_code=401,
            message="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise AppException(
            status_code=401,
            message="Invalid token",
        )

    user_id: int | None = payload.get("sub")
    if user_id is None:
        raise AppException(
            status_code=401,
            message="Invalid token payload",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise AppException(
            status_code=401,
            message="User not found",
        )

    return user
