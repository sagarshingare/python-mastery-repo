"""Reusable decorator utilities for function instrumentation and retries."""

from __future__ import annotations

import functools
import logging
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])
logger = logging.getLogger(__name__)


def timer(function: F) -> F:
    """Measure the execution time of a function and log the result."""

    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        duration = time.perf_counter() - start
        logger.info("%s executed in %.6fs", function.__name__, duration)
        return result

    return wrapper  # type: ignore[return-value]


def retry(max_attempts: int = 3, delay_seconds: float = 0.5) -> Callable[[F], F]:
    """Retry a function until it succeeds or exceeds the maximum attempts."""

    def decorator(function: F) -> F:

        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: BaseException | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return function(*args, **kwargs)
                except Exception as error:
                    last_exception = error
                    logger.warning(
                        "Attempt %d/%d failed for %s: %s",
                        attempt,
                        max_attempts,
                        function.__name__,
                        error,
                    )
                    time.sleep(delay_seconds)
            raise last_exception  # type: ignore[raise-value]

        return wrapper  # type: ignore[return-value]

    return decorator


def memoize(function: F) -> F:
    """Cache results of a pure function based on its input arguments."""
    cache: dict[tuple[Any, ...], Any] = {}

    @functools.wraps(function)
    def wrapper(*args: Any) -> Any:
        if args in cache:
            logger.debug("Cache hit for %s with args=%s", function.__name__, args)
            return cache[args]
        result = function(*args)
        cache[args] = result
        return result

    return wrapper  # type: ignore[return-value]


def validate_non_empty_string(function: F) -> F:
    """Ensure string arguments are non-empty before invoking the function."""

    @functools.wraps(function)
    def wrapper(value: str, *args: Any, **kwargs: Any) -> Any:
        if not value or not value.strip():
            raise ValueError("String value must not be empty")
        return function(value, *args, **kwargs)

    return wrapper  # type: ignore[return-value]
