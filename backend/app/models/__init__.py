# Models package
from app.models.user import User
from app.models.student import Student
from app.models.course import Course
from app.models.attendance import Attendance
from app.models.notice import Notice

__all__ = ["User", "Student", "Course", "Attendance", "Notice"]
