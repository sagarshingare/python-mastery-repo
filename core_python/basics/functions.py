"""Python function utilities and advanced function patterns.

This module demonstrates production-ready Python function design, including:
- positional-only and keyword-only parameter styles
- default arguments and variable positional/keyword arguments
- closures and partial application
- higher-order functions and composition
- memoization decorators for performance
- safe numeric operations

Python version: 3.10+
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import wraps
from typing import Any, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def calculate_summary_statistics(values: Iterable[float], *, round_digits: int = 2) -> dict[str, float]:
    """Return min, max, average, and count for numeric values.

    Args:
        values: Iterable of floating-point values.
        round_digits: Number of decimal digits to keep for summary values.

    Returns:
        A dictionary containing min, max, average, and count.

    Example:
        calculate_summary_statistics([1.0, 2.0, 3.0]) -> {'min': 1.0, 'max': 3.0, 'average': 2.0, 'count': 3}
    """
    values_list = list(values)
    if not values_list:
        raise ValueError("values must not be empty")

    minimum = min(values_list)
    maximum = max(values_list)
    average = sum(values_list) / len(values_list)
    return {
        "min": round(minimum, round_digits),
        "max": round(maximum, round_digits),
        "average": round(average, round_digits),
        "count": len(values_list),
    }


def build_greeting(prefix: str, *parts: str, separator: str = " ") -> str:
    """Build a full greeting by concatenating positional string parts.

    Args:
        prefix: Introductory word such as 'Hello' or 'Welcome'.
        *parts: String fragments to include in the greeting.
        separator: Separator used between parts.

    Returns:
        A concatenated greeting string.

    Example:
        build_greeting('Hello', 'world', 'from', 'Python') -> 'Hello world from Python'
    """
    return separator.join((prefix, *parts))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers and return a default value when denominator is zero.

    Args:
        numerator: Dividend value.
        denominator: Divisor value.
        default: Fallback return value when denominator is zero.

    Returns:
        The quotient or the default value.

    Example:
        safe_divide(10.0, 2.0) -> 5.0
        safe_divide(10.0, 0.0) -> 0.0
    """
    if denominator == 0:
        return default
    return numerator / denominator


def merge_options(*dicts: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    """Merge multiple dictionaries and apply runtime keyword overrides.

    Args:
        *dicts: Dictionary values to merge left-to-right.
        **overrides: Keyword arguments that override merged values.

    Returns:
        A new dictionary containing merged options.

    Example:
        merge_options({'a': 1}, {'b': 2}, a=3) -> {'a': 3, 'b': 2}
    """
    merged: dict[str, Any] = {}
    for source in dicts:
        merged.update(source)
    merged.update(overrides)
    return merged


def filter_map_example(values: Iterable[T], predicate: Callable[[T], bool], transformer: Callable[[T], R]) -> list[R]:
    """Filter elements using a predicate and map them with a transformer.

    Args:
        values: Values to process.
        predicate: Function that returns True for elements to keep.
        transformer: Function to apply to each kept element.

    Returns:
        A list of transformed elements.

    Example:
        filter_map_example([1, 2, 3], lambda x: x % 2 == 1, lambda x: x * 10) -> [10, 30]
    """
    return [transformer(item) for item in values if predicate(item)]


def make_power(exponent: int) -> Callable[[float], float]:
    """Return a closure that raises values to the configured exponent.

    Args:
        exponent: Power to apply in the returned function.

    Returns:
        A function that applies exponentiation to a number.

    Example:
        square = make_power(2)
        square(3.0) -> 9.0
    """
    def power(value: float) -> float:
        return value ** exponent

    return power


def compose(*functions: Callable[..., Any]) -> Callable[..., Any]:
    """Compose multiple functions into a single pipeline.

    Args:
        *functions: Functions to compose from left to right.

    Returns:
        A new function that applies each function in order.

    Example:
        composed = compose(str.upper, lambda s: s + '!')
        composed('hello') -> 'HELLO!'
    """
    def composed(value: Any) -> Any:
        for fn in functions:
            value = fn(value)
        return value

    return composed


def positional_only_example(a: int, b: int, /, c: int, *, d: int = 5) -> int:
    """Demonstrate Python positional-only and keyword-only parameters.

    Args:
        a: First positional-only argument.
        b: Second positional-only argument.
        c: Regular positional or keyword argument.
        d: Keyword-only argument with default.

    Returns:
        The sum of all arguments.

    Example:
        positional_only_example(1, 2, 3, d=4) -> 10
    """
    return a + b + c + d


def keyword_only_example(value: int, *, factor: int = 2) -> int:
    """Demonstrate keyword-only function parameters for safer APIs.

    Args:
        value: Input integer.
        factor: Multiplicative factor supplied as a keyword.

    Returns:
        The scaled value.

    Example:
        keyword_only_example(3, factor=4) -> 12
    """
    return value * factor


def apply_transformations(value: T, *functions: Callable[[T], T]) -> T:
    """Apply a pipeline of transformations to a value.

    This helper shows how to accept an arbitrary number of callable arguments.
    """
    for fn in functions:
        value = fn(value)
    return value


def memoize(function: Callable[..., R]) -> Callable[..., R]:
    """Simple memoization decorator for pure functions."""
    cache: dict[tuple[Any, ...], R] = {}

    @wraps(function)
    def wrapper(*args: Any) -> R:
        key = tuple(args)
        if key not in cache:
            cache[key] = function(*args)
        return cache[key]

    return wrapper


@memoize
def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number using recursion with memoization."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n in (0, 1):
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
