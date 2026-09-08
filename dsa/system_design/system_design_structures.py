"""System design data structures: LRU Cache, Trie, Bloom Filter."""

from __future__ import annotations

import hashlib
import math
from collections import OrderedDict, defaultdict
from typing import Any


class LRUCache:
    """Least Recently Used (LRU) cache with O(1) get and put.

    Uses ``collections.OrderedDict`` for O(1) move-to-end.

    Example::

        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")       # returns 1, marks "a" as most recent
        cache.put("c", 3)    # evicts "b"
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._cache: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Any | None:
        """Return the value for *key*, or None if missing. Marks as recently used."""
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: Any, value: Any) -> None:
        """Insert or update *key*. Evicts the LRU item if at capacity."""
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False)

    @property
    def size(self) -> int:
        return len(self._cache)

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self._capacity}, items={dict(self._cache)})"


class LFUCache:
    """Least Frequently Used (LFU) cache with O(1) get and put operations.

    When capacity is reached, evicts the key with minimum frequency.
    Ties in frequency are broken using LRU (least recently used among minimum frequency).
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._vals: dict[Any, Any] = {}
        self._counts: dict[Any, int] = {}
        self._freq_keys: dict[int, OrderedDict[Any, None]] = defaultdict(OrderedDict)
        self._min_freq: int = 0

    def get(self, key: Any) -> Any | None:
        """Return the value for key, or None if not found, updating frequency."""
        if key not in self._vals:
            return None
        count = self._counts[key]
        self._counts[key] = count + 1
        del self._freq_keys[count][key]

        if not self._freq_keys[count] and self._min_freq == count:
            self._min_freq += 1

        self._freq_keys[count + 1][key] = None
        return self._vals[key]

    def put(self, key: Any, value: Any) -> None:
        """Insert or update key-value pair, evicting LFU item if capacity exceeded."""
        if key in self._vals:
            self._vals[key] = value
            self.get(key)
            return

        if len(self._vals) >= self._capacity:
            evict_key, _ = self._freq_keys[self._min_freq].popitem(last=False)
            del self._vals[evict_key]
            del self._counts[evict_key]

        self._vals[key] = value
        self._counts[key] = 1
        self._freq_keys[1][key] = None
        self._min_freq = 1

    @property
    def size(self) -> int:
        return len(self._vals)

    def __len__(self) -> int:
        return len(self._vals)

    def __repr__(self) -> str:
        return f"LFUCache(capacity={self._capacity}, items={self._vals})"


class TrieNode:
    """A node in a Trie (prefix tree)."""

    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end: bool = False


class Trie:
    """A Trie (prefix tree) for efficient string operations.

    Supports insert, search, prefix search, and autocomplete.
    """

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie. O(m) where m = len(word)."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True if the exact *word* is in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Return True if any word in the trie starts with *prefix*."""
        return self._find_node(prefix) is not None

    def autocomplete(self, prefix: str, limit: int = 10) -> list[str]:
        """Return up to *limit* words that start with *prefix*."""
        node = self._find_node(prefix)
        if node is None:
            return []
        results: list[str] = []
        self._collect_words(node, prefix, results, limit)
        return results

    def _find_node(self, prefix: str) -> TrieNode | None:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node: TrieNode, prefix: str, results: list[str], limit: int) -> None:
        if len(results) >= limit:
            return
        if node.is_end:
            results.append(prefix)
        for char in sorted(node.children):
            self._collect_words(node.children[char], prefix + char, results, limit)


class BloomFilter:
    """A space-efficient probabilistic set with tunable false-positive rate.

    Uses multiple hash functions to test membership. Never produces false
    negatives but may produce false positives.

    Args:
        expected_items: Expected number of items to insert.
        fp_rate: Desired false-positive rate (default 1%).
    """

    def __init__(self, expected_items: int = 1000, fp_rate: float = 0.01) -> None:
        self._size = self._optimal_size(expected_items, fp_rate)
        self._num_hashes = self._optimal_hashes(self._size, expected_items)
        self._bit_array = [False] * self._size
        self._count = 0

    def add(self, item: str) -> None:
        """Add an item to the filter."""
        for idx in self._get_indices(item):
            self._bit_array[idx] = True
        self._count += 1

    def __contains__(self, item: str) -> bool:
        """Test whether *item* might be in the filter (may be a false positive)."""
        return all(self._bit_array[idx] for idx in self._get_indices(item))

    def _get_indices(self, item: str) -> list[int]:
        indices: list[int] = []
        for i in range(self._num_hashes):
            digest = hashlib.sha256(f"{i}:{item}".encode()).hexdigest()
            indices.append(int(digest, 16) % self._size)
        return indices

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        return int(-n * math.log(p) / (math.log(2) ** 2))

    @staticmethod
    def _optimal_hashes(m: int, n: int) -> int:
        return max(1, int((m / n) * math.log(2)))

    @property
    def size(self) -> int:
        return self._size

    @property
    def count(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return f"BloomFilter(size={self._size}, hashes={self._num_hashes}, items={self._count})"
