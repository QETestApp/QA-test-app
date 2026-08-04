"""Attendance model."""

from datetime import datetime, timezone, date as date_type

from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey

from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # Present, Absent, Late
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
