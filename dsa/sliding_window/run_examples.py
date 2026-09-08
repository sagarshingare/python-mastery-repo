"""Run Sliding Window algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.sliding_window.sliding_window import (
    count_anagram_substrings,
    longest_substring_k_distinct,
    max_consecutive_ones,
    max_sum_subarray,
    min_window_substring,
)

logger = logging.getLogger(__name__)


def run_fixed_window_examples() -> None:
    logger.info("Running fixed-size sliding window (max subarray sum of size k, anagram count)")
    nums = [2, 1, 5, 1, 3, 2]
    k = 3
    print(f"max_sum_subarray({nums}, k={k}) -> {max_sum_subarray(nums, k)}")

    s = "cbaebabacd"
    p = "abc"
    anagrams = count_anagram_substrings(s, p)
    print(f"count_anagram_substrings('{s}', '{p}') -> count: {anagrams}")


def run_dynamic_window_examples() -> None:
    logger.info("Running dynamic/variable sliding window (k distinct, min window, max ones)")
    text = "eceba"
    k = 2
    print(f"longest_substring_k_distinct('{text}', k={k}) -> {longest_substring_k_distinct(text, k)}")

    s = "ADOBECODEBANC"
    t = "ABC"
    print(f"min_window_substring('{s}', '{t}') -> '{min_window_substring(s, t)}'")

    bits = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    flips = 2
    print(f"max_consecutive_ones({bits}, k={flips}) -> {max_consecutive_ones(bits, flips)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Sliding Window examples")
    parser.add_argument(
        "--module",
        choices=["fixed", "dynamic", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "fixed":
        run_fixed_window_examples()
    elif args.module == "dynamic":
        run_dynamic_window_examples()
    else:
        run_fixed_window_examples()
        run_dynamic_window_examples()


if __name__ == "__main__":
    main()
