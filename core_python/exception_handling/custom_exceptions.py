"""
Custom exception classes for domain-specific errors and structured API failures.
================================================================================
Covers:
- Base domain exception with structured error code and HTTP mapping
- Specific client errors (Validation, NotFound, Unauthorized, Conflict)
- Infrastructure errors (ResourceUnavailable, DatabaseError)
"""

from __future__ import annotations
import time
from typing import Any, Dict, Optional


class AppError(Exception):
    """Base application exception with structured error code, status, and metadata."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize exception to structured JSON-compatible payload."""
        return {
            "error": self.error_code,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
            "timestamp": self.timestamp,
        }


class ValidationError(AppError):
    """Raised when client input fails business rules or schema validation."""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        details = {"field": field} if field else {}
        super().__init__(message, error_code="VALIDATION_FAILED", status_code=400, details=details)


class NotFoundError(AppError):
    """Raised when requested entity or resource is missing."""

    def __init__(self, resource_type: str, resource_id: str) -> None:
        msg = f"{resource_type} with ID '{resource_id}' was not found."
        super().__init__(msg, error_code="NOT_FOUND", status_code=404, details={"type": resource_type, "id": resource_id})


class ResourceUnavailableError(AppError):
    """Raised when external infrastructure (db, cache, third-party api) is unreachable."""

    def __init__(self, resource_name: str, reason: str = "Timeout") -> None:
        msg = f"Resource '{resource_name}' is currently unavailable: {reason}"
        super().__init__(msg, error_code="SERVICE_UNAVAILABLE", status_code=503, details={"resource": resource_name, "reason": reason})


class DatabaseError(AppError):
    """Raised on SQL or storage failure, typically wrapping a low-level DB driver exception."""

    def __init__(self, message: str = "Database operation failed") -> None:
        super().__init__(message, error_code="DATABASE_ERROR", status_code=500)
