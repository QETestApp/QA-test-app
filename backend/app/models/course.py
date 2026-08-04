"""Course model."""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_name = Column(String, nullable=False)
    course_code = Column(String, unique=True, nullable=False, index=True)
    duration = Column(String, nullable=True)
    faculty = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
