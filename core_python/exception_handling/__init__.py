"""
Exception handling module for error recovery, custom hierarchies, and chaining.
"""

from .custom_exceptions import (
    AppError,
    DatabaseError,
    NotFoundError,
    ResourceUnavailableError,
    ValidationError,
)
from .handling_strategies import (
    execute_with_chaining,
    execute_with_suppressed_cause,
    get_formatted_traceback,
    guard_against_resource_failure,
    safe_execute,
    validate_input,
)
from .context_managers import SuppressAndLog

__all__ = [
    "AppError",
    "DatabaseError",
    "NotFoundError",
    "ResourceUnavailableError",
    "SuppressAndLog",
    "ValidationError",
    "execute_with_chaining",
    "execute_with_suppressed_cause",
    "get_formatted_traceback",
    "guard_against_resource_failure",
    "safe_execute",
    "validate_input",
]
