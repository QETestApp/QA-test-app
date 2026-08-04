"""
Consistent error handling and custom exception classes.

All API errors follow this format:
{
    "success": false,
    "message": "...",
    "errors": [{"field": "...", "message": "..."}]
}
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppException(Exception):
    """Custom application exception with consistent error format."""

    def __init__(
        self,
        status_code: int,
        message: str,
        errors: list[dict] | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.errors = errors or []


def error_response(status_code: int, message: str, errors: list[dict] | None = None) -> JSONResponse:
    """Build a consistent error JSONResponse."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "errors": errors or [],
        },
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom AppException."""
    return error_response(exc.status_code, exc.message, exc.errors)


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle FastAPI/Starlette HTTPException with consistent format."""
    return error_response(exc.status_code, str(exc.detail))


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors with consistent format."""
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err.get("loc", []) if str(loc) != "body")
        errors.append({
            "field": field or "unknown",
            "message": err.get("msg", "Validation error"),
        })
    return error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Validation failed",
        errors,
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected errors."""
    return error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Internal server error",
    )
