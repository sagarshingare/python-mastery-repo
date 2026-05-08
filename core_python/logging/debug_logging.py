"""Structured logging utilities and decorators for production Python."""

from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


def setup_logger(name: str, log_file: Path | None = None) -> logging.Logger:
    """Initialize a structured logger that writes to console and optional file."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        if log_file is not None:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    return logger


@contextmanager
def log_scope(logger: logging.Logger, scope_name: str) -> Iterator[None]:
    """Log entry and exit around a processing scope."""
    logger.info("Entering %s", scope_name)
    try:
        yield
    finally:
        logger.info("Exiting %s", scope_name)


def time_execution(function: callable) -> callable:
    """Decorator that logs execution time for a function."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        duration = time.perf_counter() - start_time
        logger = logging.getLogger(function.__module__)
        logger.info("%s executed in %.6fs", function.__name__, duration)
        return result

    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper
