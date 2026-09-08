"""
Exception handling strategies, chaining, suppression, and recovery patterns.
=============================================================================
Covers:
- Safe execution with fallback values
- Explicit exception chaining with `raise ... from cause` (PEP 3134)
- Suppressing exception context with `raise ... from None`
- Safe input validation
- Traceback string extraction and logging
"""

from __future__ import annotations
import logging
import traceback
from typing import Any, Callable, Optional, TypeVar
from .custom_exceptions import AppError, DatabaseError, ResourceUnavailableError, ValidationError

T = TypeVar("T")
logger = logging.getLogger(__name__)


def safe_execute(function: Callable[..., T], *args: Any, default: Optional[T] = None, **kwargs: Any) -> Optional[T]:
    """Execute a callable safely, returning default on exception."""
    try:
        return function(*args, **kwargs)
    except Exception as exc:
        logger.error("safe_execute failed for %s: %s", getattr(function, "__name__", str(function)), exc)
        return default


def validate_input(value: str) -> None:
    """Validate string input, raising ValidationError if invalid."""
    if not value or not value.strip():
        raise ValidationError("string value cannot be empty", field="input")


def guard_against_resource_failure(resource_name: str, available: bool = True) -> None:
    """Ensure an external resource is available, or raise ResourceUnavailableError."""
    if not available:
        raise ResourceUnavailableError(resource_name, reason="Resource connection offline")


def execute_with_chaining(raw_query: str) -> str:
    """Demonstrates explicit exception chaining with `raise ... from original_error`.

    Preserves the root cause exception in the __cause__ attribute.
    """
    try:
        if "syntax_error" in raw_query:
            # Simulate low-level driver failure
            raise ConnectionRefusedError("Connection reset by peer on socket 5432")
        return f"Executed query: {raw_query}"
    except ConnectionRefusedError as driver_err:
        # Wrap in high-level domain exception while preserving driver error in traceback
        raise DatabaseError("Failed executing user query due to connection fault") from driver_err


def execute_with_suppressed_cause(secret_token: str) -> str:
    """Demonstrates suppressing exception cause with `raise ... from None`.

    Hides internal traceback context from leaking to public callers or security logs.
    """
    try:
        if secret_token != "valid_token":
            raise PermissionError(f"Internal cryptographic key mismatch for {secret_token}")
        return "Access granted"
    except PermissionError:
        # Hide original trace and secret token details
        raise ValidationError("Invalid authentication credentials provided") from None


def get_formatted_traceback(exc: BaseException) -> str:
    """Extract full traceback as a formatted string."""
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
