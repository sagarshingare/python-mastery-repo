"""Context managers for exception handling."""

from __future__ import annotations

import logging
from typing import Any, Type

logger = logging.getLogger(__name__)


class SuppressAndLog:
    """
    A context manager that suppresses specified exceptions and logs them.

    This is useful for silencing non-critical errors in a controlled way.
    """

    def __init__(self, *suppress: Type[Exception]) -> None:
        self._suppress = suppress

    def __enter__(self) -> "SuppressAndLog":
        return self

    def __exit__(
        self,
        exc_type: Type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: Any,
    ) -> bool:
        if exc_type and issubclass(exc_type, self._suppress):
            logger.warning(
                "Suppressed and logged exception: %s: %s", exc_type.__name__, exc_val
            )
            return True  # Suppress the exception
        return False  # Do not suppress other exceptions

