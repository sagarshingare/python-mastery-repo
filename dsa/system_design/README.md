# System Design Data Structures

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.13: System Design Data Structures**

Low-level data structures powering high-throughput, low-latency distributed systems and caching layers.

## Key Data Structures

- **`LRUCache`**: Constant time $O(1)$ `get()` and `put()` eviction cache backed by `collections.OrderedDict`.
- **`Trie` & `TrieNode`**: Prefix tree supporting fast dictionary insertion, exact lookup, and autocomplete prefix search.
- **`BloomFilter`**: Space-efficient probabilistic set with tunable false-positive rate using optimal multi-hash calculation.

## Quick Start

```python
from dsa.system_design import BloomFilter, LRUCache, Trie

# LRU Cache
cache = LRUCache(capacity=2)
cache.put("x", 1)
cache.put("y", 2)
assert cache.get("x") == 1
cache.put("z", 3)  # Evicts 'y'
assert cache.get("y") is None

# Trie
trie = Trie()
trie.insert("python")
trie.insert("pytest")
assert trie.starts_with("py") == ["pytest", "python"]

# Bloom Filter
bf = BloomFilter(expected_items=1000, fp_rate=0.01)
bf.add("user_42")
assert "user_42" in bf
assert "user_99" not in bf
```
