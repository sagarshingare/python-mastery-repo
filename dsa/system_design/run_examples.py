"""Run System Design data structure demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.system_design.system_design_structures import (
    BloomFilter,
    LFUCache,
    LRUCache,
    Trie,
)

logger = logging.getLogger(__name__)


def run_lru_cache_examples() -> None:
    logger.info("Running LRUCache demonstrations")
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    print(f"LRUCache after put('a', 1), put('b', 2): {cache}")
    print(f"get('a') -> {cache.get('a')} (marks 'a' recently used)")
    cache.put("c", 3)  # evicts 'b'
    print(f"After put('c', 3): get('b') -> {cache.get('b')} (evicted!), get('c') -> {cache.get('c')}")


def run_lfu_cache_examples() -> None:
    logger.info("Running LFUCache demonstrations")
    lfu = LFUCache(capacity=2)
    lfu.put(1, 10)
    lfu.put(2, 20)
    print(f"LFU get(1) -> {lfu.get(1)} (freq of 1 is now 2)")
    lfu.put(3, 30)  # capacity full: key 2 has freq 1, key 1 has freq 2 => evict 2
    print(f"After put(3, 30): get(2) -> {lfu.get(2)} (evicted!), get(3) -> {lfu.get(3)}, get(1) -> {lfu.get(1)}")


def run_trie_examples() -> None:
    logger.info("Running Trie (prefix tree) demonstrations")
    trie = Trie()
    for word in ["apple", "app", "application", "apt", "banana", "band"]:
        trie.insert(word)

    print(f"search('app') -> {trie.search('app')}")
    print(f"search('appl') -> {trie.search('appl')}")
    print(f"starts_with('app') -> {trie.starts_with('app')}")
    print(f"autocomplete('app', limit=5) -> {trie.autocomplete('app')}")
    print(f"autocomplete('ban', limit=5) -> {trie.autocomplete('ban')}")


def run_bloom_filter_examples() -> None:
    logger.info("Running BloomFilter probabilistic membership demonstrations")
    bf = BloomFilter(expected_items=100, fp_rate=0.01)
    for email in ["alice@example.com", "bob@example.com", "charlie@example.com"]:
        bf.add(email)

    print(f"Contains 'alice@example.com': {'alice@example.com' in bf}")
    print(f"Contains 'eve@example.com': {'eve@example.com' in bf}")
    print(f"Bloom filter stats: size={bf.size} bits, items={bf.count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run System Design data structure examples")
    parser.add_argument(
        "--module",
        choices=["lru", "lfu", "trie", "bloom", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "lru":
        run_lru_cache_examples()
    elif args.module == "lfu":
        run_lfu_cache_examples()
    elif args.module == "trie":
        run_trie_examples()
    elif args.module == "bloom":
        run_bloom_filter_examples()
    else:
        run_lru_cache_examples()
        run_lfu_cache_examples()
        run_trie_examples()
        run_bloom_filter_examples()


if __name__ == "__main__":
    main()
