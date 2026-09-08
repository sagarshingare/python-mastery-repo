"""Illustrates best practices for exception handling in Python."""

import logging
from typing import Union

logger = logging.getLogger(__name__)

# ===== BAD PRACTICES =====


def bad_practice_generic_exception(a: int, b: int) -> Union[float, None]:
    """
    BAD PRACTICE: Catches the generic `Exception` class.

    This can hide bugs and make debugging difficult because it catches
    everything, including `SystemExit`, `KeyboardInterrupt`, and other
    exceptions you likely want to propagate.
    """
    try:
        return a / b
    except Exception:  # noqa
        logger.error("Something went wrong, but I don't know what.")
        return None


def bad_practice_swallow_exception(file_path: str) -> None:
    """
    BAD PRACTICE: Swallows an exception without logging or re-raising.

    This is often called "eating" the exception. It completely hides the
    fact that an error occurred, making the system behave unpredictably.
    """
    try:
        with open(file_path, "r") as f:
            _ = f.read()
    except FileNotFoundError:
        # The error is gone, and no one will ever know.
        pass


# ===== GOOD PRACTICES =====


def good_practice_specific_exception(a: int, b: int) -> Union[float, None]:
    """
    GOOD PRACTICE: Catches specific, expected exceptions.

    This allows you to handle different error conditions appropriately and lets
    unexpected errors propagate to be handled at a higher level.
    """
    try:
        return a / b
    except ZeroDivisionError:
        logger.error("Cannot divide by zero.")
        return None
    except TypeError:
        logger.error("Invalid types for division.")
        return None


def good_practice_finally_for_cleanup() -> None:
    """
    GOOD PRACTICE: Uses a `finally` block for cleanup actions.

    The `finally` block is always executed, whether an exception occurred
    or not. This makes it the perfect place for releasing resources like
    files, network connections, or locks.
    """
    resource = None
    try:
        logger.info("Acquiring resource...")
        resource = "locked"
    except Exception:
        logger.error("Failed to acquire resource.")
    finally:
        if resource:
            logger.info("Releasing resource.")
            resource = "unlocked"


def good_practice_clear_error_message(age: int) -> None:
    """
    GOOD PRACTICE: Raises exceptions with clear, informative messages.

    A good error message should explain what went wrong and provide context
    to help with debugging.
    """
    if age < 0:
        raise ValueError(f"Invalid age: {age}. Age cannot be negative.")

