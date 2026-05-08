"""Core Python collection utilities for built-in and specialized collection types.

Python version: 3.10+

This module demonstrates the collection classes that are commonly used in
production Python code. It covers built-in sequence and set types plus the
specialized tools from the `collections` module.
"""

from __future__ import annotations

from collections import Counter, ChainMap, OrderedDict, UserDict, deque, defaultdict, namedtuple
from typing import Iterable, TypeVar

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


def flatten_list(nested: Iterable[Iterable[int]]) -> list[int]:
    """Flatten nested iterables of ints into a single list.

    Example:
        [[1, 2], [3]] -> [1, 2, 3]
    """
    return [item for sublist in nested for item in sublist]


def list_to_tuple(items: Iterable[T]) -> tuple[T, ...]:
    """Convert a list-like iterable into an immutable tuple."""
    return tuple(items)


def tuple_to_list(values: tuple[T, ...]) -> list[T]:
    """Convert a tuple to a mutable list."""
    return list(values)


def count_keywords(words: Iterable[str]) -> dict[str, int]:
    """Count keyword occurrences with Counter.

    Example:
        ["python", "code", "python"] -> {"python": 2, "code": 1}
    """
    return dict(Counter(words))


def group_by_category(items: Iterable[tuple[str, int]]) -> dict[str, list[int]]:
    """Group numeric values by category label using defaultdict.

    Example:
        [("a", 1), ("b", 2), ("a", 3)] -> {"a": [1, 3], "b": [2]}
    """
    groups: dict[str, list[int]] = defaultdict(list)
    for category, value in items:
        groups[category].append(value)
    return dict(groups)


def unique_preserve_order(items: Iterable[T]) -> list[T]:
    """Return a list of unique values preserving insertion order."""
    return list(dict.fromkeys(items))


def build_frozenset(items: Iterable[T]) -> frozenset[T]:
    """Build an immutable frozenset from the provided items."""
    return frozenset(items)


def frozenset_operations(first: frozenset[T], second: frozenset[T]) -> dict[str, frozenset[T]]:
    """Return common immutable set operations between two frozensets."""
    return {
        "union": first | second,
        "intersection": first & second,
        "difference": first - second,
        "symmetric_difference": first ^ second,
    }


def invert_dictionary(mapping: dict[K, V]) -> dict[V, list[K]]:
    """Invert a dictionary mapping while preserving duplicate values."""
    inverted: dict[V, list[K]] = defaultdict(list)
    for key, value in mapping.items():
        inverted[value].append(key)
    return dict(inverted)


def merge_dictionaries(*mappings: dict[K, V]) -> dict[K, V]:
    """Merge dictionaries into a single mapping; later values override earlier ones."""
    result: dict[K, V] = {}
    for mapping in mappings:
        result.update(mapping)
    return result


def set_operations(first: set[T], second: set[T]) -> dict[str, set[T]]:
    """Return union, intersection, difference, and symmetric difference."""
    return {
        "union": first | second,
        "intersection": first & second,
        "difference": first - second,
        "symmetric_difference": first ^ second,
    }


def build_named_person(name: str, age: int, title: str) -> tuple[str, int, str]:
    """Create a namedtuple representing a person.

    The returned object is tuple-like and allows access via named fields.
    """
    Person = namedtuple("Person", ["name", "age", "title"])
    return Person(name, age, title)


def build_ordered_counts(words: Iterable[str]) -> OrderedDict[str, int]:
    """Create a frequency-ordered dictionary of word counts."""
    counts = Counter(words)
    return OrderedDict(counts.most_common())


def merge_config_maps(*maps: dict[str, V]) -> ChainMap[str, V]:
    """Overlay multiple configuration maps using ChainMap.

    Later maps shadow keys from earlier maps without merging values.
    """
    return ChainMap(*maps)


def build_deque(items: Iterable[T], maxlen: int | None = None) -> deque[T]:
    """Create a deque for efficient appends and pops from both ends."""
    return deque(items, maxlen=maxlen)


def rotate_deque(buffer: deque[T], steps: int) -> deque[T]:
    """Rotate a deque in place by the given number of steps."""
    buffer.rotate(steps)
    return buffer


def normalize_mapping_keys(mapping: dict[str, V]) -> UserDict[str, V]:
    """Return a UserDict with normalized lowercase string keys."""
    normalized = {key.lower(): value for key, value in mapping.items()}
    return UserDict(normalized)
