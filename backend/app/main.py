"""QA Test Playground — FastAPI Application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
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

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger("qa_test_playground")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables and seed data."""
    # Import all models so Base.metadata knows about them
    import app.models  # noqa: F401

    logger.info("Starting application in %s mode", settings.APP_ENV)
    Base.metadata.create_all(bind=engine)

    # Seed test data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "A QA testing playground exposing realistic REST APIs with complete CRUD functionality, "
        "JWT authentication, validation, and predictable workflows for manual/automated testing."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# ── CORS ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)
# ── Exception Handlers ─────────────────────────────────────────
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# ── Routers ─────────────────────────────────────────────────────
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(students.router, prefix=settings.API_PREFIX)
app.include_router(courses.router, prefix=settings.API_PREFIX)
app.include_router(attendance.router, prefix=settings.API_PREFIX)
app.include_router(notices.router, prefix=settings.API_PREFIX)


# ── Root ────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    """API health check and welcome message."""
    return {
        "success": True,
        "message": "QA Test Playground API is running",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Production-friendly health endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }
