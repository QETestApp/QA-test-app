"""
Seed data for the QA Test Playground.

Seeds:
    - 1 admin user (admin@test.com / password123)
    - 10 students
    - 5 courses
    - 20 attendance records
    - 5 notices

Only runs when the database is empty (idempotent).
"""

import hashlib
from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.student import Student
from app.models.course import Course
from app.models.attendance import Attendance
from app.models.notice import Notice


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def seed_database(db: Session) -> None:
    """Seed the database with test data if it's empty."""

    # Check if already seeded
    if db.query(User).count() > 0:
        return

    print("[SEED] Seeding database with test data...")

    # ── Admin User ──────────────────────────────────────────────
    admin = User(
        email="admin@test.com",
        hashed_password=_hash_password("password123"),
        name="Admin User",
    )
    db.add(admin)
    db.flush()

    # ── Courses ─────────────────────────────────────────────────
    courses_data = [
        {"course_name": "Computer Science", "course_code": "CSE", "duration": "4 Years", "faculty": "Dr. Alan Turing"},
        {"course_name": "Electrical Engineering", "course_code": "EE", "duration": "4 Years", "faculty": "Dr. Nikola Tesla"},
        {"course_name": "Mechanical Engineering", "course_code": "ME", "duration": "4 Years", "faculty": "Dr. James Watt"},
        {"course_name": "Business Administration", "course_code": "MBA", "duration": "2 Years", "faculty": "Dr. Peter Drucker"},
        {"course_name": "Data Science", "course_code": "DS", "duration": "3 Years", "faculty": "Dr. Ada Lovelace"},
    ]
    courses = []
    for c in courses_data:
        course = Course(**c)
        db.add(course)
        courses.append(course)
    db.flush()

    # ── Students ────────────────────────────────────────────────
    students_data = [
        {"student_id": "STU-001", "name": "John Doe", "email": "john.doe@test.com", "phone": "+1-555-0101", "course": "CSE", "semester": 3, "date_of_birth": date(2002, 5, 15), "address": "123 Main St, Springfield"},
        {"student_id": "STU-002", "name": "Jane Smith", "email": "jane.smith@test.com", "phone": "+1-555-0102", "course": "CSE", "semester": 5, "date_of_birth": date(2001, 8, 22), "address": "456 Oak Ave, Portland"},
        {"student_id": "STU-003", "name": "Bob Johnson", "email": "bob.johnson@test.com", "phone": "+1-555-0103", "course": "EE", "semester": 2, "date_of_birth": date(2003, 1, 10), "address": "789 Pine Rd, Seattle"},
        {"student_id": "STU-004", "name": "Alice Williams", "email": "alice.williams@test.com", "phone": "+1-555-0104", "course": "ME", "semester": 4, "date_of_birth": date(2002, 11, 3), "address": "321 Elm St, Boston"},
        {"student_id": "STU-005", "name": "Charlie Brown", "email": "charlie.brown@test.com", "phone": "+1-555-0105", "course": "MBA", "semester": 1, "date_of_birth": date(2000, 7, 28), "address": "654 Maple Dr, Chicago"},
        {"student_id": "STU-006", "name": "Diana Prince", "email": "diana.prince@test.com", "phone": "+1-555-0106", "course": "DS", "semester": 3, "date_of_birth": date(2001, 3, 14), "address": "987 Cedar Ln, Denver"},
        {"student_id": "STU-007", "name": "Edward Norton", "email": "edward.norton@test.com", "phone": "+1-555-0107", "course": "CSE", "semester": 7, "date_of_birth": date(2000, 9, 5), "address": "147 Birch Ct, Austin"},
        {"student_id": "STU-008", "name": "Fiona Apple", "email": "fiona.apple@test.com", "phone": "+1-555-0108", "course": "EE", "semester": 6, "date_of_birth": date(2001, 12, 18), "address": "258 Walnut Way, Miami"},
        {"student_id": "STU-009", "name": "George Miller", "email": "george.miller@test.com", "phone": "+1-555-0109", "course": "DS", "semester": 2, "date_of_birth": date(2003, 4, 25), "address": "369 Spruce Ave, Nashville"},
        {"student_id": "STU-010", "name": "Hannah Davis", "email": "hannah.davis@test.com", "phone": "+1-555-0110", "course": "MBA", "semester": 2, "date_of_birth": date(2001, 6, 8), "address": "482 Willow Blvd, Atlanta"},
    ]
    students = []
    for s in students_data:
        student = Student(**s)
        db.add(student)
        students.append(student)
    db.flush()

    # ── Attendance Records ──────────────────────────────────────
    statuses = ["Present", "Absent", "Late"]
    attendance_data = []
    base_date = date(2025, 8, 1)
    for i in range(20):
        student_idx = i % len(students)
        day_offset = i % 10
        record = Attendance(
            student_id=students[student_idx].id,
            date=date(base_date.year, base_date.month, base_date.day + day_offset),
            status=statuses[i % 3],
        )
        db.add(record)
    db.flush()

    # ── Notices ─────────────────────────────────────────────────
    notices_data = [
        {"title": "Welcome to QA Test Playground", "description": "This application is designed for QA testing. Feel free to test all CRUD operations.", "created_by": "Admin User"},
        {"title": "Semester Registration Open", "description": "Students can now register for the upcoming semester. Deadline is August 30th.", "created_by": "Admin User"},
        {"title": "Library Hours Extended", "description": "The library will remain open until 10 PM during exam weeks.", "created_by": "Admin User"},
        {"title": "Sports Day Announcement", "description": "Annual sports day will be held on September 15th. All students are encouraged to participate.", "created_by": "Admin User"},
        {"title": "Maintenance Notice", "description": "The system will undergo maintenance on Sunday from 2 AM to 6 AM.", "created_by": "Admin User"},
    ]
    for n in notices_data:
        notice = Notice(**n)
        db.add(notice)

    db.commit()
    print("[OK] Database seeded successfully!")
    print("     Admin login: admin@test.com / password123")
