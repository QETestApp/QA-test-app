"""
QA Test Playground — FastAPI Application

A testing playground exposing ~23 realistic REST APIs with complete CRUD,
JWT authentication, OpenAPI documentation, and consistent error handling.

Swagger UI: http://localhost:8000/docs
OpenAPI JSON: http://localhost:8000/openapi.json
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import engine, Base, SessionLocal
from app.errors import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.routers import auth, students, courses, attendance, notices
from app.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables and seed data."""
    # Import all models so Base.metadata knows about them
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # Seed test data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="QA Test Playground API",
    description=(
        "A QA testing playground exposing realistic REST APIs with complete CRUD functionality, "
        "JWT authentication, validation, and predictable workflows for manual/automated testing."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# ── CORS ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local Development
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:3000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",

        # Vercel Production
        "https://qa-test-app-seven.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ── Exception Handlers ─────────────────────────────────────────
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ── Routers ─────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(attendance.router)
app.include_router(notices.router)


# ── Root ────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    """API health check and welcome message."""
    return {
        "success": True,
        "message": "QA Test Playground API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
