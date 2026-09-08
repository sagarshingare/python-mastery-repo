"""
Reusable decorator utilities for function instrumentation, retries, and advanced metaprogramming.
=================================================================================================
Covers:
- Function decorators (`timer`, `validate_non_empty_string`)
- Parameterized decorators (`retry`, `repeat`)
- Dual-use decorator pattern (supports `@dec` AND `@dec(arg=val)`)
- Stateful class decorators (`CallCounter`)
- Class-level decorators (`singleton_class`, `time_all_methods`)
- Metadata and signature preservation via `functools.wraps`
"""

from __future__ import annotations
import functools
import inspect
import logging
import time
from typing import Any, Callable, Dict, Optional, Tuple, Type, TypeVar, Union, overload

F = TypeVar("F", bound=Callable[..., Any])
C = TypeVar("C", bound=Type[Any])
logger = logging.getLogger(__name__)


# --- 1. Basic Function Decorators ---

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


def validate_non_empty_string(function: F) -> F:
    """Ensure string arguments are non-empty before invoking the function."""

    @functools.wraps(function)
    def wrapper(value: str, *args: Any, **kwargs: Any) -> Any:
        if not value or not value.strip():
            raise ValueError("String value must not be empty")
        return function(value, *args, **kwargs)

    return wrapper  # type: ignore[return-value]


# --- 2. Parameterized Decorator: retry & repeat ---

def retry(max_attempts: int = 3, delay_seconds: float = 0.05) -> Callable[[F], F]:
    """Retry a function until it succeeds or exceeds the maximum attempts."""

    def decorator(function: F) -> F:

        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[BaseException] = None
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
                    if attempt < max_attempts and delay_seconds > 0:
                        time.sleep(delay_seconds)
            if last_exception:
                raise last_exception
            return None

        return wrapper  # type: ignore[return-value]

    return decorator


def repeat(num_times: int = 2) -> Callable[[F], F]:
    """Execute the decorated function multiple times, returning the last result."""

    def decorator(function: F) -> F:
        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = None
            for _ in range(num_times):
                result = function(*args, **kwargs)
            return result

        return wrapper  # type: ignore[return-value]

    return decorator


# --- 3. Pure Function Memoization ---

def memoize(function: F) -> F:
    """Cache results of a pure function based on its input arguments."""
    cache: Dict[Tuple[Any, ...], Any] = {}

    @functools.wraps(function)
    def wrapper(*args: Any) -> Any:
        if args in cache:
            logger.debug("Cache hit for %s with args=%s", function.__name__, args)
            return cache[args]
        result = function(*args)
        cache[args] = result
        return result

    # Expose cache inspection and clearing
    setattr(wrapper, "cache", cache)
    setattr(wrapper, "clear_cache", cache.clear)
    return wrapper  # type: ignore[return-value]


# --- 4. Dual-Use Decorator (Parenthesized or Bare) ---

def audit_log(_func: Optional[F] = None, *, action: str = "DEFAULT_ACTION") -> Any:
    """Dual-use decorator: can be used as `@audit_log` OR `@audit_log(action='CUSTOM')`."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info("[AUDIT] Action: '%s' invoked on function '%s'", action, func.__name__)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    if _func is None:
        # Called with arguments: @audit_log(action='...')
        return decorator
    # Called bare: @audit_log
    return decorator(_func)


# --- 5. Class as a Decorator (Stateful Decorator) ---

class CallCounter:
    """A decorator implemented as a class that maintains per-function invocation state."""

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func
        self.call_count: int = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.call_count += 1
        return self.func(*args, **kwargs)

    def reset(self) -> None:
        self.call_count = 0


# --- 6. Class Decorators ---

def singleton_class(cls: C) -> C:
    """Class decorator that enforces singleton instance pattern."""
    instances: Dict[Type[Any], Any] = {}

    @functools.wraps(cls, updated=())
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance  # type: ignore[return-value]
