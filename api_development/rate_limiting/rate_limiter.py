"""Rate limiting algorithms: Token Bucket and Sliding Window log.

Thread-safe implementations designed for production API gateways, endpoints, and background jobs.
"""

from __future__ import annotations

import collections
import threading
import time
from functools import wraps
from typing import Any, Callable


class RateLimitExceeded(Exception):
    """Raised when a request exceeds the configured rate limit."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: float = 0.0) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class TokenBucket:
    """Thread-safe Token Bucket rate limiter.

    Allows bursts up to ``capacity`` and refills tokens smoothly at ``refill_rate`` per second.

    Example::

        limiter = TokenBucket(capacity=10, refill_rate=2.0)
        if limiter.consume():
            # Process request
            pass
    """

    def __init__(self, capacity: int, refill_rate: float) -> None:
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("capacity and refill_rate must be positive.")
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = float(refill_rate)
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self, now: float) -> None:
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        """Attempt to consume *tokens*. Return True if successful, False otherwise."""
        with self._lock:
            now = time.monotonic()
            self._refill(now)
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def time_until_available(self, tokens: int = 1) -> float:
        """Calculate estimated seconds until requested tokens will be available."""
        with self._lock:
            now = time.monotonic()
            self._refill(now)
            if self.tokens >= tokens:
                return 0.0
            deficit = tokens - self.tokens
            return deficit / self.refill_rate


class SlidingWindowRateLimiter:
    """Thread-safe sliding log window rate limiter.

    Maintains timestamps of requests within a moving time window (e.g. 100 requests per 60 seconds).
    Accurately avoids the burst-at-boundary flaw of fixed window counters.
    """

    def __init__(self, max_requests: int, window_seconds: float) -> None:
        if max_requests <= 0 or window_seconds <= 0:
            raise ValueError("max_requests and window_seconds must be positive.")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # client_id -> deque of monotonic timestamps
        self._windows: dict[str, collections.deque[float]] = collections.defaultdict(collections.deque)
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> bool:
        """Check and record request for *client_id*. Returns True if within limit."""
        with self._lock:
            now = time.monotonic()
            q = self._windows[client_id]
            cutoff = now - self.window_seconds

            # Purge timestamps older than current window
            while q and q[0] <= cutoff:
                q.popleft()

            if len(q) < self.max_requests:
                q.append(now)
                return True
            return False

    def retry_after(self, client_id: str) -> float:
        """Returns seconds until the oldest request leaves the window."""
        with self._lock:
            now = time.monotonic()
            q = self._windows[client_id]
            if len(q) < self.max_requests:
                return 0.0
            oldest = q[0]
            return max(0.0, (oldest + self.window_seconds) - now)


def rate_limit(
    max_requests: int,
    window_seconds: float,
    key_func: Callable[..., str] | None = None,
) -> Callable[..., Any]:
    """Decorator to rate limit function calls per key (or globally)."""
    limiter = SlidingWindowRateLimiter(max_requests, window_seconds)

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = key_func(*args, **kwargs) if key_func else "global"
            if not limiter.is_allowed(key):
                retry = limiter.retry_after(key)
                raise RateLimitExceeded(
                    f"Rate limit of {max_requests} requests per {window_seconds}s exceeded for key '{key}'.",
                    retry_after=round(retry, 2),
                )
            return fn(*args, **kwargs)

        wrapper.limiter = limiter  # type: ignore[attr-defined]
        return wrapper

    return decorator
