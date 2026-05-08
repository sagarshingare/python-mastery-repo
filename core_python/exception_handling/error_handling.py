"""Exception handling utilities and custom error classes."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    """A validation error for domain-specific input checks."""


class ResourceUnavailableError(RuntimeError):
    """Raise when an external resource is not available."""


def safe_execute(function: callable, *args: Any, default: Any = None, **kwargs: Any) -> Any:
    """Execute a function and return a default value on exception."""
    try:
        return function(*args, **kwargs)
    except Exception as error:
        logger.exception("safe_execute failed for %s", function.__name__)
        return default


def validate_input(data: Any) -> None:
    """Raise a ValidationError when the input does not meet basic rules."""
    if data is None:
        raise ValidationError("data cannot be None")
    if isinstance(data, str) and not data.strip():
        raise ValidationError("string value cannot be empty")


def guard_against_resource_failure(resource_name: str, available: bool) -> None:
    """Raise a resource-specific error if a resource is unavailable."""
    if not available:
        raise ResourceUnavailableError(f"Resource '{resource_name}' is unavailable")
