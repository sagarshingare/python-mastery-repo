"""Python control flow examples with practical utility functions.

This module is designed for Python 3.9+ and covers the most common branching and
loop constructs used in production code.
"""

from __future__ import annotations

from typing import Iterable, Iterator, List, Tuple


def filter_positive_numbers(values: Iterable[int]) -> List[int]:
    """Return only positive integers from the input iterable.

    Example:
        [3, -1, 0, 5] -> [3, 5]
    """
    return [value for value in values if value > 0]


def categorize_scores(scores: Iterable[int]) -> List[str]:
    """Map numeric scores to qualitative categories using if/elif/else.

    Example:
        [92, 80, 65, 50] -> ["excellent", "good", "needs_improvement", "failed"]
    """
    categories: list[str] = []
    for score in scores:
        if score >= 90:
            categories.append("excellent")
        elif score >= 75:
            categories.append("good")
        elif score >= 60:
            categories.append("needs_improvement")
        else:
            categories.append("failed")
    return categories


def cumulative_sum(values: Iterable[int]) -> List[int]:
    """Return the running cumulative sum of a numeric iterable.

    Example:
        [1, 2, 3] -> [1, 3, 6]
    """
    total = 0
    result: list[int] = []
    for value in values:
        total += value
        result.append(total)
    return result


def classify_numbers(values: Iterable[int]) -> List[str]:
    """Show conditional evaluation with a ternary-style expression.

    Outputs 'even' for even values and 'odd' for odd values.
    Example:
        [2, 3, 4] -> ["even", "odd", "even"]
    """
    return ["even" if value % 2 == 0 else "odd" for value in values]


def while_sum(limit: int) -> int:
    """Use a while loop to compute the sum of numbers from 1 to limit.

    Example:
        limit=5 -> 15
    """
    total = 0
    current = 1
    while current <= limit:
        total += current
        current += 1
    return total


def find_first_divisible(values: Iterable[int], divisor: int) -> int | None:
    """Find the first value divisible by divisor using a loop with break.

    Returns None when no value is divisible.
    Example:
        values=[5, 7, 10], divisor=5 -> 10
    """
    for value in values:
        if value % divisor == 0:
            return value
    return None


def zip_and_enumerate(keys: Iterable[str], values: Iterable[int]) -> List[Tuple[int, str, int]]:
    """Combine enumerate and zip to pair index, key, and value.

    Example:
        keys=['a', 'b'], values=[1, 2] -> [(0, 'a', 1), (1, 'b', 2)]
    """
    return [(index, key, value) for index, (key, value) in enumerate(zip(keys, values))]


def loop_else_search(values: Iterable[int], target: int) -> str:
    """Demonstrate the else clause on loops.

    If the loop exits normally, the else block executes.
    Example:
        values=[1, 2, 3], target=4 -> 'not found'
    """
    for value in values:
        if value == target:
            return "found"
    else:
        return "not found"


def repeated_pattern(count: int) -> Iterator[int]:
    """Generate repeated values until a stop condition using an iterator.

    Example:
        count=3 -> yields 0, 1, 2
    """
    current = 0
    while current < count:
        yield current
        current += 1
