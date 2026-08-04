"""
Notices router — Full CRUD.

Endpoints:
    POST   /notices       — Create a notice
    GET    /notices       — List notices
    GET    /notices/{id}  — Get a single notice
    PUT    /notices/{id}  — Update a notice
    DELETE /notices/{id}  — Delete a notice
"""

import math
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.database import get_db
from app.dependencies import get_current_user
from app.errors import AppException
from app.models.notice import Notice
from app.models.user import User
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeResponse

router = APIRouter(prefix="/notices", tags=["Notices"])


@router.post(
    "",
    status_code=201,
    summary="Create Notice",
    description="Create a new notice.",
    responses={
        201: {"description": "Notice created"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
    },
)
def create_notice(
    body: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notice = Notice(
        title=body.title,
        description=body.description,
        created_by=body.created_by or current_user.name,
    )
    db.add(notice)
    db.commit()
    db.refresh(notice)

    return {
        "success": True,
        "message": "Notice created successfully",
        "data": NoticeResponse.model_validate(notice).model_dump(),
    }


@router.get(
    "",
    summary="List Notices",
    description="List all notices with optional search and pagination.",
    responses={
        200: {"description": "Notices list"},
        401: {"description": "Unauthorized"},
    },
)
def list_notices(
    title: str | None = Query(None, description="Filter by title"),
    created_by: str | None = Query(None, description="Filter by creator"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("id", description="Sort field"),
    order: str = Query("asc", description="Sort order (asc, desc)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Notice)

    if title:
        query = query.filter(Notice.title.ilike(f"%{title}%"))
    if created_by:
        query = query.filter(Notice.created_by.ilike(f"%{created_by}%"))

    total = query.count()

    sort_columns = {
        "id": Notice.id,
        "title": Notice.title,
        "created_by": Notice.created_by,
        "created_at": Notice.created_at,
    }
    sort_col = sort_columns.get(sort, Notice.id)
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))

    offset = (page - 1) * limit
    notices = query.offset(offset).limit(limit).all()

    return {
        "success": True,
        "data": [NoticeResponse.model_validate(n).model_dump() for n in notices],
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": math.ceil(total / limit) if total > 0 else 0,
    }


@router.get(
    "/{notice_id}",
    summary="Get Notice",
    description="Get a single notice by ID.",
    responses={
        200: {"description": "Notice found"},
        401: {"description": "Unauthorized"},
        404: {"description": "Notice not found"},
    },
)
def get_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise AppException(status_code=404, message="Notice not found")

    return {
        "success": True,
        "data": NoticeResponse.model_validate(notice).model_dump(),
    }


@router.put(
    "/{notice_id}",
    summary="Update Notice",
    description="Update an existing notice.",
    responses={
        200: {"description": "Notice updated"},
        401: {"description": "Unauthorized"},
        404: {"description": "Notice not found"},
        422: {"description": "Validation error"},
    },
)
def update_notice(
    notice_id: int,
    body: NoticeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise AppException(status_code=404, message="Notice not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(notice, field, value)

    notice.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(notice)

    return {
        "success": True,
        "message": "Notice updated successfully",
        "data": NoticeResponse.model_validate(notice).model_dump(),
    }


@router.delete(
    "/{notice_id}",
    summary="Delete Notice",
    description="Delete a notice by ID.",
    responses={
        200: {"description": "Notice deleted"},
        401: {"description": "Unauthorized"},
        404: {"description": "Notice not found"},
    },
)
def delete_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise AppException(status_code=404, message="Notice not found")

    db.delete(notice)
    db.commit()

    return {
        "success": True,
        "message": "Notice deleted successfully",
    }
