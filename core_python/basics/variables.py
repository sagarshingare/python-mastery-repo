"""Variable examples demonstrating Python assignment, typing, and immutability.

This module shows how values are created and transformed using Python primitives.
Each function includes a description of what it does and the expected output.
"""

from __future__ import annotations

import logging
import sys
from typing import Iterable, Tuple

logger = logging.getLogger(__name__)

PYTHON_VERSION = sys.version.split()[0]
"""The Python interpreter version used by this module."""

DEFAULT_DISCOUNT_RATE = 0.1
"""A constant representing the default discount rate for pricing examples."""


def compute_discounted_price(price: float, discount_rate: float = DEFAULT_DISCOUNT_RATE) -> float:
    """Calculate a discounted price while validating numeric input.

    This function demonstrates assignment of local variables, basic math, and
    defensive validation for business-critical pricing logic.

    Args:
        price: The original product price.
        discount_rate: The discount percentage expressed as a decimal.

    Returns:
        The final price after discount.

    Raises:
        ValueError: If inputs are invalid.

    Example:
        >>> compute_discounted_price(100.0, 0.2)
        80.0
    """
    logger.debug("Computing discounted price: price=%s, discount_rate=%s", price, discount_rate)

    if price < 0:
        logger.error("Invalid price %s: price must be non-negative", price)
        raise ValueError("price must be non-negative")
    if not 0 <= discount_rate <= 1:
        logger.error("Invalid discount_rate %s: must be between 0 and 1", discount_rate)
        raise ValueError("discount_rate must be between 0 and 1")

    final_price = price * (1 - discount_rate)
    logger.info("Final price calculated: %s", final_price)
    return round(final_price, 2)


def swap_values(first: str, second: str) -> tuple[str, str]:
    """Swap two values using tuple unpacking.

    Python allows multiple assignment in a single statement. This function
    returns the swapped values without needing a temporary variable.

    Args:
        first: The first value.
        second: The second value.

    Returns:
        A tuple containing the swapped pair.

    Example:
        >>> swap_values("a", "b")
        ("b", "a")
    """
    logger.debug("Swapping values: first=%s, second=%s", first, second)
    return second, first


def split_full_name(full_name: str) -> tuple[str, str]:
    """Split a full name into first and last name using unpacking.

    Args:
        full_name: A string containing a first and last name.

    Returns:
        A tuple with (first_name, last_name).

    Example:
        >>> split_full_name("Jane Doe")
        ("Jane", "Doe")
    """
    first_name, last_name = full_name.strip().split(" ", 1)
    logger.debug("Split full name %s into first=%s last=%s", full_name, first_name, last_name)
    return first_name, last_name


def compute_compound_interest(principal: float, rate: float, periods: int) -> float:
    """Calculate compound interest using a loop and repeated assignment.

    Args:
        principal: The starting balance.
        rate: The interest rate per period.
        periods: The number of compounding periods.

    Returns:
        The balance after compounding rounded to two decimals.

    Example:
        >>> compute_compound_interest(1000.0, 0.05, 2)
        1102.5
    """
    if principal < 0 or periods < 0:
        raise ValueError("principal and periods must be non-negative")

    balance = principal
    for period in range(periods):
        balance *= 1 + rate
        logger.debug("Period %s balance=%s", period + 1, balance)
    return round(balance, 2)


def describe_sequence_behavior(values: Iterable[int]) -> tuple[list[int], tuple[int, ...]]:
    """Demonstrate iterable conversion and immutability.

    This function converts an iterable to a list and a tuple so learners can see
    how mutable and immutable sequences behave in Python.

    Args:
        values: A sequence of integers.

    Returns:
        A tuple containing the list and tuple versions.

    Example:
        >>> describe_sequence_behavior([1, 2, 3])
        ([1, 2, 3], (1, 2, 3))
    """
    value_list = list(values)
    value_tuple = tuple(value_list)
    logger.debug("Converted values to list=%s and tuple=%s", value_list, value_tuple)
    return value_list, value_tuple
