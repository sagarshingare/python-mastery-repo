"""Practical debugging and logging patterns for beginner Python engineers.

This module provides helper functions compatible with Python 3.10+ and demonstrates
production-grade logging patterns including:
- configurable logger setup
- lifecycle and contextual logging
- exception capture with tracebacks
- execution timing and section boundaries
"""

from __future__ import annotations

import logging
import time
import traceback
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def setup_logger(name: str, log_file: Path | None = None, level: int = logging.INFO) -> logging.Logger:
    """Create and configure a logger for console and optional file output.

    Args:
        name: The logger name to use.
        log_file: Optional file path for log persistence.
        level: Logging level threshold.

    Returns:
        A configured logger instance.

    Example output:
        2026-05-07 10:00:00 INFO core_python_basics - Starting step: load_data
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_file is not None:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


def record_processing_step(logger: logging.Logger, step_name: str) -> None:
    """Record a standard processing lifecycle message."""
    logger.info("Starting step: %s", step_name)


def log_debug_context(logger: logging.Logger, message: str, context: dict[str, Any]) -> None:
    """Log a message with structured context details."""
    formatted_context = ", ".join(f"{key}={value!r}" for key, value in context.items())
    logger.debug("%s | context: %s", message, formatted_context)


def log_exception(logger: logging.Logger, error: Exception, message: str = "Unhandled exception") -> None:
    """Log an exception with a debug traceback."""
    logger.error("%s: %s", message, error)
    logger.debug("Traceback:\n%s", traceback.format_exc())


def time_execution(function: Callable[..., T]) -> Callable[..., T]:
    """Decorator that logs the execution duration for a function."""
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        duration = time.perf_counter() - start_time
        logger = logging.getLogger(function.__module__)
        if not logger.handlers:
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
            fallback_handler = logging.StreamHandler()
            fallback_handler.setFormatter(formatter)
            logger.addHandler(fallback_handler)
            logger.setLevel(logging.INFO)
        logger.info("Completed %s in %.4fs", function.__name__, duration)
        return result

    return wrapper


@contextmanager
def logging_section(logger: logging.Logger, section_name: str) -> Any:
    """Context manager that logs section start and end boundaries."""
    logger.info("BEGIN %s", section_name)
    try:
        yield
    finally:
        logger.info("END %s", section_name)
