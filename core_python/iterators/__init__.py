"""
Iterators module for iteration protocol, custom iterables, and traversal utilities.
"""

from .iterator_utils import (
    DatasetCollection,
    PeekableIterator,
    RangeIterator,
    group_consecutive,
    pairwise,
    read_until_sentinel,
    take,
)

__all__ = [
    "DatasetCollection",
    "PeekableIterator",
    "RangeIterator",
    "group_consecutive",
    "pairwise",
    "read_until_sentinel",
    "take",
]
